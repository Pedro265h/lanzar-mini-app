# Caso real · Mamá Segura (14-15 de octubre de 2026)

App para embarazadas y mamás de recién nacidos en Latinoamérica, inspirada en el nicho del curso de Hotmart "Vive tu parto sin miedo" (sin usar su contenido). Tercera app del sistema, después de Escudriña (Biblia) y Mi Peludo (mascotas). Se hizo de cero a campaña en Meta en unos 2 días de trabajo.

## Producto

- **Funciones:**
  - "¿Esto es normal?" para embarazo, posparto y bebé, con alarmas fijas y fotos opcionales.
  - Semana a semana de la 4 a la 42.
  - Simulador del bebé con 11 imágenes realistas de las semanas clave, crossfade y tamaño que crece.
  - "Mis ecografías": sube la foto, la IA solo copia los datos escritos, y su bebé se ve en el simulador con un gráfico de crecimiento.
  - 14 clases, plan de parto, contador de contracciones (5-1-1), 12 guías del recién nacido y el chat "Pregúntale".
- **Dominio:** el dueño compró `mamaegura.app` (sin la "s"). Se le avisó una vez y decidió quedarse con ese.
- **Precio:** US$4,99 al mes · US$29,99 al año con 2 días gratis. Garantía de 7 días.

## Lo que más costó (y cómo se resolvió)

| Problema | Solución |
|---|---|
| Al empezar la prueba Meta iba a recibir una compra falsa de US$29,99 | Prueba = valor 0 o próximo cobro en menos de 5 días → StartTrial; la compra llega con el primer cobro real |
| Faltaba el webhook de la app en Hotmart: nadie se iba a activar | Se registró con OK (solo este producto, 16 eventos). La "prueba de configuración" no se envió, porque crea cuentas basura |
| El píxel del navegador no mandaba nada | La lista de dominios autorizados del píxel tenía solo dominios viejos; se agregó el de la app |
| Taiwán y Singapur bloquearon el geo "todo el mundo" | Se excluyeron |
| La página nueva no tenía Instagram y la API no podía crear la identidad de IG | Se montó solo en Facebook |
| La página se creó fuera del portafolio y con otro nombre ("Madre segura") | Se agregó al portafolio con OK y se le avisó para que la renombre |
| Fotos de IA con franjas pegadas arriba | Dejar de pedir "espacio vacío arriba" |
| Higgsfield 429 y "presets" recomendados | Reenviar en tandas; `declined_preset_id` |
| La voz local (Kokoro) no estaba instalada y HeyGen sin sesión | ElevenLabs por Higgsfield, una frase por escena |

## Resultado en Meta (todo en pausa)

- 1 campaña VLD (Mayor Volumen, compra), CBO $60 → hay que subirla a $90 con 9 anuncios.
- 6 anuncios de imagen (noche, fiebre, ecografía, las dos, calma, maleta) y 3 videos (urgencia "3 a. m.", oferta "2 días gratis", emocional "desde la primera semana"), cada uno en su conjunto.
- Solo mujeres 18-45, todo el mundo menos TW y SG, español, solo Facebook.

## Costos de IA aproximados

- Fotos: 2 créditos cada una (Nano Banana Pro 2k).
- Clips: 6,25 cada uno (Kling 3.0 std, 5 s).
- Voz: 0,3 por frase.
- Las 12 fotos de anuncios costaron unos 24 créditos; cada video, entre 8 y 31.
- Música: gratis (MusicGen local).

## Pendientes típicos al terminar

- Revisión profesional del contenido de salud.
- Que el dueño haga una prueba gratis real para confirmar el aviso de Hotmart.
- Conectar Instagram a la página.
- Ajustar el presupuesto al número de anuncios y activar.
