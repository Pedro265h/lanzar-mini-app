# Fase 6 · Anuncios de imagen realistas

## Método

1. **Fotos sin texto con IA** (Higgsfield `nano_banana_pro`, resolución 2k, 2 créditos cada una): una por idea y formato (4:5 y 9:16). El texto NO lo pone la IA: lo pone el HTML encima, así sale perfecto.
2. **Composición en HTML** con `scripts/anuncios/armar_anuncios.py`: foto de fondo + velo (oscuro de noche, crema de día) + titular en la tipografía de la marca + **una tarjeta igual a la de la app** (semáforo verde o rojo, "Semana 24 · del tamaño de…", contador de contracciones o etiquetas) + marca + botón "Pruébala 2 días gratis" + "Te orienta, no reemplaza a tu médico".
3. **Render exacto:** `ANCHO=1080 ALTO=1350 node scripts/capturas/cdp2.mjs pasos-45.json png` (y 1080×1920). Exporta a JPG (calidad 92) para Meta.
4. **Revisa con una hoja de contacto** (PIL) antes de entregar: caras tapadas, tarjetas sobre la barriga, logos pisados.

## Prompts que funcionan (fotos)

- "Candid photorealistic vertical photo, shot on iPhone…, Latin American woman around 28…, real skin texture, no makeup, authentic documentary style, shallow depth of field… No text, no logos, no watermark."
- Describe el **momento** (la emoción y lo que hace) y la luz: lámpara de noche cálida, ventana de mañana.
- **No pidas "el tercio de arriba vacío para el texto":** el modelo pega una franja de pared falsa con una costura visible. Pide una foto continua ("One continuous single photograph, natural composition") y resuelve el texto con el velo y la posición del encuadre.
- Si una foto sale rara (un test pegado a la camiseta, un corte), rehazla: son 2 créditos.
- Para el 4:5 se puede recortar la 9:16 con `object-position` (cuidando que las caras queden por debajo del titular).
- Límite de Higgsfield: unas 9 generaciones a la vez; el resto da error 429 y se reenvía cuando terminen.
- Las referencias de imagen con fetos las bloquea su filtro: genera solo con texto.

## 6 ideas que cubren a los dos públicos (ejemplo de embarazo y recién nacido)

| # | Público | Titular | Tarjeta |
|---|---|---|---|
| 1 | Embarazo | ¿Es normal o voy a urgencias? | Verde: "Acidez y ardor en la semana 32" |
| 2 | Recién nacido | 3 a. m. Llora y lo sientes caliente. | Rojo: "Fiebre de 38 °C en un bebé de 3 semanas" |
| 3 | Embarazo | Mira cómo crece tu bebé, semana a semana. | Imagen real del simulador "Semana 24" |
| 4 | Ambas | Del embarazo a sus primeros meses, sin miedo. | Etiquetas de funciones |
| 5 | Recién nacido | Esa tranquilidad de saber qué es normal. | Verde: "Hipo después de mamar" |
| 6 | Final del embarazo | ¿Cómo sé que ya es el momento? | Contador 5-1-1 |

Las tarjetas deben ser **coherentes con las reglas de la app**. Por ejemplo, las contracciones antes de la semana 37 dan amarillo, no verde: no muestres un verde que la app no daría.

## Textos para Meta

- Texto principal, título y descripción por anuncio, en un `textos-para-meta.txt` (lo lee el script de montaje).
- **Sin afirmar atributos personales:** nada de "tu embarazo" ni "¿estás embarazada?" en el texto; habla de la situación ("el bebé llora y lo sientes caliente").
- Cierre igual en todos: "Pruébala 2 días gratis. Si no es para ti, cancelas desde la app."
