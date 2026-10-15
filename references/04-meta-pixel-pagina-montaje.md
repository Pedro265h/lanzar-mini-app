# Fases 5 y 8 · Píxel y API de Meta, página y montaje

## 5a. Eventos (navegador + servidor con el mismo id)

| Evento | Cuándo | Por dónde |
|---|---|---|
| PageView | Carga de la landing | Navegador |
| Lead | Usó la calculadora o simulador de la landing (1 vez) | Navegador + servidor (mismo `event_id`) |
| CompleteRegistration | Creó su cuenta | Servidor (+ navegador con el id que devuelve) |
| InitiateCheckout | Fue al pago (valor del plan) | Servidor + navegador |
| StartTrial | Empezó los días gratis (valor 0) | Solo servidor (aviso de Hotmart) |
| Purchase | Primer cobro real de la suscripción | Solo servidor (aviso de Hotmart) |

- La API de conversiones manda correo, external_id, IP, user agent, fbp/fbc (guardados al ir al pago), nombre, teléfono y país del comprador, todo con hash. **Nunca datos de salud.**
- **Nunca mandes eventos de prueba con un `test_event_code` inventado**: Meta los procesa como reales. Solo con el código real de Administrador de eventos › Probar eventos.
- Sin píxel en Hotmart (lo manda el servidor). Si Hotmart tiene el píxel configurado, se quita para no contar doble.

## 5b. Verificación (la que de verdad sirve)

1. **Servidor:** `GET /{pixel}/stats?aggregation=event_source` con un token que vea el píxel → debe aparecer `SERVER`.
2. **Navegador:** `node scripts/capturas/revisar-pixel.mjs https://<dominio>/ 12000` → debe aparecer `META Image https://www.facebook.com/tr/ id=<pixel> ev=PageView`.
3. Si carga `fbevents.js` y la config pero **no sale `/tr`**: abre la consola (`cdp-consola`) y busca *"is unavailable on this website due to it's traffic permission settings"* → el píxel tiene **lista de dominios autorizados** sin tu dominio. Administrador de eventos › el píxel › Configuración › Permisos de tráfico › Editar › agregar el dominio (con OK). La caché tarda unos minutos y luego se re-verifica.
4. El bloqueador de anuncios del dueño esconde el píxel en su Chrome: no concluyas nada desde su navegador.
5. El píxel debe estar **compartido con la cuenta publicitaria** (`GET act_X/adspixels` lo lista).

## 5c. Página de Facebook

- Fotos: perfil 1080×1080 (solo el logo, se ve en círculo) y portada 1640×624 (texto dentro de la zona central de ~1110 px; en celular se recortan los lados). Se arman en HTML y se renderizan con `cdp2.mjs`.
- **Créala dentro del portafolio de la cuenta publicitaria**, o agrégala después: Configuración del negocio › Páginas › Agregar › "Agregar una página existente" › pegar la URL (con OK; se aceptan las condiciones comerciales). Si no, la API no la ve.
- **Verifica el nombre:** los anuncios salen a nombre de la página. Ya pasó que se creó "Madre segura" en vez de "Mamá Segura".
- **Instagram:** si la página no tiene cuenta de IG, el anuncio con ubicaciones de IG falla (sub 1772103), y una página recién creada no da token de página para crear la identidad de IG por API. Monta **solo Facebook** y agrega IG cuando conecten una cuenta.

## 8. Montaje (estructura que se usa en estas apps)

- **Una campaña VLD**, Mayor Volumen (`LOWEST_COST_WITHOUT_CAP`), `OUTCOME_SALES`, compra del píxel, atribución 7 días clic + 1 día vista.
- **Un conjunto por anuncio** (imagen o video) y **CBO = $10 × número de anuncios**. Si se agregan anuncios, sube el presupuesto o avisa.
- Nombre: `🟢VLD_<APP>_<Cuenta>_001_VOL_FRIO_VTA_7D_lp_<DDMmm>`; conjuntos `<PÚBLICO>_<EDAD>_<IDIOMA>_<GEO>_NN`; anuncios `adNN_<idea>`. Todo en español.
- **Segmentación de ejemplo (embarazo y recién nacido):** solo mujeres (`genders: [2]`, con **Advantage+ audience en 0**, si no, el género es solo sugerencia), 18-45, todo el mundo, idioma "Español (todos)" (`locales: [1002]`). Excluye **Taiwán y Singapur**, que exigen declarar categorías reguladas regionales (sub 3858498 / 3858550).
- Imagen: 4:5 en feeds y 9:16 en historias y reels con `asset_customization_rules`. Video: una sola pieza 9:16 + portada (`image_hash`).
- `degrees_of_freedom_spec.creative_features_spec` con OPT_OUT feature por feature (el campo `standard_enhancements` ya no existe).
- **Todo PAUSED.** Scripts: `scripts/meta/montar_imagenes.py meta.json` y `scripts/meta/montar_video.py`.
- Si la API responde "User request limit reached", espera unos minutos y revisa en el Administrador de anuncios (no consume ese límite).

## Evento para optimizar con prueba gratis

Por defecto, **Purchase** (es la venta real y llega dentro de los 7 días). Si al inicio hay muy pocas compras, la alternativa es optimizar por **StartTrial** (llega el mismo día, con más volumen pero de menor calidad). Propónlo como opción y deja que decida el dueño.
