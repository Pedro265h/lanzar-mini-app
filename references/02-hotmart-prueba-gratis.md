# Fase 2 · Cobro con Hotmart (mensual + anual con días gratis)

## Lo que hace el usuario (tú le das los pasos)

1. Crear el producto como **suscripción** en Hotmart: mensual (p. ej. US$4,99) y anual (US$29,99) con **período de prueba de 2 días** en la oferta anual. Garantía de 7 días.
2. Pasarte los dos links de pago (`https://pay.hotmart.com/XXXX?off=yyyy`).

## Lo que haces tú

### Verificar las ofertas por la API (nunca confíes en el link pegado)

- OAuth: `POST https://api-sec-vlc.hotmart.com/security/oauth/token?grant_type=client_credentials&client_id=…&client_secret=…` con `Authorization: Basic <basic>` (si el archivo guarda el basic sin el prefijo, agrégale `Basic `).
- `GET https://developers.hotmart.com/products/api/v1/products` → el `ucode` del producto.
- `GET …/products/api/v1/products/{ucode}/offers` y `…/{ucode}/plans` → código de cada oferta, precio, `periodicity` (MONTHLY/ANNUAL) y `trial_period`.
- Ya pasó que un link pegado tenía una oferta que no existía ("Offer not found"); con la API se encontró la real.

### El link de pago desde la app

```ts
url.searchParams.set("email", u.email);
if (u.nombre) url.searchParams.set("name", u.nombre);
url.searchParams.set("sck", `u${u.id}x${await firma(env, u.id)}`); // HMAC con prefijo propio de la app
url.searchParams.set("checkoutMode", "10");
```

El `sck` firmado permite encontrar a la persona aunque pague con otro correo.

### El webhook (aviso 2.0)

- **Regístralo con OK del dueño** en Herramientas › Webhook: nombre de la app, URL `https://<dominio>/api/hotmart`, versión 2.0.0, **solo este producto**, eventos "Todos" (16). Hay que marcar la casilla de tratamiento de datos.
- **No envíes la "prueba de configuración":** manda compras ficticias que pueden crear cuentas basura en el panel. El hottok es el mismo de toda la cuenta y ya funciona en las otras apps.
- **El hottok es de toda la cuenta de Hotmart:** todas las apps de la misma cuenta reciben los avisos de todos los productos. Cada app **filtra por sus códigos de oferta** e ignora lo demás (ni activa ni reembolsa a otros).
- Verificación: cabecera `X-HOTMART-HOTTOK` comparada con `timingSafeEqual` sobre los hashes.

### La prueba gratis, bien tratada (lógica probada)

```ts
const proximo = Number(d?.purchase?.date_next_charge);
const proximoValido = Number.isFinite(proximo) && proximo > Date.now();
// Prueba: Hotmart aprueba sin cobrar; se reconoce por valor 0 o porque el próximo cobro es en pocos días.
const esPrueba = plan === "anual" && (Number(precio?.value) === 0 || (proximoValido && proximo - Date.now() < 5 * DIA));
if (tipo === "PURCHASE_COMPLETE") return ok; // llega al terminar la garantía: no da días ni cuenta como venta
if (esPrueba) {
  const finPrueba = proximoValido ? proximo : Date.now() + 2 * DIA;
  extenderPlan(u, plan, finPrueba + DIA);             // acceso hasta un día después del cobro
  marcarPrueba(u, finPrueba);                          // la app muestra "tus días gratis terminan el …"
  suscripcion("prueba");
  if (primeraVez(`prueba:${membresia}`)) {
    Meta StartTrial (valor 0) + correo "Tus días gratis empezaron" (3 cosas para hoy + fecha del cobro + cómo cancelar)
  }
} else {
  // cobro real: date_next_charge + 2 días
  if (venía de prueba) marcarPrueba(u, null);
  if (primeraVez(`compra:${membresia}`)) Meta Purchase con el valor real (y bienvenida solo si no venía de prueba)
}
```

- Meta **nunca** recibe una compra falsa de US$29,99 al empezar la prueba: recibe StartTrial, y la compra (Purchase) llega con el primer cobro, dentro de la ventana de 7 días.
- Reembolso, contracargo o disputa → corta el plan. Cancelación de suscripción → "no renueva", conserva hasta su fecha. Atrasada o vencida → "atrasada".
- **Supuesto a confirmar** con la primera prueba real (la hace el dueño con su tarjeta, no cobra): que Hotmart manda PURCHASE_APPROVED al empezar la prueba. Revisar en Hotmart › Webhook › Historial.

### Cancelar desde la app

`POST /api/cancelar` → `POST https://developers.hotmart.com/payments/api/v1/subscriptions/{subscriber_code}/cancel` con `{ send_mail: true }`. Conserva el acceso hasta su fecha. Si falla, el mensaje al usuario es humano ("cancélala en consumer.hotmart.com"), no técnico.

### Diseño del checkout (Checkout Builder)

`https://custom-checkout.hotmart.com/<productId>` → Crear una nueva página → plantilla **Saturn I**:
1. Celular: quitar el título de ejemplo, insertar una fila arriba del pago, poner `banner-movil-800x500`.
2. Computador: lo mismo con `banner-1200x400`; la fila del pago a 2 columnas y en la derecha `lateral-300x600`.
3. Guardar → Publicar → "Definir como estándar". El diálogo suele quedarse abierto: se publica desde la lista de páginas.
4. Verificar como compradora con user-agent de iPhone (si no, sale el diseño de computador).

Los banners no llevan precio (sirven para las dos ofertas): "Estás a un paso de…", 3-4 beneficios, "Acceso inmediato · pagas en tu moneda · garantía de 7 días". Foto del producto 600×600 solo con la marca.

### Textos cuando hay prueba gratis

En TODO lugar: "2 días gratis, después US$29,99 al año" (no "un solo pago"). Botón de la landing: "Empezar mis 2 días gratis". Al registrarse con el anual elegido: "Hoy no se te cobra: los primeros 2 días son gratis".
