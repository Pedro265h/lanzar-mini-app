#!/usr/bin/env python3
"""Agrega un video como anuncio nuevo a la campaña de la mini app: su propio conjunto, misma segmentación. TODO PAUSED.

Uso:
  python3 montar_video.py meta.json <numero> <nombre-corto> <video.mp4> <segundo-de-portada> <copy.json>
    ej.: python3 montar_video.py meta.json 07 video_3am ~/Downloads/videos/video1.mp4 1.8 copy-video1.json
    copy.json → {"texto": "...", "titulo": "...", "descripcion": "..."}

Usa la campaña que creó montar_imagenes.py (registro_imagenes.json junto a meta.json). Sube el video, saca la portada
del segundo indicado con ffmpeg (Meta exige una imagen en video_data), espera a que Meta lo procese y crea
creativo + conjunto + anuncio. El registro queda en registro_videos.json (no repite lo ya creado).
"""
import json
import subprocess
import sys
import time
from pathlib import Path

import requests

GRAPH = "https://graph.facebook.com/v24.0"
FB_POS = ["feed", "profile_feed", "marketplace", "search", "story", "facebook_reels"]
IG_POS = ["stream", "ig_search", "story", "reels", "profile_reels"]
OPT_OUT = {k: {"enroll_status": "OPT_OUT"} for k in (
    "text_optimizations", "image_templates", "image_touchups", "image_animation", "enhance_cta",
    "adapt_to_placement", "image_brightness_and_contrast", "image_uncrop", "inline_comment", "description_automation",
    "video_auto_crop",
)}
j = lambda x: json.dumps(x, ensure_ascii=False)  # noqa: E731


def main(ruta_config, num, corto, video, segundo, ruta_copy):
    ruta_config = Path(ruta_config).resolve()
    c = json.loads(ruta_config.read_text())
    token = Path(c["token_archivo"]).expanduser().read_text().strip()
    base = ruta_config.parent
    campana = json.loads((base / "registro_imagenes.json").read_text())["campana"]
    copy = json.loads(Path(ruta_copy).read_text())
    log_path = base / "registro_videos.json"
    log = json.loads(log_path.read_text()) if log_path.exists() else {}
    reg = log.setdefault(corto, {})
    guardar = lambda: log_path.write_text(json.dumps(log, ensure_ascii=False, indent=2))  # noqa: E731
    video = Path(video).expanduser()

    def api(metodo, ruta, **datos):
        datos["access_token"] = token
        r = (requests.get if metodo == "GET" else requests.post)(f"{GRAPH}/{ruta}", params=datos if metodo == "GET" else None,
                                                                 data=None if metodo == "GET" else datos, timeout=120)
        d = r.json()
        if "error" in d:
            e = d["error"]
            raise RuntimeError(f"{ruta}: {e.get('message')} | {e.get('error_user_title', '')} {e.get('error_user_msg', '')} (sub {e.get('error_subcode')})")
        return d

    cuenta, ig, seg = c["cuenta"], c.get("instagram"), c["segmentacion"]
    if "video_id" not in reg:
        with open(video, "rb") as f:  # hasta ~100 MB va en una sola subida; más grande, subir por partes
            d = requests.post(f"{GRAPH}/{cuenta}/advideos", data={"access_token": token, "name": corto},
                              files={"source": (video.name, f, "video/mp4")}, timeout=600).json()
        if "error" in d:
            raise RuntimeError(f"subir video: {d['error'].get('message')}")
        reg["video_id"] = d["id"]
        guardar()
        print("video subido", reg["video_id"])
    if "portada" not in reg:
        portada = video.with_suffix(".portada.jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(segundo), "-i", str(video), "-frames:v", "1", "-q:v", "2", str(portada)], check=True)
        with open(portada, "rb") as f:
            d = requests.post(f"{GRAPH}/{cuenta}/adimages", data={"access_token": token}, files={"filename": (portada.name, f)}, timeout=120).json()
        if "error" in d:
            raise RuntimeError(f"subir portada: {d['error'].get('message')}")
        reg["portada"] = next(iter(d["images"].values()))["hash"]
        guardar()
    for _ in range(40):  # Meta procesa el video antes de poder usarlo
        estado = api("GET", reg["video_id"], fields="status")["status"].get("video_status")
        if estado == "ready":
            break
        if estado == "error":
            raise RuntimeError("Meta no pudo procesar el video")
        time.sleep(10)
    nombre_ad = f"ad{num}_{corto}"
    if "creativo" not in reg:
        reg["creativo"] = api("POST", f"{cuenta}/adcreatives", name=f"{nombre_ad}_{c.get('fecha', '')}", url_tags=c.get("url_tags", ""),
                              object_story_spec=j({"page_id": c["pagina"], **({"instagram_user_id": ig} if ig else {}), "video_data": {
                                  "video_id": reg["video_id"], "image_hash": reg["portada"], "message": copy["texto"],
                                  "title": copy["titulo"], "link_description": copy["descripcion"],
                                  "call_to_action": {"type": c.get("boton", "LEARN_MORE"), "value": {"link": c["link"]}}}}),
                              degrees_of_freedom_spec=j({"creative_features_spec": OPT_OUT}))["id"]
        guardar()
    if "conjunto" not in reg:
        targeting = {
            "age_min": seg["edad"][0], "age_max": seg["edad"][1],
            "geo_locations": seg.get("geo", {"country_groups": ["worldwide"]}) | {"location_types": ["home", "recent"]},
            "publisher_platforms": ["facebook", "instagram"] if ig else ["facebook"], "facebook_positions": FB_POS,
            **({"instagram_positions": IG_POS} if ig else {}),
            "targeting_automation": {"advantage_audience": 0 if seg.get("generos") else 1},
        }
        if seg.get("generos"):
            targeting["genders"] = seg["generos"]
        if seg.get("idiomas"):
            targeting["locales"] = seg["idiomas"]
        if seg.get("excluir_paises"):
            targeting["excluded_geo_locations"] = {"countries": seg["excluir_paises"]}
        reg["conjunto"] = api("POST", f"{cuenta}/adsets", name=f'{c["prefijo_conjunto"]}_{num}', campaign_id=campana, status="PAUSED",
            billing_event="IMPRESSIONS", optimization_goal="OFFSITE_CONVERSIONS",
            promoted_object=j({"pixel_id": c["pixel"], "custom_event_type": c.get("evento", "PURCHASE")}),
            attribution_spec=j([{"event_type": "CLICK_THROUGH", "window_days": 7}, {"event_type": "VIEW_THROUGH", "window_days": 1}]),
            targeting=j(targeting))["id"]
        guardar()
    if "anuncio" not in reg:
        reg["anuncio"] = api("POST", f"{cuenta}/ads", name=nombre_ad, adset_id=reg["conjunto"], status="PAUSED",
                             creative=j({"creative_id": reg["creativo"]}))["id"]
        guardar()
    print("listo", f'{c["prefijo_conjunto"]}_{num}', "→", nombre_ad)


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print(__doc__)
        sys.exit(1)
    try:
        main(*sys.argv[1:7])
    except RuntimeError as e:
        print("ERROR:", e)
        sys.exit(1)
