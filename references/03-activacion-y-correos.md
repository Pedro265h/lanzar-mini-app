# Fases 3 y 4 · Activación en la prueba y correos

## 3. "Tu camino": que la prueba de 2 días enganche

La prueba gratis decide si paga. La meta: que en 48 horas sienta que la app ya acompaña SU proceso.

- **Tarjeta "Tu camino" en Hoy:** 5 pasos armados con SU etapa, numerados y con barra de avance ("2 de 5"). El encabezado dice "Día 1 de tus 2 días gratis" mientras dura la prueba.
  - **Día 1:** conocer al bebé en su semana (o lo de la edad de su bebé o mascota), revisar un síntoma en el semáforo y subir su ecografía o foto.
  - **Día 2 ("Mañana, o ya si quieres"):** la clase que le toca según la etapa, y el plan (de parto) o las señales de urgencia si va muy al inicio.
  - Cada paso lleva a la pantalla exacta. Se marca hecho por lo que la persona hace de verdad, por ejemplo cuando ya hay una consulta o una ecografía.
  - Un aviso al completar cada paso ("Vas 3 de 5. Sigue así"), y una celebración el día que termina el camino.
  - Se ve los primeros 7 días o mientras dure la prueba. Se guarda en la copia de la cuenta, así sirve en otro celular.
- **Personalización:** apodo del bebé (o nombre de la mascota) en la etapa → "Así está Frijolito hoy", "Faltan 109 días para conocer a Frijolito".
- **"Lo que viene":** una tarjeta con la próxima semana ("En 3 días: semana 25, va a medir como…"). Hace volver.
- **Honestidad que vende:** en Hoy y en Cuenta, "Tus días gratis terminan el 17 de octubre. Después sigue tu plan anual (US$29,99 por todo el año)". El enlace "Cancelar la renovación" lleva a una pantalla "Antes de irte" que muestra lo que ya armó (su semana, sus consultas, sus ecografías) con "Seguir" como botón principal y "Sí, cancelar" como secundario. Cancelar es un toque.
- **Correo de bienvenida de la prueba:** "Tus días gratis empezaron", 3 cosas para hacer hoy, la fecha del cobro y cómo cancelar.

## 4. Secuencia de correos para quien se registra y no compra

### Infraestructura

- **Dominio propio en Email Sending** (no el subdominio compartido de otras marcas): Cloudflare › Envío de email › Incorporar dominio. Agrega registros en `cf-bounce.<dominio>` y DKIM; no toca la app. El token de API del dueño no tiene ese permiso, así que se hace desde el dashboard (con OK).
- **Remitente:** `hola@<dominio>` (`CORREO_SECUENCIA`). La bienvenida también sale de ahí.
- **Respuestas:** Email Routing en el mismo dominio (MX, SPF, DKIM, DMARC) + regla `hola@<dominio>` → Gmail del dueño. Es una regla de reenvío: **con OK explícito**. Destino ya verificado en la cuenta.
- **Motor:** una fila por persona en el Durable Object (paso, próximo envío, token de baja). La alarma del DO envía lo que toca y se reprograma. Horario 8:00-21:00 (hora del país base). Se corta sola al comprar o empezar la prueba, al darse de baja, si es admin o si la cuenta está bloqueada. Si no hay remitente, reintenta cada hora sin perder el correo.
- **Baja:** link en el pie + cabeceras `List-Unsubscribe` y `List-Unsubscribe-Post` (baja con un clic en Gmail).

### Contenido (7 correos en 10 días: 1 h, 24 h, 48 h, 72 h, 5 d, 7 d, 10 d)

1. **"{Nombre}, tus 2 días gratis te esperan"**: hoy no pagas nada, qué vive en los 2 días y que cancela desde la app.
2-5. Valor real del nicho: las señales que nunca debes esperar, el semáforo ("¿Es normal o voy a urgencias?"), cómo saber que empezó el parto y el plan de parto en 10 minutos. Cada uno cierra con la prueba gratis.
6. **Preguntas frecuentes:** "¿Cómo funcionan los 2 días gratis?", "¿Me van a cobrar sin avisarme?", "¿Reemplaza a mi médico?", garantía y cómo pagar.
7. **"¿Lo dejamos aquí?"**: último correo, sin presión barata.

- **Todos los botones** van a `/app/#/cuenta?plan=anual`: con la sesión abierta salta **directo** al pago del anual con los días gratis.
- **Personalización con sus datos** (marcador `[semana]` en el texto): "Vas en la semana 24: Frijolito ya mide como una mazorca de maíz (unos 30 cm y 600 g). Faltan 109 días para conocer a Frijolito". Para eso, la calculadora de la landing **guarda la fecha en el localStorage de la app** y se sube al crear la cuenta.
- **Mamá con el bebé ya nacido:** se saltan los correos que solo sirven en el embarazo (`soloEmbarazo`).
- **Vista previa en el panel:** `/api/admin/correo?paso=1..7` con una persona de ejemplo (`?sin=1` sin sus datos).
- **Prueba local:** acción admin `correo_ahora` para forzar el siguiente; los correos quedan en `.wrangler/tmp/email/` (texto y HTML). Revisa que salgan los 7 en orden y el salto de los del embarazo.
