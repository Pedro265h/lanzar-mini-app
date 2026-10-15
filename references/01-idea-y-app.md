# Fase 0 y 1 · Idea y app en Cloudflare

## 0. Idea, nicho, nombre y precio

- **Fuente de ideas:** productos que ya venden en el mercado de Hotmart (cursos con miles de ventas). La app NO usa su contenido: toma el dolor del nicho y lo resuelve con una herramienta diaria.
- **Funciones:** 4-6, alrededor de una estrella que responde una duda que da miedo:
  - Semáforo "¿Esto es normal?": lo que siente → verde (normal), amarillo (consultar pronto), rojo (urgencias). Las alarmas son reglas fijas y la IA solo puede subir el nivel.
  - Contenido que hace volver: semana a semana, clases cortas, guías, plan (de parto, de lectura…).
  - Algo visual que enamora: simulador (el bebé crece semana a semana con imágenes realistas), fotos propias (ecografías) que se ven en el simulador.
  - Chat "Pregúntale" con límites diarios.
- **Nombre:** corto, que diga el beneficio. Revisa que el `.app` esté libre ANTES de proponerlo. Si el usuario compra un dominio con un error (p. ej. `mamaegura.app`), avísale una vez; si decide quedarse con él, no lo vuelvas a mencionar.
- **Precio (referencia que funcionó):** mensual US$4,99 · anual US$29,99 con 2 días gratis ("ahorras 50 %", "menos de US$0,09 al día").
- **Contenido de salud:** lo escriben sub-agentes con reglas de seguridad, pero **antes de escalar la pauta debe revisarlo un profesional** (obstetra, pediatra, veterinario). Dilo en la entrega.

## 1. App en Cloudflare (stack probado)

- **Worker + assets estáticos** (`run_worker_first` solo para `/api/*`) · **Durable Object con SQLite** (`Almacen`: usuarios, sesiones, datos, compras, suscripciones, secuencia de correos, embudo, opiniones) · **R2** para fotos privadas · **Email Sending** (binding `send_email`) · **ratelimits** para las rutas de IA.
- **IA:** Claude (`claude-opus-5-5`) con `@anthropic-ai/sdk`: `client.beta.messages.create` con `betas: ["server-side-fallback-2026-07-01"]`, `fallbacks: "default"`, `output_config: { effort, format: json_schema }`. El esquema JSON **sin** `maxItems`. La salida estructurada alimenta el semáforo.
- **Cuentas:** Google (GSI) + código de 6 números por correo. Un admin por lista `ADMINS` (no ve el muro de pago y la secuencia lo salta).
- **Datos:** en `localStorage` (clave `<app>:v1`) y copia en la cuenta (`/api/datos`, se mezcla por id y por `actualizado`). Las fotos grandes van a R2 y en el celular queda una miniatura.
- **Dominio propio:** `routes` con `custom_domain: true` para el dominio y el `www`. La redirección de `www` va **en el HTML** (los assets no pasan por el worker).
- **Google:** agregar el origen `https://<dominio>` al cliente OAuth. Se verifica con una consola sin ventana: si dice "origin not allowed", falta.
- **Muro de pago:** sin cuenta → `#/cuenta`; con cuenta y sin plan → `#/plan`. Si eligió plan en la página (`?plan=anual`), al crear la cuenta va **directo** al pago, sin volver a preguntar.
- **Landing:** promesa + simulador/calculadora (evento Lead) + dolor + funciones + confianza + planes en tarjetas separadas (el anual primero con "2 días gratis") + preguntas frecuentes + botón fijo en el celular. Los ejemplos son ficticios, nunca atribuidos al dueño.
- **Ganchos:** la landing lee `utm_content` (el nombre del anuncio) y muestra el mismo titular del anuncio que trajo a la persona.
- **Panel admin:** embudo en vivo (visita → calculadora → eligió plan → cuenta → compra), compras, bajas, pruebas gratis, costo de IA, opiniones.
- **Service worker:** sube la versión de caché (`<app>-vN`) en cada despliegue con cambios de front.
- **Despliegue:** `npx wrangler deploy` con el `CLOUDFLARE_API_TOKEN` del dueño (no el login OAuth de otra persona). Secretos con `wrangler secret put` leyendo desde archivos.

### Pruebas locales que siempre se hacen

- `wrangler dev` + `.dev.vars` (`MODO_LOCAL=1` devuelve el código de acceso en la respuesta, para entrar sin correo).
- Capturas con `scripts/capturas/cdp2.mjs`: inyectar `localStorage` **después** de cargar y recargar (si no, la app pisa lo inyectado).
- Si Chrome reusa el puerto 9333 con otra sesión: `pkill -f remote-debugging-port=9333`.
