# 🚀 Lanzar Mini App — Skill para Claude

> Lanza una mini app de suscripción de punta a punta: la app en Cloudflare, el cobro en Hotmart con días gratis, los correos que recuperan a quien no compra, el píxel de Meta y una campaña lista con anuncios de imagen y videos para Reels.

---

## ¿Qué hace?

Convierte una idea como *"quiero una app para mamás embarazadas que se venda en Hotmart"* en un producto vendiendo:

1. **Idea y app**: nicho, promesa, stack (Cloudflare Workers + Durable Object + R2), landing con calculadora y panel de administración.
2. **Hotmart con prueba gratis**: links de pago, webhook, la diferencia entre empezar la prueba y la compra real, cancelación desde la app y el diseño del checkout.
3. **Activación en la prueba**: "Tu camino" de 5 pasos para que en 48 horas la persona sienta que la app sigue SU proceso, más una salida honesta y fácil para cancelar.
4. **Correos**: dominio propio para enviar, reenvío de respuestas a tu Gmail y una secuencia de 7 correos personalizados para quien se registró y no compró.
5. **Meta**: píxel + API de conversiones con el mismo id de evento, verificación real (incluida la trampa de los dominios autorizados) y creación de la página.
6. **Anuncios de imagen**: fotos realistas con IA sin texto, armadas en HTML con tarjetas iguales a las de la app, en 4:5 y 9:16.
7. **Videos para Reels**: tres ángulos (urgencia, oferta directa y emocional) con voz, la app real dentro de un celular, subtítulos palabra por palabra y música.
8. **Montaje**: campaña VLD de Mayor Volumen, un conjunto por anuncio, todo en pausa hasta que tú des el OK.

## 🚀 Instalación

### Mac / Linux (1 comando)

```bash
curl -fsSL https://raw.githubusercontent.com/Pedro265h/lanzar-mini-app/main/install.sh | bash
```

### Windows (PowerShell, 1 comando)

```powershell
irm https://raw.githubusercontent.com/Pedro265h/lanzar-mini-app/main/install.ps1 | iex
```

### Manual

```bash
git clone https://github.com/Pedro265h/lanzar-mini-app.git ~/.claude/skills/lanzar-mini-app
```

## 💬 Cómo usarla

Escríbele a Claude algo como:

> *"Quiero lanzar una mini app para dueños de perros, con plan mensual y anual con 2 días gratis en Hotmart"*

> *"Ya tengo los links de Hotmart, conecta el webhook y arma la secuencia de correos"*

> *"Hazme 6 anuncios de imagen y 3 videos y móntalos en pausa en mi cuenta"*

## ⚙️ Requisitos

- **Cloudflare**: cuenta con Workers, un dominio propio y un token de API (Workers, DNS, Email Routing).
- **Hotmart**: producto con oferta mensual y anual (la anual con días de prueba) y credenciales de API.
- **Meta**: cuenta publicitaria, píxel, token de la API de conversiones y un token de la Marketing API.
- **Creativos**: Higgsfield (fotos, clips y voz), HyperFrames (`npx hyperframes`), Node, Python 3, ffmpeg y Google Chrome.
- **Música (opcional)**: `transformers` + `torch` para MusicGen local.

Los tokens nunca van en el código ni en el chat: se guardan en archivos locales o como secretos de Wrangler. `scripts/meta/meta.ejemplo.json` muestra el formato.

## 🛡️ Reglas que la skill respeta

- Todo lo que crea en Meta queda **en pausa**; nada gasta sin tu OK.
- Cambios de configuración de cuentas (webhooks, dominios del píxel, reenvío de correo, páginas del portafolio) se hacen **con tu OK, uno por uno**.
- Nunca manda eventos de prueba inventados a un píxel real.
- En apps de salud: orienta, no diagnostica; las alarmas son reglas fijas y ningún dato de salud viaja a Meta.

## 📁 Estructura

```
lanzar-mini-app/
├── SKILL.md                              # flujo por fases, reglas de oro y firma
├── install.sh / install.ps1              # instaladores de 1 comando
├── references/
│   ├── 01-idea-y-app.md                  # idea, stack, landing, panel
│   ├── 02-hotmart-prueba-gratis.md       # links, webhook, prueba vs compra, checkout
│   ├── 03-activacion-y-correos.md        # "Tu camino" y secuencia de 7 correos
│   ├── 04-meta-pixel-pagina-montaje.md   # eventos, verificación, página, campaña
│   ├── 05-creativos-imagen.md            # fotos con IA + composición en HTML
│   ├── 06-videos.md                      # voz, clips, capturas, música, render
│   └── caso-mama-segura.md               # caso real completo
└── scripts/
    ├── capturas/cdp2.mjs                 # capturas exactas con Chrome sin ventana
    ├── capturas/revisar-pixel.mjs        # confirma que el píxel dispara
    ├── anuncios/armar_anuncios.py        # arma los anuncios de imagen
    ├── video/armar_video.py              # composición HyperFrames con voz y subtítulos
    ├── video/generar_musica.py           # música de fondo con MusicGen
    └── meta/                             # montaje de imágenes y videos por API
```

---

## 👋 Sobre esta versión

Mantenida por **Pedro Hernández**: IA aplicada al marketing y la automatización, en español.
Sistemas reales con Claude Code, agentes y automatizaciones.

### ¿Quieres aprender más?

Si quieres aprender a **crear y lanzar tus propias apps con IA**, de la idea a la venta,
suscríbete a la comunidad:

👉 **https://www.skool.com/pedro-hernandez-7383**

- **Instagram**: [@pedro.hernandez._](https://instagram.com/pedro.hernandez._)

---

_Creada por Pedro_
