# PLANTILLA · Video de anuncio para Reels (9:16) con HyperFrames: una frase de voz por escena, fotos animadas,
# capturas reales de la app en un celular y subtítulos palabra por palabra.
# Los tiempos salen de la duración real de cada voz (assets/voz-N-r.wav) y los subtítulos de la transcripción
# (assets/palabras-N.json, de `npx hyperframes transcribe assets/voz-N-r.wav -l es -m small --json`).
# Edita GUION (las frases exactas que dice la voz), los clips de cada escena y los textos de la marca.
# Uso: python3 armar_video.py → index.html; luego `npx hyperframes lint`, `check`, `snapshot` y `render`.
# Ejemplo real: video "3 a. m." de Mamá Segura, 15-oct-2026.
import html
import json
import subprocess
from pathlib import Path

AQUI = Path(__file__).resolve().parent
A = AQUI / "assets"

GUION = [
    "Son las tres de la mañana… y algo no se siente normal.",
    "¿Esperas? ¿Llamas? ¿Corres a urgencias? Y en internet… solo encuentras más miedo.",
    "Por eso existe Mamá Segura. Le cuentas lo que sientes, y en segundos sabes si es normal, si lo hablas con tu médico… o si es para urgencias.",
    "Mira cómo crece tu bebé, semana a semana. Sube tu ecografía y míralo con sus medidas reales.",
    "Del embarazo a sus primeros meses: contracciones, lactancia, fiebre. Todo en un solo lugar.",
    "¡Pruébala dos días gratis! Hoy no pagas nada. Toca el botón… y deja de vivir con miedo.",
]
ENTRADA = 0.1   # la voz entra un poco después del corte
COLA = [0.3, 0.3, 0.3, 0.3, 0.3, 1.3]  # silencio después de cada frase (la última deja leer el cierre)
SAFE_TOP, SAFE_BOTTOM = 250, 330


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).strip())


def palabras(i, texto, inicio):
    """Las palabras del guion con su tiempo (absoluto). Si la transcripción tiene las mismas, sus tiempos; si no, reparte
    el tramo hablado según el largo de cada palabra."""
    w = json.loads((A / f"palabras-{i}.json").read_text())
    mias = texto.split()
    if len(w) == len(mias):
        return [(m, inicio + x["start"], inicio + x["end"]) for m, x in zip(mias, w)]
    t0, t1 = w[0]["start"], w[-1]["end"]
    total = sum(len(m) + 1 for m in mias)
    out, t = [], t0
    for m in mias:
        d = (t1 - t0) * (len(m) + 1) / total
        out.append((m, inicio + t, inicio + t + d))
        t += d
    return out


def grupos(ws, maximo=4):
    """Corta en frases cortas para los subtítulos: hasta 4 palabras, o antes si hay puntuación."""
    out, act = [], []
    for w in ws:
        act.append(w)
        if len(act) >= maximo or w[0][-1] in ".,?!…:":
            out.append(act)
            act = []
    if act:
        out.append(act)
    return out


# ---------- tiempos ----------
escenas = []
t = 0.0
for i, texto in enumerate(GUION, 1):
    v = dur(A / f"voz-{i}-r.wav")
    d = round(ENTRADA + v + COLA[i - 1], 3)
    escenas.append({"n": i, "inicio": round(t, 3), "dur": d, "voz": v, "texto": texto,
                    "ws": palabras(i, texto, t + ENTRADA)})
    t += d
TOTAL = round(t, 3)
E = {e["n"]: e for e in escenas}
w_at = lambda n, palabra: next(x[1] for x in E[n]["ws"] if palabra.lower() in x[0].lower())  # noqa: E731

e = html.escape
partes, js = [], []

# ---------- fondos (videos y marca) ----------
def video(id_, src, n):
    s = E[n]
    partes.append(f'<video id="{id_}" class="clip media" src="assets/{src}" muted playsinline data-start="{s["inicio"]}" data-duration="{s["dur"]}" data-track-index="0"></video>')


video("v-noche", "clip-noche-l.mp4", 1)
video("v-fiebre", "clip-fiebre-l.mp4", 2)
video("v-ambas", "clip-ambas-l.mp4", 5)
video("v-calma", "clip-calma-l.mp4", 6)
for n in (1, 2, 5):
    s = E[n]
    partes.append(f'<div id="velo-{n}" class="clip velo" data-start="{s["inicio"]}" data-duration="{s["dur"]}" data-track-index="1"></div>')
s6 = E[6]
partes.append(f'<div id="velo-6" class="clip velo velo-cierre" data-start="{s6["inicio"]}" data-duration="{s6["dur"]}" data-track-index="1"></div>')
marca_ini = E[3]["inicio"]
marca_dur = round(E[3]["dur"] + E[4]["dur"], 3)
partes.append(f'<div id="fondo-marca" class="clip fondo-marca" data-start="{marca_ini}" data-duration="{marca_dur}" data-track-index="0"><div class="orbe orbe-1"></div><div class="orbe orbe-2"></div></div>')

# ---------- escena 1: la hora ----------
s = E[1]
partes.append(f'<div id="hora" class="clip capa" data-start="{s["inicio"]}" data-duration="{s["dur"]}" data-track-index="2"><div class="hora"><span id="hora-num">3:00</span><small>a. m.</small></div></div>')
js.append(f'tl.fromTo("#hora .hora", {{opacity: 0, y: -30}}, {{opacity: 1, y: 0, duration: 0.5, ease: "power3.out"}}, {s["inicio"] + 0.15});')
js.append(f'tl.fromTo("#hora-num", {{opacity: 1}}, {{opacity: 0.35, duration: 0.12, repeat: 3, yoyo: true, ease: "none"}}, {s["inicio"] + 1.2});')

# ---------- escena 3: la marca y el semáforo ----------
s = E[3]
logo = '<svg viewBox="0 0 120 120" aria-hidden="true"><path d="M60 106C22 80 8 60 8 40 8 23 20 12 35 12c11 0 19 6 25 15 6-9 14-15 25-15 15 0 27 11 27 28 0 20-14 40-52 66Z" fill="#FFFFFF"/><path d="M68 84C52 73 46 64 46 55c0-7 5-12 11-12 5 0 8 3 11 7 3-4 6-7 11-7 6 0 11 5 11 12 0 9-6 18-22 29Z" fill="#F4A988"/></svg>'
t_marca = w_at(3, "Mamá")
partes.append(f'<div id="marca" class="clip capa" data-start="{s["inicio"]}" data-duration="1.9" data-track-index="2"><div class="marca-centro">{logo}<div class="marca-nombre">Mamá Segura</div></div></div>')
js.append(f'tl.fromTo("#marca svg", {{scale: 0.4, opacity: 0}}, {{scale: 1, opacity: 1, duration: 0.55, ease: "back.out(1.8)"}}, {s["inicio"] + 0.05});')
js.append(f'tl.fromTo("#marca .marca-nombre", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.45, ease: "power3.out"}}, {t_marca - 0.1});')
js.append(f'tl.to("#marca .marca-centro", {{opacity: 0, y: -60, duration: 0.35, ease: "power2.in"}}, {s["inicio"] + 1.5});')
tel_ini = round(s["inicio"] + 1.7, 3)
partes.append(f'<div id="tel-1" class="clip capa" data-start="{tel_ini}" data-duration="{round(s["inicio"] + s["dur"] - tel_ini, 3)}" data-track-index="3"><div class="telefono"><div class="pantalla"><img id="img-resultado" src="assets/resultado.png" alt=""></div></div><div class="etiqueta-flotante" id="chip-verde"><i></i>Es normal en tu semana</div></div>')
js.append(f'tl.fromTo("#tel-1 .telefono", {{y: 900, rotation: 6}}, {{y: 0, rotation: 0, duration: 0.7, ease: "power3.out"}}, {tel_ini});')
js.append(f'tl.fromTo("#chip-verde", {{opacity: 0, x: 60, scale: 0.8}}, {{opacity: 1, x: 0, scale: 1, duration: 0.45, ease: "back.out(2)"}}, {w_at(3, "normal,") - 0.1});')
js.append(f'tl.fromTo("#img-resultado", {{y: 0}}, {{y: -430, duration: 1.6, ease: "power2.inOut"}}, {w_at(3, "médico") - 0.2});')

# ---------- escena 4: el bebé que crece ----------
s = E[4]
semanas = [8, 12, 16, 20, 24, 28, 32, 36, 40]
imgs = "".join(f'<img class="sem" id="sem-{n}" src="assets/semana-{n:02d}.png" alt="">' for n in semanas)
partes.append(f'<div id="tel-2" class="clip capa" data-start="{s["inicio"]}" data-duration="{s["dur"]}" data-track-index="3"><div class="telefono"><div class="pantalla">{imgs}<img class="sem" id="sem-24b" src="assets/semana-24.png" alt=""></div></div><div class="etiqueta-flotante eco" id="chip-eco"><b>Tu ecografía</b><span>24 semanas · 610 g</span></div></div>')
t_crece = w_at(4, "crece")
paso = 0.42
for k, n in enumerate(semanas):
    js.append(f'tl.fromTo("#sem-{n}", {{opacity: 0}}, {{opacity: 1, duration: 0.06, ease: "none"}}, {round(t_crece - 0.3 + k * paso, 3)});')
t_eco = w_at(4, "ecografía")
js.append(f'tl.fromTo("#sem-24b", {{opacity: 0}}, {{opacity: 1, duration: 0.3, ease: "none"}}, {t_eco - 0.5});')
js.append(f'tl.fromTo("#chip-eco", {{opacity: 0, x: 60, scale: 0.8}}, {{opacity: 1, x: 0, scale: 1, duration: 0.45, ease: "back.out(2)"}}, {t_eco - 0.1});')
js.append(f'tl.fromTo("#tel-2 .telefono", {{scale: 0.96}}, {{scale: 1, duration: {round(s["dur"], 2)}, ease: "none"}}, {s["inicio"]});')

# ---------- escena 5: todo en un lugar ----------
s = E[5]
chips = [("contracciones,", "Contracciones"), ("lactancia,", "Lactancia"), ("fiebre.", "Fiebre"), ("Todo", "Plan de parto"), ("lugar.", "Recién nacido")]
html_chips = "".join(f'<span class="chip" id="chip5-{k}">{e(c)}</span>' for k, (_, c) in enumerate(chips))
partes.append(f'<div id="chips5" class="clip capa" data-start="{s["inicio"]}" data-duration="{s["dur"]}" data-track-index="2"><div class="chips">{html_chips}</div></div>')
for k, (palabra, _) in enumerate(chips):
    js.append(f'tl.fromTo("#chip5-{k}", {{opacity: 0, y: 30, scale: 0.7}}, {{opacity: 1, y: 0, scale: 1, duration: 0.35, ease: "back.out(2.2)"}}, {w_at(5, palabra) - 0.05});')

# ---------- escena 6: el cierre ----------
s = E[6]
partes.append(f'''<div id="cierre" class="clip capa" data-start="{s["inicio"]}" data-duration="{s["dur"]}" data-track-index="2"><div class="cierre">
<div class="cierre-marca">{logo}<span>Mamá Segura</span></div>
<div class="cierre-titulo" id="c-titulo">Pruébala <em>2 días gratis</em></div>
<div class="cierre-sub" id="c-sub">Hoy no pagas nada</div>
<div class="cierre-boton" id="c-boton">Toca el botón y empieza hoy</div>
<div class="cierre-legal">Te orienta, no reemplaza a tu médico</div></div></div>''')
js.append(f'tl.fromTo("#cierre .cierre-marca", {{opacity: 0, y: -20}}, {{opacity: 1, y: 0, duration: 0.4, ease: "power3.out"}}, {s["inicio"] + 0.05});')
js.append(f'tl.fromTo("#c-titulo", {{opacity: 0, scale: 0.85}}, {{opacity: 1, scale: 1, duration: 0.5, ease: "back.out(1.7)"}}, {w_at(6, "Pruébala") - 0.05});')
js.append(f'tl.fromTo("#c-sub", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: 0.4, ease: "power3.out"}}, {w_at(6, "Hoy") - 0.05});')
js.append(f'tl.fromTo("#c-boton", {{opacity: 0, y: 30}}, {{opacity: 1, y: 0, duration: 0.4, ease: "power3.out"}}, {w_at(6, "Toca") - 0.05});')
js.append(f'tl.fromTo("#c-boton", {{scale: 1}}, {{scale: 1.07, duration: 0.35, repeat: 5, yoyo: true, ease: "sine.inOut"}}, {w_at(6, "Toca") + 0.4});')
js.append(f'tl.fromTo("#cierre .cierre-legal", {{opacity: 0}}, {{opacity: 1, duration: 0.4}}, {w_at(6, "Toca")});')

# ---------- destello del corte a la marca ----------
partes.append(f'<div id="destello" class="clip destello" data-start="{round(E[3]["inicio"] - 0.12, 3)}" data-duration="0.45" data-track-index="5"></div>')
js.append(f'tl.fromTo("#destello", {{opacity: 0.9}}, {{opacity: 0, duration: 0.4, ease: "power2.out"}}, {round(E[3]["inicio"] - 0.12, 3)});')

# ---------- voz ----------
for s in escenas:
    partes.append(f'<audio id="voz-{s["n"]}" src="assets/voz-{s["n"]}-r.wav" data-start="{round(s["inicio"] + ENTRADA, 3)}" data-duration="{round(s["voz"], 3)}" data-track-index="6" data-volume="1"></audio>')

# ---------- subtítulos palabra por palabra (no en el cierre: ahí el texto ya está en pantalla) ----------
k = 0
for s in escenas:
    if s["n"] == 6:
        continue
    arriba = 1400 if s["n"] in (3, 4) else 1270
    gs = grupos(s["ws"])
    for j, g in enumerate(gs):
        ini = g[0][1] - 0.05
        fin = (gs[j + 1][0][1] - 0.05) if j + 1 < len(gs) else min(s["inicio"] + s["dur"], g[-1][2] + 0.35)
        spans = " ".join(f'<span class="w" id="w{k}-{m}">{e(w[0])}</span>' for m, w in enumerate(g))
        partes.append(f'<div id="sub-{k}" class="clip sub" style="top:{arriba}px" data-start="{round(ini, 3)}" data-duration="{round(fin - ini, 3)}" data-track-index="4"><p>{spans}</p></div>')
        js.append(f'tl.fromTo("#sub-{k} p", {{y: 18, opacity: 0}}, {{y: 0, opacity: 1, duration: 0.16, ease: "power2.out"}}, {round(ini, 3)});')
        for m, w in enumerate(g):
            js.append(f'tl.set("#w{k}-{m}", {{color: "#FFC9B0", scale: 1.06}}, {round(w[1], 3)});')
            js.append(f'tl.set("#w{k}-{m}", {{color: "#FFFFFF", scale: 1}}, {round(w[2] + 0.02, 3)});')
        k += 1

CSS = f"""
@font-face {{ font-family: "Fraunces"; src: url("assets/fonts/Fraunces-700.woff2") format("woff2"); font-weight: 700; }}
@font-face {{ font-family: "Nunito Sans"; src: url("assets/fonts/NunitoSans-700.woff2") format("woff2"); font-weight: 700; }}
@font-face {{ font-family: "Nunito Sans"; src: url("assets/fonts/NunitoSans-900.woff2") format("woff2"); font-weight: 900; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #2A1420; }}
#root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #2A1420; font-family: "Nunito Sans", sans-serif; }}
.media {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
.velo {{ position: absolute; inset: 0; background: linear-gradient(180deg, rgba(20,8,14,.55) 0%, rgba(20,8,14,0) 28%, rgba(20,8,14,0) 52%, rgba(20,8,14,.78) 100%); }}
.velo-cierre {{ background: linear-gradient(180deg, rgba(120,35,70,.45) 0%, rgba(110,30,62,.82) 45%, rgba(70,18,40,.92) 100%); }}
.fondo-marca {{ position: absolute; inset: 0; background: linear-gradient(160deg, #B5476B 0%, #A63D61 45%, #7E2C49 100%); overflow: hidden; }}
.orbe {{ position: absolute; border-radius: 50%; filter: blur(60px); opacity: .55; }}
.orbe-1 {{ width: 700px; height: 700px; background: #F4A988; left: -260px; top: 120px; }}
.orbe-2 {{ width: 600px; height: 600px; background: #FFD3BF; right: -240px; bottom: 260px; opacity: .35; }}
.capa {{ position: absolute; inset: 0; }}
.hora {{ position: absolute; left: 0; right: 0; top: {SAFE_TOP + 40}px; text-align: center; color: #fff; font-family: "Fraunces", serif; font-weight: 700; font-size: 190px; line-height: 1; text-shadow: 0 8px 40px rgba(0,0,0,.6); }}
.hora small {{ display: block; font-family: "Nunito Sans", sans-serif; font-weight: 900; font-size: 52px; letter-spacing: .12em; margin-top: 10px; color: #FFC9B0; }}
.marca-centro {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 26px; }}
.marca-centro svg {{ width: 260px; height: 260px; }}
.marca-nombre {{ font-family: "Fraunces", serif; font-weight: 700; font-size: 112px; color: #fff; }}
.telefono {{ position: absolute; left: 202px; top: 236px; width: 676px; height: 1136px; border-radius: 74px; background: #1C1018; padding: 18px; box-shadow: 0 40px 90px rgba(30,5,18,.55), inset 0 0 0 3px rgba(255,255,255,.12); }}
.pantalla {{ position: relative; width: 640px; height: 1100px; border-radius: 58px; overflow: hidden; background: #FFF8F3; }}
.pantalla img {{ position: absolute; left: 0; top: 0; width: 640px; height: auto; }}
.pantalla .sem {{ opacity: 0; }}
.etiqueta-flotante {{ position: absolute; right: 36px; top: 300px; display: flex; align-items: center; gap: 14px; background: #fff; color: #2E8B57; font-weight: 900; font-size: 38px; padding: 22px 30px; border-radius: 999px; box-shadow: 0 18px 50px rgba(30,5,18,.35); }}
.etiqueta-flotante i {{ width: 26px; height: 26px; border-radius: 50%; background: #2E8B57; box-shadow: 0 0 0 9px rgba(46,139,87,.18); }}
.etiqueta-flotante.eco {{ flex-direction: column; align-items: flex-start; gap: 4px; color: #3A2433; top: 880px; right: 50px; border-radius: 30px; }}
.etiqueta-flotante.eco b {{ color: #A63D61; font-size: 30px; letter-spacing: .06em; text-transform: uppercase; }}
.etiqueta-flotante.eco span {{ font-size: 40px; }}
.chips {{ position: absolute; left: 60px; right: 60px; top: {SAFE_TOP + 60}px; display: flex; flex-wrap: wrap; justify-content: center; gap: 18px; }}
.chip {{ display: inline-block; background: #fff; color: #3A2433; font-weight: 900; font-size: 46px; padding: 18px 34px; border-radius: 999px; box-shadow: 0 14px 40px rgba(20,5,12,.35); }}
.cierre {{ position: absolute; left: 70px; right: 70px; top: 520px; display: flex; flex-direction: column; align-items: center; text-align: center; color: #fff; }}
.cierre-marca {{ display: flex; align-items: center; gap: 18px; font-family: "Fraunces", serif; font-weight: 700; font-size: 64px; }}
.cierre-marca svg {{ width: 92px; height: 92px; }}
.cierre-titulo {{ margin-top: 70px; font-family: "Fraunces", serif; font-weight: 700; font-size: 132px; line-height: 1.02; }}
.cierre-titulo em {{ font-style: normal; color: #FFC9B0; display: block; }}
.cierre-sub {{ margin-top: 34px; font-weight: 900; font-size: 60px; }}
.cierre-boton {{ margin-top: 80px; background: #fff; color: #A63D61; font-weight: 900; font-size: 52px; padding: 34px 60px; border-radius: 999px; box-shadow: 0 20px 60px rgba(0,0,0,.35); }}
.cierre-legal {{ margin-top: 48px; font-weight: 700; font-size: 30px; opacity: .85; }}
.sub {{ position: absolute; left: 60px; right: 60px; height: 240px; display: flex; align-items: flex-start; justify-content: center; text-align: center; }}
.sub p {{ font-weight: 900; font-size: 76px; line-height: 1.12; color: #fff; text-shadow: 0 4px 0 rgba(0,0,0,.25), 0 6px 26px rgba(0,0,0,.65); }}
.sub .w {{ display: inline-block; }}
.destello {{ position: absolute; inset: 0; background: #FFF8F3; }}
"""

pagina = f"""<!doctype html>
<html lang="es">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>{CSS}</style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="1080" data-height="1920">
      {chr(10).join(partes)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      {chr(10).join(js)}
      window.__timelines["main"] = tl;
      tl.seek(0);
    </script>
  </body>
</html>
"""
(AQUI / "index.html").write_text(pagina)
print("duración", TOTAL, "s ·", len(partes), "elementos")
for s in escenas:
    print(f'  escena {s["n"]}: {s["inicio"]:.2f} → {s["inicio"] + s["dur"]:.2f}')
