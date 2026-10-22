#!/usr/bin/env python3
"""Monta los anuncios de imagen de una mini app en Meta: UNA campaña VLD con un conjunto por anuncio. TODO PAUSED.

Mayor Volumen (LOWEST_COST_WITHOUT_CAP), OUTCOME_SALES, optimiza la compra del píxel de la app, CBO = $10 por anuncio
(ajustable). Cada anuncio lleva su imagen 4:5 en los feeds y la 9:16 en historias y reels (asset_customization_rules),
sin mejoras automáticas de Meta (OPT_OUT). Sin Instagram conectado, sale solo en Facebook.

Uso:
  python3 montar_imagenes.py meta.json
    meta.json  → configuración (copia meta.ejemplo.json): cuenta, página, píxel, link, segmentación y la lista de
                 anuncios con sus imágenes y copys. El registro queda en registro_imagenes.json junto a meta.json:
                 si algo falla a la mitad, se vuelve a correr y sigue donde quedó (no duplica).

Trampas conocidas (Marketing API v24):
  - geo "todo el mundo" pide declarar categorías reguladas de Taiwán y Singapur → se excluyen (excluir_paises).
  - "solo mujeres" fijo exige advantage_audience 0 (con Advantage+ el género es solo sugerencia).
  - página nueva sin Instagram → anuncios con ubicaciones de IG fallan (sub 1772103): instagram = null → solo Facebook.
  - el token necesita acceso a la página: la página debe estar en el portafolio de la cuenta.
"""
import json
import sys
from pathlib import Path

import requests

GRAPH = "https://graph.facebook.com/v24.0"
FB_FEED = ["feed", "profile_feed", "marketplace", "search"]
FB_VERTICAL = ["story", "facebook_reels"]
IG_FEED = ["stream", "ig_search"]
IG_VERTICAL = ["story", "reels", "profile_reels"]
OPT_OUT = {k: {"enroll_status": "OPT_OUT"} for k in (
    "text_optimizations", "image_templates", "image_touchups", "image_animation", "enhance_cta",
    "adapt_to_placement", "image_brightness_and_contrast", "image_uncrop", "inline_comment", "description_automation",
)}
j = lambda x: json.dumps(x, ensure_ascii=False)  # noqa: E731


def main(ruta_config):
    ruta_config = Path(ruta_config).resolve()
    c = json.loads(ruta_config.read_text())
    token = Path(c["token_archivo"]).expanduser().read_text().strip()
    base = ruta_config.parent
    log_path = base / "registro_imagenes.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {"imagenes": {}, "conjuntos": {}, "anuncios": {}, "creativos": {}}
    guardar = lambda: log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2))  # noqa: E731

    def api(metodo, ruta, **datos):
        datos["access_token"] = token
        r = (requests.get if metodo == "GET" else requests.post)(f"{GRAPH}/{ruta}", params=datos if metodo == "GET" else None,
                                                                 data=None if metodo == "GET" else datos, timeout=120)
        d = r.json()
        if "error" in d:
            e = d["error"]
            raise RuntimeError(f"{ruta}: {e.get('message')} | {e.get('error_user_title', '')} {e.get('error_user_msg', '')} (sub {e.get('error_subcode')})")
        return d

    cuenta, pagina, ig = c["cuenta"], c["pagina"], c.get("instagram")
    plataformas = ["facebook", "instagram"] if ig else ["facebook"]
    ig_pos = (lambda pos: {"instagram_positions": pos}) if ig else (lambda pos: {})
    seg = c["segmentacion"]

    # 1. Imágenes (4:5 y 9:16 de cada anuncio)
    for a in c["anuncios"]:
        for clave in ("imagen_45", "imagen_916"):
            archivo = (base / a[clave]).resolve()
            if archivo.name in log["imagenes"]:
                continue
            with open(archivo, "rb") as f:
                d = requests.post(f"{GRAPH}/{cuenta}/adimages", data={"access_token": token}, files={"filename": (archivo.name, f)}, timeout=120).json()
            if "error" in d:
                raise RuntimeError(f"subir {archivo.name}: {d['error'].get('message')}")
            log["imagenes"][archivo.name] = next(iter(d["images"].values()))["hash"]
            guardar()
            print("subida", archivo.name)

    # 2. Campaña
    if "campana" not in log:
        # objetivo: OUTCOME_SALES (compra o prueba) por defecto; OUTCOME_LEADS si se optimiza el evento LEAD (p. ej. un test gratis).
        log["campana"] = api("POST", f"{cuenta}/campaigns", name=c["campana"], objective=c.get("objetivo", "OUTCOME_SALES"), status="PAUSED",
                             special_ad_categories="[]", buying_type="AUCTION",
                             daily_budget=int(round(c.get("presupuesto_por_anuncio_usd", 10) * 100 * len(c["anuncios"]))),
                             bid_strategy="LOWEST_COST_WITHOUT_CAP")["id"]
        guardar()
        print("campaña", c["campana"])

    targeting = {
        "age_min": seg["edad"][0], "age_max": seg["edad"][1],
        "geo_locations": seg.get("geo", {"country_groups": ["worldwide"]}) | {"location_types": ["home", "recent"]},
        "publisher_platforms": plataformas, "facebook_positions": FB_FEED + FB_VERTICAL, **ig_pos(IG_FEED + IG_VERTICAL),
        "targeting_automation": {"advantage_audience": 0 if seg.get("generos") else 1},
    }
    if seg.get("generos"):
        targeting["genders"] = seg["generos"]
    if seg.get("idiomas"):
        targeting["locales"] = seg["idiomas"]
    if seg.get("excluir_paises"):
        targeting["excluded_geo_locations"] = {"countries": seg["excluir_paises"]}

    # 3. Un conjunto por anuncio
    for a in c["anuncios"]:
        aid = a["id"]
        nombre_ad = a["nombre"]
        if aid not in log["creativos"]:
            spec = {
                "images": [
                    {"hash": log["imagenes"][Path(a["imagen_45"]).name], "adlabels": [{"name": "img_feed"}]},
                    {"hash": log["imagenes"][Path(a["imagen_916"]).name], "adlabels": [{"name": "img_vertical"}]},
                ],
                "bodies": [{"text": a["texto"]}], "titles": [{"text": a["titulo"]}], "descriptions": [{"text": a["descripcion"]}],
                "link_urls": [{"website_url": c["link"], "display_url": c.get("link_visible", c["link"])}],
                "call_to_action_types": [c.get("boton", "LEARN_MORE")], "ad_formats": ["SINGLE_IMAGE"], "optimization_type": "PLACEMENT",
                "asset_customization_rules": [
                    {"customization_spec": {"publisher_platforms": plataformas, "facebook_positions": FB_FEED, **ig_pos(IG_FEED)},
                     "image_label": {"name": "img_feed"}, "priority": 1},
                    {"customization_spec": {"publisher_platforms": plataformas, "facebook_positions": FB_VERTICAL, **ig_pos(IG_VERTICAL)},
                     "image_label": {"name": "img_vertical"}, "priority": 2},
                ],
            }
            log["creativos"][aid] = api("POST", f"{cuenta}/adcreatives", name=f"{nombre_ad}_{c.get('fecha', '')}",
                                        object_story_spec=j({"page_id": pagina, **({"instagram_user_id": ig} if ig else {})}),
                                        asset_feed_spec=j(spec), url_tags=c.get("url_tags", ""),
                                        degrees_of_freedom_spec=j({"creative_features_spec": OPT_OUT}))["id"]
            guardar()
        nombre_conj = f'{c["prefijo_conjunto"]}_{a["numero"]}'
        if aid not in log["conjuntos"]:
            log["conjuntos"][aid] = api("POST", f"{cuenta}/adsets", name=nombre_conj, campaign_id=log["campana"], status="PAUSED",
                billing_event="IMPRESSIONS", optimization_goal="OFFSITE_CONVERSIONS",
                promoted_object=j({"pixel_id": c["pixel"], "custom_event_type": c.get("evento", "PURCHASE")}),
                attribution_spec=j([{"event_type": "CLICK_THROUGH", "window_days": 7}, {"event_type": "VIEW_THROUGH", "window_days": 1}]),
                targeting=j(targeting))["id"]
            guardar()
        if aid not in log["anuncios"]:
            log["anuncios"][aid] = api("POST", f"{cuenta}/ads", name=nombre_ad, adset_id=log["conjuntos"][aid], status="PAUSED",
                                       creative=j({"creative_id": log["creativos"][aid]}))["id"]
            guardar()
        print("  listo", nombre_conj, "→", nombre_ad)
    print("registro:", log_path)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    try:
        main(sys.argv[1])
    except RuntimeError as e:
        print("ERROR:", e)
        sys.exit(1)
