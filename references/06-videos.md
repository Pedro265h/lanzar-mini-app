# Fase 7 · Videos para Reels (9:16) con voz, la app real y música

## Herramientas

- **HyperFrames** (HTML → MP4): invoca la skill `hyperframes` y lee `hyperframes-core` (contrato de composición). El flujo `product-launch-video` genera la voz con HeyGen o Kokoro; como aquí la voz viene de ElevenLabs, se arma la composición propia con `scripts/video/armar_video.py`.
- **Voz:** Higgsfield `text2speech_v2` con `variant: elevenlabs` (≈0,3 créditos por frase). La voz "Marisol" (`75e72cd5-011b-4130-a474-e8b1ab341f04`) sonó bien en español. **Una frase por escena**, así la duración de cada escena sale del audio. Acepta 2-3 frases a la vez; si da 429, reenvía en tandas.
- **Velocidad:** para un tono de anuncio con presión, `atempo=1.15` con ffmpeg (no cambia el tono); para el emocional, velocidad natural.
- **Subtítulos:** `npx hyperframes transcribe assets/voz-N-r.wav -l es -m small --json` → tiempos por palabra. Se muestra el texto del guion (con tildes y signos) con los tiempos de la transcripción; si el número de palabras no coincide, el tiempo se reparte por largo de palabra. Revisa la transcripción también para confirmar que la voz dijo bien el texto.
- **Fotos en movimiento:** Kling 3.0 (`kling3_0`, std, 5 s, `sound: off`, 9:16, ≈6,25 créditos) con la foto como `start_image` (sirve el `job_id` de la foto generada). Prompt: movimiento sutil y natural, "very slow camera push-in, no text, no morphing". A veces Higgsfield sugiere un "preset" en vez de generar: reenvía con `declined_preset_id`. Si la escena dura más que el clip, alárgalo con `setpts=1.15*PTS`.
- **La app real:** capturas con `cdp2.mjs` en local con datos de ejemplo inyectados (cuenta de prueba, incluso en prueba gratis para que salga "Día 1 de tus 2 días gratis"). Esconde la burbuja de opiniones con CSS. Van dentro de un celular dibujado en CSS, con scroll o fundidos entre pantallas.
- **Música:** `scripts/video/generar_musica.py` (MusicGen local, gratis; con aceleración de la Mac). Da unos 28 s: se alarga con `acrossfade`, fundidos, `loudnorm=I=-20` y `data-volume` ≈0,2 debajo de la voz. Avisa que es música generada y que puede cambiarse.

## Tres ángulos que se complementan

| Video | Voz | Estructura |
|---|---|---|
| **Urgencia** ("3 a. m.") | Rápida, con presión | Gancho de miedo real ("3:00 a. m.") → el problema (internet da más miedo) → aparece la marca y el semáforo real → el bebé creciendo → las dos mamás → cierre con "Pruébala 2 días gratis · Hoy no pagas nada · Toca el botón" |
| **Oferta directa** ("2 días gratis") | Rápida | "2 días gratis" gigante → "DÍA 1" con la app real (Hoy y Tu camino) → semáforo verde y rojo → "DÍA 2" (clase y plan) → recién nacido → lista de chequeo de la oferta |
| **Emocional** ("desde la primera semana") | Natural, con pausas y piano | Test positivo → primer control con las preguntas en burbujas → app en la semana 7 → crece de la 6 a la 40 → parto piel con piel → "Desde la primera semana hasta sus primeros meses" |

## Reglas de diseño y verificación

- Zonas seguras de Reels: arriba 250 px y abajo 330 px los tapa la interfaz. Subtítulos alrededor de y=1270-1430.
- Subtítulos grandes (casi todos ven sin sonido). Resaltado de la palabra activa: durazno sobre fondo oscuro, frambuesa sobre fondo crema. Sobre fondos claros, la tinta va oscura.
- Cambios de pantalla tipo "pasar páginas" (fundidos de 0,06 s) para que no se encimen los textos.
- Fuentes locales con `@font-face` (las pide el lint). Nada de `transform` en CSS sobre lo que anima GSAP.
- Ciclo: `python3 armar_video.py` → `npx hyperframes lint` (0 errores; los avisos de "sub-composición" son de orden y no afectan el render) → `npx hyperframes check` → `npx hyperframes snapshot --at <mitades de escena>` → revisar la hoja de contacto → `npx hyperframes render --quality high`. Un video de 37 s se renderiza en ~30 s.
- Verifica el MP4: `ffprobe` (1080×1920, h264 + aac) y `volumedetect` (voz alrededor de -19 dB de promedio).
- Costo típico por video: 25-31 créditos de Higgsfield si se generan clips nuevos, unos 8 si se reusan.
