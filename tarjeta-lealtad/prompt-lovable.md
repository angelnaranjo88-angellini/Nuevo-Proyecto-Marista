# Santa Nails — Generador de artes para las tarjetas de lealtad

## Contexto

Santa Nails es un estudio de uñas en México. Necesito una página web que
renderice **a tamaño real** las piezas impresas de mi programa de lealtad y las
deje listas para exportar a PDF y mandar a imprenta.

**Esto NO es una app con base de datos ni un sistema de sellos digitales.** Es un
generador de artes para impresión: las piezas se ven en pantalla exactamente
como se van a imprimir, y se exportan en su medida real.

## Entregable

Una sola ruta `/` con:

1. Una barra superior con: selector de pieza, toggle "Sangrado 3 mm", selector de
   color de acento (verde / rosa) y botón **Imprimir / Exportar PDF**.
2. El lienzo central mostrando la pieza seleccionada a tamaño real sobre un fondo
   gris neutro (`#EDEBE8`), con una sombra suave para que se lea como papel.
3. Las 4 piezas listadas abajo, cada una con sus medidas exactas.

Stack: React + Tailwind. Sin backend, sin auth, sin base de datos.

## Marca

- **Nombre:** Santa Nails
- **Logo:** voy a subir el archivo del logo (letras color crema sobre negro, con
  un ala de mariposa saliendo de la última "a"). Úsalo como asset y colócalo tal
  cual — **no lo redibujes ni lo reconstruyas con tipografía web.**
- **Motivo de marca:** hadas y mariposas. Voy a subir también un PNG de un hada
  (silueta oscura con alas de mariposa y destellos). Ese hada es el sello.

## Sistema de color

Define estos tokens en `index.css` bajo `:root` y usa **solo** estos colores en
toda la página y en las piezas. Son los mismos que voy a usar en mi app, así que
quiero el bloque limpio y reutilizable:

```css
:root {
  /* Base de marca */
  --sn-black:        #0B0B0B;   /* fondo del logo, tinta principal */
  --sn-cream:        #F5E9DA;   /* crema del logo */
  --sn-cream-soft:   #FBF4EA;   /* crema más claro, para superficies */

  /* Acentos */
  --sn-green:        #A8CEA2;   /* verde salvia */
  --sn-green-deep:   #6E9A6A;   /* verde para texto sobre crema */
  --sn-pink:         #F9A8B5;   /* rosa */
  --sn-pink-deep:    #C9707F;   /* rosa para texto sobre crema */

  /* Neutros de apoyo */
  --sn-ink-soft:     #4A4640;   /* texto secundario sobre crema */
  --sn-muted:        #8A857F;   /* etiquetas, letra chica */
  --sn-rule:         #DDD6CF;   /* líneas divisorias y renglones */
}
```

Reglas de uso:

- **Negro + crema es la base.** Verde y rosa son acentos, nunca fondos grandes de
  texto largo.
- Sobre crema, el texto de color usa `--sn-green-deep` / `--sn-pink-deep`, nunca
  los tonos claros: `#A8CEA2` sobre crema no alcanza contraste legible.
- Nada de degradados. Nada de sombras de colores. Bloques de color plano.

## Tipografía

Dos fuentes de Google Fonts, nada más:

- **Display / títulos:** `Prata` — serif de alto contraste, es lo más cercano al
  logo. Fallback: `Georgia, serif`.
- **Texto, etiquetas y letra chica:** `Jost` — geométrica, elegante. Fallback:
  `"Helvetica Neue", Arial, sans-serif`.

Las etiquetas chicas van en MAYÚSCULAS con `letter-spacing: 0.18em`.

## Las 4 piezas

| # | Pieza | Medida | Fondo |
|---|---|---|---|
| 1 | Tarjeta — frente | 85 × 55 mm | negro `--sn-black` |
| 2 | Tarjeta — reverso | 85 × 55 mm | crema `--sn-cream-soft` |
| 3 | Invitación de referido | 85 × 55 mm | rosa `--sn-pink` |
| 4 | Hoja de mostrador | A5, 148 × 210 mm | crema `--sn-cream-soft` |

**Trabaja todo en milímetros reales** (`width: 85mm; height: 55mm`), no en px.
Los tamaños de letra en `pt`. Así lo que se ve en pantalla es lo que sale impreso.

---

### Pieza 1 — Tarjeta, FRENTE (85 × 55 mm, fondo negro)

Márgenes internos de 5 mm. Marco decorativo: línea de 0.3 mm en
`--sn-green` al 40% de opacidad, a 2.5 mm del borde, esquinas de 1 mm.

De arriba a abajo:

1. **El logo de Santa Nails** (el asset que subo), alineado a la izquierda,
   ancho aproximado 32 mm.
2. Etiqueta: `ESTUDIO DE UÑAS · TARJETA DE LEALTAD` — Jost, 5 pt, mayúsculas,
   tracking 0.18em, color `--sn-green`.
3. **Los 5 sellos.** Fila de 5 círculos iguales, `gap` parejo, cada uno de
   13 mm de diámetro:
   - Relleno `--sn-cream`, sin borde.
   - Dentro de cada círculo, **el hada al 14% de opacidad**, centrada, ocupando
     ~70% del círculo. Es una marca de agua: el sello físico se estampa encima.
   - Un número chiquito (1 a 5) en Prata 7 pt, color `--sn-pink-deep`, pegado
     abajo del círculo, centrado.
4. **Banda del premio.** Rectángulo de ancho completo, 7 mm de alto, fondo
   `--sn-green`, esquinas 1 mm. Adentro, en una fila con `justify-content: space-between`:
   - Izquierda: un destello de 4 puntas (SVG) + `6ª VISITA · 20% DE DESCUENTO`
     en Jost 6 pt, mayúsculas, tracking 0.13em, color `--sn-black`.
   - Derecha: `TOPE $150` en Jost 5 pt, color `--sn-black` al 70%.
5. **Renglones para escribir**, hasta abajo, en Jost 5 pt mayúsculas color
   `--sn-cream` al 55%, con línea de 0.25 mm en `--sn-cream` al 30%:
   `NOMBRE ______   TEL ______   1ER SELLO ______`

---

### Pieza 2 — Tarjeta, REVERSO (85 × 55 mm, fondo crema)

Márgenes internos de 5 mm. Todo el texto en `--sn-ink-soft` salvo lo indicado.

**CÓMO FUNCIONA** (Jost 5 pt, mayúsculas, tracking 0.18em, `--sn-pink-deep`),
y debajo tres puntos numerados. El número va en un círculo de 3 mm relleno
`--sn-black` con la cifra en crema, 4.5 pt:

1. Un sello por cita, con consumo mínimo de **$400**.
2. Sello extra si traes una clienta nueva y ella toma su primer servicio completo (máximo 2 por tarjeta).
3. Con 5 sellos, tu 6ª cita lleva **20% de descuento**.

**CONDICIONES** (mismo estilo de encabezado), y debajo este párrafo corrido en
Jost 4.5 pt, `line-height: 1.5`, color `--sn-muted`. Cópialo **textual**:

> Vigencia de 8 meses desde el primer sello · El beneficio se usa dentro de los 60 días posteriores al 5º sello · Consumo mínimo para canjear $500 · Descuento máximo $150 · Un sello por cita y por persona · Se requieren mínimo 4 visitas pagadas · No acumula en retiros, reparaciones, servicios gratuitos, anticipos, cancelaciones ni citas no asistidas · La visita de canje no acumula sello · No aplica en diciembre, 10 de mayo ni 14 de febrero · No se combina con otras promociones ni es canjeable por efectivo · Personal e intransferible · Los sellos son válidos únicamente con el sello oficial del estudio.

Hasta abajo, separado por una línea de 0.25 mm en `--sn-rule`: a la izquierda
`@SANTANAILS · [TELÉFONO]` y a la derecha `TARJETA Nº ______`, ambos en Jost
5 pt mayúsculas color `--sn-muted`.

---

### Pieza 3 — Invitación de referido (85 × 55 mm, fondo rosa)

Esta es la tarjeta que mi clienta le da a una amiga. Texto en `--sn-black`.

1. El logo de Santa Nails arriba a la izquierda, ~26 mm de ancho. Si el logo que
   subo viene en crema, úsalo en negro aquí (o aplica `filter` para invertirlo);
   sobre rosa el crema no contrasta.
2. Etiqueta `ESTUDIO DE UÑAS · INVITACIÓN` en Jost 5 pt mayúsculas tracking 0.18em.
3. El hada, en negro al 100%, del lado derecho, de unos 22 mm de alto, saliéndose
   ligeramente del borde derecho (recortada por `overflow: hidden`).
4. **`$50`** en Prata 26 pt, y a un lado, en dos renglones, Prata 8 pt:
   `de descuento` / `en tu primera cita`.
5. `EN SERVICIOS DESDE $400` en Jost 5.5 pt mayúsculas tracking 0.13em.
6. Renglón `TE INVITA ______________` en Jost 5 pt mayúsculas, línea de 0.25 mm.
7. Letra chica en Jost 4.5 pt, `line-height: 1.5`, negro al 60%, textual:

> Válida 60 días desde su entrega · Únicamente en la primera visita · No se combina con otras promociones ni es canjeable por efectivo · Presenta esta tarjeta al agendar.

---

### Pieza 4 — Hoja de mostrador (A5, 148 × 210 mm, fondo crema)

Es la hoja que vive junto a la caja, para que quien atienda sepa cuándo sellar.
Márgenes de 12 mm. Cuerpo de texto en 9 pt (aquí sí se puede leer cómodo).

Encabezado: `SANTA NAILS · PROGRAMA DE LEALTAD` en Jost 7 pt mayúsculas
`--sn-pink-deep`, y debajo **Reglas de mostrador** en Prata 20 pt `--sn-black`.
A la derecha, el hada en negro, 18 mm de alto. Línea divisoria abajo.

Luego, en dos columnas:

**SÍ DAS UN SELLO** (viñeta: palomita en `--sn-green-deep`)
- Servicio de $400 o más, pagado y terminado.
- Una cita, una persona, un sello. Anota la fecha dentro del círculo.
- Referido: cuando su invitada ya pagó su primer servicio completo.

**NO DAS UN SELLO** (viñeta: tache en `--sn-pink-deep`)
- Retiros, reparaciones y servicios de cortesía.
- Anticipos, depósitos y servicios menores a $400.
- Cancelaciones y citas no asistidas.
- La visita en la que se canjea el descuento.

Otra fila de dos columnas:

**REFERIDOS**
- Dale la tarjeta rosa de $50 a la clienta que invita.
- La invitada la presenta al agendar; aplica desde $400.
- Máximo 2 sellos por referido en cada tarjeta.

**CANJE DE LA 6ª VISITA**
- 5 sellos y mínimo 4 visitas pagadas.
- Consumo mínimo $500. Descuento 20%, tope $150.
- Dentro de los 60 días del 5º sello.

Recuadro destacado, fondo `--sn-green` al 25%, esquinas 1.5 mm:

**REGISTRO PARALELO · OBLIGATORIO**
Anota en la libreta el nombre, el teléfono, la fecha del primer sello y el número
de sellos de cada clienta. Sin ese registro no se repone una tarjeta perdida — y
ese teléfono es lo que te deja recuperar a una clienta que dejó de venir.

Al final, **TÉRMINOS COMPLETOS** en dos columnas, Jost 7 pt, color `--sn-muted`:

> Vigencia de 8 meses desde el primer sello. El beneficio debe utilizarse dentro de los 60 días posteriores al quinto sello. Consumo mínimo para canjear: $500 MXN. Descuento del 20% con tope máximo de $150 MXN. Un sello por cita y por persona, en servicios desde $400 MXN. Se requieren mínimo 4 visitas pagadas. No aplica en retiros, reparaciones, servicios gratuitos, anticipos, cancelaciones ni citas no asistidas. La visita de canje no acumula sello. No aplica en diciembre, 10 de mayo ni 14 de febrero. La recompensa no se combina con otras promociones ni es canjeable por efectivo. La tarjeta es personal e intransferible. Los sellos son válidos únicamente con el sello o firma oficial del estudio. La clienta referida recibe $50 de descuento en su primera visita, en servicios desde $400 MXN, válido 60 días desde la entrega de la invitación.

---

## Impresión

Esta parte es la que más importa: si sale mal, la imprenta me rebota el archivo.

- Cada pieza debe imprimirse **en su tamaño real**, sin que el navegador la
  escale. Antes de llamar `window.print()`, inyecta dinámicamente una regla
  `@page { size: <ancho>mm <alto>mm; margin: 0; }` con las medidas de la pieza
  seleccionada, y quítala al terminar.
- En `@media print`: oculta la barra de herramientas y el fondo gris; deja
  visible **solo** la pieza seleccionada, sin sombra y sin bordes redondeados
  del contenedor.
- Fuerza `-webkit-print-color-adjust: exact; print-color-adjust: exact;` en las
  piezas, o los fondos negro y rosa salen en blanco.
- **Toggle de sangrado:** cuando esté activo, cada pieza se renderiza 3 mm más
  grande por cada lado (la tarjeta pasa a 91 × 61 mm), con el color de fondo
  extendido hasta el borde nuevo y **marcas de corte** — líneas de 0.25 mm en
  negro, de 3 mm de largo, en las cuatro esquinas, separadas 1 mm del área de
  corte. El contenido no se mueve: sigue centrado en los 85 × 55 mm de adentro.

## Qué NO quiero

- No inventes texto. Todo el copy está arriba; úsalo textual, incluidos los
  puntos medios `·` y los montos.
- No agregues secciones, íconos decorativos, ilustraciones ni "detalles bonitos"
  que no pedí.
- Nada de degradados, glassmorphism, sombras de colores ni bordes redondeados
  grandes. Los radios máximos son de 1.5 mm.
- No uses emoji en ninguna pieza.
- No cambies los colores ni los "mejores". Los hex de arriba son los definitivos.
- No metas base de datos, login, ni estado de sellos. Las piezas son estáticas.
- No redibujes el logo con tipografía web: usa el archivo que subo.

## Primer mensaje sugerido para Lovable

Pega todo lo de arriba, y súbele en el mismo mensaje:
1. El logo de Santa Nails (PNG o SVG con fondo transparente).
2. El PNG del hada (silueta, fondo transparente).

Si el hada no viene con fondo transparente, pídele a Lovable que la recorte o
que la aplique con `mix-blend-mode: multiply` dentro de los círculos crema.
