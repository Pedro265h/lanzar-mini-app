# PLANTILLA · Anuncios de imagen para Meta (feed 4:5 de 1080x1350 y Reels/Stories 9:16 de 1080x1920).
# Foto realista (fotos/) + titular + una tarjeta igual a la de la app + botón de la oferta. El texto lo pone el HTML,
# no la IA de imágenes, así sale perfecto. Copia este archivo a <proyecto>/marca/ads/, pon las fotos en fotos/ y edita
# ANUNCIOS (titular, sub, tarjeta y posición de la tarjeta para no tapar caras), MARCA y BEBE.
# Uso: python3 armar_anuncios.py  →  html/*.html + pasos-45.json / pasos-916.json
#      ANCHO=1080 ALTO=1350 node ../../scripts/capturas/cdp2.mjs pasos-45.json png   (y 1080x1920 con pasos-916.json)
# Ejemplo real: Mamá Segura (embarazo y recién nacido), 15-oct-2026.
import html, json, pathlib

AQUI = pathlib.Path(__file__).resolve().parent
BEBE = (AQUI.parent.parent / "public/img/bebe/semana-24.jpg").as_uri()
LOGO = """<svg width="44" height="44" viewBox="0 0 120 120" aria-hidden="true"><path d="M60 106C22 80 8 60 8 40 8 23 20 12 35 12c11 0 19 6 25 15 6-9 14-15 25-15 15 0 27 11 27 28 0 20-14 40-52 66Z" fill="#A63D61"/><path d="M68 84C52 73 46 64 46 55c0-7 5-12 11-12 5 0 8 3 11 7 3-4 6-7 11-7 6 0 11 5 11 12 0 9-6 18-22 29Z" fill="#F4A988"/></svg>"""

# tema: oscuro (texto claro sobre la foto de noche) o claro (texto oscuro sobre crema).
# tarjeta: semaforo (color, etiqueta, titulo, pista) · bebe · chips · contador.
# pos: dónde va la tarjeta en cada formato (css), para no tapar caras.
ANUNCIOS = [
    {
        "id": "1-noche", "tema": "oscuro",
        "fotos": {"45": "1-noche-45.png", "916": "1-noche-916.png"},
        "foco": {"45": "center 70%", "916": "center bottom"},
        "titular": "¿Es normal o voy a urgencias?",
        "sub": "Cuéntale lo que sientes y en segundos sabes qué hacer.",
        "tarjeta": {"tipo": "semaforo", "color": "#2E8B57", "etiqueta": "Verde · es normal", "titulo": "Acidez y ardor en la semana 32", "pista": "Comidas pequeñas y no acostarte justo después de comer."},
        "pos": {"45": "right:40px; top:690px; width:470px", "916": "left:44px; top:1220px; width:420px"},
    },
    {
        "id": "2-fiebre", "tema": "oscuro",
        "fotos": {"45": "2-fiebre-45.png", "916": "2-fiebre-916.png"},
        "foco": {"45": "center 75%", "916": "center bottom"},
        "titular": "3 a. m. Llora y lo sientes caliente.",
        "sub": "¿Esperas, llamas al pediatra o vas a urgencias? Te lo decimos al instante.",
        "tarjeta": {"tipo": "semaforo", "color": "#C8323C", "etiqueta": "Rojo · urgencias ahora", "titulo": "Fiebre de 38 °C en un bebé de 3 semanas", "pista": "Antes de los 3 meses, la fiebre siempre es para urgencias."},
        "pos": {"45": "left:40px; top:760px; width:470px", "916": "left:44px; top:1110px; width:520px"},
    },
    {
        "id": "3-eco", "tema": "claro",
        "fotos": {"45": "3-eco-45.png", "916": "3-eco-916.png"},
        "foco": {"45": "center 70%", "916": "center bottom"},
        "titular": "Mira cómo crece tu bebé, semana a semana.",
        "sub": "Su tamaño, su peso y lo que ya puede hacer. Con tu ecografía, sus medidas reales.",
        "tarjeta": {"tipo": "bebe", "semana": "Semana 24", "titulo": "Del tamaño de una mazorca de maíz", "pista": "Unos 30 cm y 600 g"},
        "pos": {"45": "left:40px; top:610px; width:420px", "916": "left:44px; top:880px; width:460px"},
    },
    {
        "id": "4-ambas", "tema": "claro",
        "fotos": {"45": "4-ambas-916.png", "916": "4-ambas-916.png"},
        "foco": {"45": "center 19%", "916": "center bottom"},
        "capa_fin": {"45": 34},
        "titular": "Del embarazo a sus primeros meses, sin miedo.",
        "sub": "Para la que espera a su bebé y para la que ya lo tiene en brazos.",
        "tarjeta": {"tipo": "chips", "chips": ["¿Esto es normal?", "Semana a semana", "Plan de parto", "Recién nacido"]},
        "pos": {"45": "left:40px; right:40px; top:1050px", "916": "left:44px; right:44px; top:1330px"},
    },
    {
        "id": "5-calma", "tema": "claro",
        "fotos": {"45": "5-calma-45.png", "916": "5-calma-916.png"},
        "foco": {"45": "center 75%", "916": "center bottom"},
        "titular": "Esa tranquilidad de saber qué es normal.",
        "sub": "Lactancia, sueño, cordón, cólicos: respuestas claras para ti y tu bebé, a cualquier hora.",
        "tarjeta": {"tipo": "semaforo", "color": "#2E8B57", "etiqueta": "Verde · es normal", "titulo": "Hipo después de mamar", "pista": "Es muy común en recién nacidos y se le pasa solo."},
        "pos": {"45": "left:40px; top:640px; width:440px", "916": "left:44px; top:1235px; width:560px"},
    },
    {
        "id": "6-maleta", "tema": "claro",
        "fotos": {"45": "6-maleta-45.png", "916": "6-maleta-916.png"},
        "foco": {"45": "center 75%", "916": "center bottom"},
        "titular": "¿Cómo sé que ya es el momento?",
        "sub": "Cuenta tus contracciones y ten claras las señales para ir a la clínica.",
        "tarjeta": {"tipo": "contador", "datos": [["5 min", "entre una y otra"], ["1 min", "dura cada una"], ["1 hora", "seguidas así"]], "titulo": "Es momento de ir a tu clínica"},
        "pos": {"45": "left:40px; top:330px; width:470px", "916": "right:44px; top:900px; width:520px"},
    },
]

e = html.escape


def tarjeta(t):
    if t["tipo"] == "semaforo":
        return f"""<div class="t-etq" style="color:{t['color']}"><i style="background:{t['color']}"></i>{e(t['etiqueta'])}</div>
<div class="t-tit">{e(t['titulo'])}</div><div class="t-pista">{e(t['pista'])}</div>"""
    if t["tipo"] == "bebe":
        return f"""<div class="t-bebe"><img src="{BEBE}" alt=""><div><div class="t-etq" style="color:#A63D61">{e(t['semana'])}</div>
<div class="t-tit">{e(t['titulo'])}</div><div class="t-pista">{e(t['pista'])}</div></div></div>"""
    if t["tipo"] == "chips":
        return '<div class="chips">' + "".join(f'<span><b>✓</b>{e(c)}</span>' for c in t["chips"]) + "</div>"
    if t["tipo"] == "contador":
        celdas = "".join(f'<div><strong>{e(a)}</strong><small>{e(b)}</small></div>' for a, b in t["datos"])
        return f"""<div class="t-etq" style="color:#A63D61"><i style="background:#A63D61"></i>Contador de contracciones</div>
<div class="cont">{celdas}</div><div class="t-tit">{e(t['titulo'])}</div>"""
    return ""


def pagina(a, fmt):
    ancho, alto = (1080, 1350) if fmt == "45" else (1080, 1920)
    oscuro = a["tema"] == "oscuro"
    sup = 250 if fmt == "916" else 64  # en Reels/Stories, arriba y abajo los tapa la interfaz
    inf = 330 if fmt == "916" else 48
    tinta = "#FFFFFF" if oscuro else "#3A2433"
    suave = "rgba(255,255,255,.88)" if oscuro else "#5B4352"
    fin = a.get("capa_fin", {}).get(fmt)  # hasta dónde baja el velo de arriba (en %), si las caras quedan altas
    capa_sup = (
        f"linear-gradient(180deg, rgba(22,10,18,.88) 0%, rgba(22,10,18,.62) 26%, rgba(22,10,18,0) {fin or 50}%)"
        if oscuro else
        f"linear-gradient(180deg, rgba(255,248,243,.97) 0%, rgba(255,248,243,.86) {min(24, (fin or 46) - 10)}%, rgba(255,248,243,0) {fin or 46}%)"
    )
    capa_inf = (
        "linear-gradient(0deg, rgba(22,10,18,.9) 0%, rgba(22,10,18,0) 30%)"
        if oscuro else
        "linear-gradient(0deg, rgba(58,36,51,.72) 0%, rgba(58,36,51,0) 30%)"
    )
    tam_tit = 84 if fmt == "916" else 76
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Nunito+Sans:opsz,wght@6..12,600;6..12,800;6..12,900&display=block" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:{ancho}px;height:{alto}px;overflow:hidden;background:#000}}
.lienzo{{position:relative;width:{ancho}px;height:{alto}px;overflow:hidden;font-family:"Nunito Sans",Arial,sans-serif}}
.foto{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:{a['foco'][fmt]}}}
.capa{{position:absolute;inset:0;background:{capa_sup},{capa_inf}}}
.cabeza{{position:absolute;left:56px;right:56px;top:{sup}px}}
h1{{font-family:Fraunces,Georgia,serif;font-weight:700;font-size:{tam_tit}px;line-height:1.03;letter-spacing:-.01em;color:{tinta};text-wrap:balance}}
.sub{{margin-top:22px;font-size:{36 if fmt == '916' else 33}px;line-height:1.3;font-weight:600;color:{suave};max-width:900px;text-wrap:pretty}}
.tarjeta{{position:absolute;{a['pos'][fmt]};background:#FFFFFF;border-radius:28px;padding:26px 28px;box-shadow:0 18px 50px rgba(30,10,20,.35);color:#3A2433}}
.t-etq{{display:flex;align-items:center;gap:10px;font-size:21px;font-weight:900;letter-spacing:.08em;text-transform:uppercase}}
.t-etq i{{width:16px;height:16px;border-radius:50%;display:inline-block;box-shadow:0 0 0 6px rgba(0,0,0,.05)}}
.t-tit{{margin-top:10px;font-family:Fraunces,Georgia,serif;font-weight:600;font-size:34px;line-height:1.12}}
.t-pista{{margin-top:8px;font-size:23px;line-height:1.35;color:#6E5866;font-weight:600}}
.t-bebe{{display:flex;gap:20px;align-items:center}}
.t-bebe img{{width:150px;height:150px;border-radius:50%;object-fit:cover;flex:none;box-shadow:0 0 0 6px #FDE7DD}}
.t-bebe .t-tit{{font-size:30px}}
.tarjeta:has(.chips){{background:transparent;box-shadow:none;padding:0}}
.chips{{display:flex;flex-wrap:wrap;gap:12px}}
.chips span{{display:inline-flex;align-items:center;gap:10px;background:#FFFFFF;border-radius:999px;padding:14px 22px;font-size:26px;font-weight:800;color:#3A2433;box-shadow:0 10px 30px rgba(30,10,20,.18)}}
.chips b{{color:#2E8B57}}
.cont{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}}
.cont div{{background:#FBEDE6;border-radius:18px;padding:14px 10px;text-align:center}}
.cont strong{{display:block;font-family:Fraunces,Georgia,serif;font-size:34px;color:#A63D61}}
.cont small{{display:block;font-size:18px;color:#6E5866;font-weight:700;margin-top:2px}}
.pie{{position:absolute;left:44px;right:44px;bottom:{inf}px;display:flex;align-items:center;justify-content:space-between;gap:18px}}
.marca{{display:flex;align-items:center;gap:12px;color:#FFFFFF;font-family:Fraunces,Georgia,serif;font-weight:700;font-size:38px;text-shadow:0 2px 12px rgba(0,0,0,.35)}}
.marca small{{display:block;font-family:"Nunito Sans",Arial,sans-serif;font-weight:700;font-size:19px;opacity:.9;margin-top:2px}}
.cta{{background:#A63D61;color:#FFFFFF;font-weight:900;font-size:31px;border-radius:999px;padding:24px 38px;white-space:nowrap;box-shadow:0 12px 30px rgba(166,61,97,.45)}}
</style></head><body><div class="lienzo">
<img class="foto" src="../fotos/{a['fotos'][fmt]}" alt="">
<div class="capa"></div>
<div class="cabeza"><h1>{e(a['titular'])}</h1><p class="sub">{e(a['sub'])}</p></div>
<div class="tarjeta">{tarjeta(a['tarjeta'])}</div>
<div class="pie"><div class="marca">{LOGO}<div>Mamá Segura<small>Te orienta, no reemplaza a tu médico</small></div></div><div class="cta">Pruébala 2 días gratis</div></div>
</div></body></html>"""


salida = AQUI / "html"
salida.mkdir(exist_ok=True)
pasos = {"45": [], "916": []}
for a in ANUNCIOS:
    for fmt in ("45", "916"):
        if not (AQUI / "fotos" / a["fotos"][fmt]).exists():
            print("falta la foto", a["fotos"][fmt])
            continue
        nombre = f"{a['id']}-{fmt}"
        (salida / f"{nombre}.html").write_text(pagina(a, fmt))
        pasos[fmt] += [{"ir": (salida / f"{nombre}.html").as_uri(), "esperar": 3500}, {"foto": nombre}]
for fmt, p in pasos.items():
    (AQUI / f"pasos-{fmt}.json").write_text(json.dumps(p, ensure_ascii=False, indent=1))
print("listo:", sum(len(p) // 2 for p in pasos.values()), "anuncios")
