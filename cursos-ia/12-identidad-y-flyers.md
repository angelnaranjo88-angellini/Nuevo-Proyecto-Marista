# 12 · Identidad Chaos Ctrl y prompts para flyers

## Parte 1 · Tu identidad, como está en el manual

### Paleta oficial

| Rol sugerido | Hex | Uso |
|---|---|---|
| **Fondo dominante** | `#050A34` | Azul marino casi negro. El 60–70% de cada pieza |
| **Fondo secundario / bloques** | `#092676` | Azul profundo. Tarjetas, sombra del logo, bloques |
| **Acento y llamadas a la acción** | `#085CF0` | Azul eléctrico. Botones, badge de asesoría, precio |
| **Destaque claro** | `#AFE9FD` | Celeste. Datos, subrayados, detalles sobre fondo oscuro |
| **Texto y superficies claras** | `#E8E6D8` | Crema. Titulares sobre oscuro, fondos claros |

**Es una paleta 100% fría.** Eso te da elegancia y coherencia, pero te quita el color de urgencia que suele usarse para precios y cupos. La solución dentro de tu propia paleta: **el azul eléctrico `#085CF0` es tu color de acción** y el **celeste `#AFE9FD` tu color de dato**. Reserva el eléctrico para el botón, el precio y el badge de asesoría — nada más. Si lo usas en todo, deja de funcionar.

### Tipografía

| Rol | Fuente | Dónde |
|---|---|---|
| Titulares | **Horizon** | Mayúsculas, apretadas. Es la del logo secundario |
| Etiquetas, datos, temario | **Lekton** | Mono. Hace que los datos se lean como datos |
| Cuerpo | **Coolvetica** | Párrafos y textos de apoyo |

Las tres van en Canva (súbelas si no están). En el plan visual usé **Lekton** —que sí está en Google Fonts— y sustitutos cercanos para las otras dos.

### Los activos que ya tienes

- **Logo principal:** la tecla de teclado crema con "CHAOS / Ctrl" sobre el cuadro negro redondeado. Es el que va en los flyers, arriba a la izquierda, pequeño.
- **Logo secundario:** "CHAOS CTRL" en Horizon con la sombra azul desplazada. Para portadas y piezas donde la marca es el protagonista.
- **Iconos dibujados a mano** (la tecla CTRL en perspectiva, la C entre garabatos, la espiral). **Estos son tu mejor activo y están desaprovechados:** la C rodeada de garabatos es literalmente "el caos", y la tecla Ctrl es "el control". Úsalos como elemento gráfico suelto en los flyers, en celeste `#AFE9FD` sobre el azul marino.

### Un detalle que hay que corregir hoy

Tu manual trae el tagline **"GOOD VIBES / GREAT BREWS"** — eso viene de la plantilla original, que era de una cafetería. Cámbialo antes de que se te cuele en una pieza publicada. Opciones que sí dicen lo que haces:

- **DEL CAOS AL CONTROL**
- **IA APLICADA, EN VIVO**
- **CONTROL + IA**

La primera es la más fuerte: está en el nombre, es memorable, y es literalmente el antes y después de tu cliente.

---

## Parte 2 · Cómo vas a producir los flyers

Vas a generarlos en ChatGPT. Dos cosas que hay que saber antes:

**1. Los logos de las apps van a salir mal.** ChatGPT no reproduce fielmente los logos de ChatGPT, Gemini, Claude o Copilot: los deforma, les inventa formas o les pone letras raras. Los prompts de abajo los piden de todas formas porque a veces salen aceptables — pero **si salen deformes, la corrección son dos minutos en Canva**: descarga los iconos reales y pégalos encima de los cuadros que generó. Quedan perfectos y es más rápido que regenerar diez veces.

**2. El texto en español a veces se rompe.** Los acentos y la ñ. Revisa siempre antes de publicar: "asesoría", "más", "días", "diseño". Si una palabra salió mal, regenera o corrígela en Canva.

**El flujo más rápido y confiable:**

```
ChatGPT genera la composición completa
        ↓
¿Salieron bien logos y acentos?
        ↓                    ↓
       SÍ                   NO
        ↓                    ↓
   Publícalo         Canva: pega los iconos
                     reales y corrige el texto
                             ↓
                        Publícalo
```

---

## Parte 3 · Los prompts

Cópialos tal cual. Lo que está `[entre corchetes]` es lo que tú cambias antes de pegarlo.

### 3.1 · Ctrl + Inicio — flyer principal (formato 4:5, feed)

```
Create a vertical 4:5 social media flyer for a live AI course. Dark,
premium, editorial tech design. NOT a generic template.

BACKGROUND: deep navy #050A34, almost black. Very subtle texture: thin
hand-drawn scribble lines in light blue #AFE9FD at 12% opacity in the
upper right corner, like tangled chaos resolving into a clean grid
toward the bottom. Keep it faint — it is texture, not decoration.

LAYOUT, top to bottom:

1. Top left, small: a cream #E8E6D8 rounded-square keyboard-key logo
   containing the words "CHAOS" above a thin line and "Ctrl" below.
   Small, about 10% of the width.

2. Headline, huge, cream #E8E6D8, uppercase, heavy squarish techno
   sans-serif, very tight letter spacing, three lines, left aligned:
   "DOMINA
   CHATGPT
   DE VERDAD"

3. Below it, one line in light blue #AFE9FD, small, monospaced:
   "No el 10% que usa todo el mundo"

4. A horizontal row of 5 evenly spaced rounded-square app icons on a
   subtle #092676 strip: ChatGPT, Google Gemini, Claude, Microsoft
   Copilot and Grok. Flat, simple, correctly proportioned, evenly sized.

5. A short list of 4 items, cream text, monospaced, each preceded by a
   small electric blue #085CF0 arrow:
   "Modelos de razonamiento
   Proyectos, archivos y conectores
   Imagenes, video y presentaciones
   Prompts que si funcionan"

6. A BOLD BADGE that must be the second most visible element on the
   whole flyer: a solid electric blue #085CF0 rectangle with slightly
   rounded corners, spanning most of the width, containing in dark navy
   #050A34 heavy uppercase text:
   "+ 1 MES DE ASESORIA INCLUIDO"
   and under it in smaller text:
   "Cuando acaba el curso, sigo contigo"

7. Bottom block: on the left, in monospaced cream, three short lines:
   "5 sesiones · 10 horas en vivo"
   "Grupos de 10 personas maximo"
   "Lunes a viernes 7 a 9 pm"
   On the right, very large in electric blue #085CF0: "$1,290"

8. Bottom edge: a full-width cream #E8E6D8 button with dark navy text:
   "ESCRIBEME POR WHATSAPP"

STYLE: high contrast, generous margins, strong typographic hierarchy,
only three text sizes, lots of breathing room. Premium and confident,
like a design studio poster — not a busy sales flyer. Only these four
colors: #050A34, #092676, #085CF0, #AFE9FD, #E8E6D8. All text in
Spanish, spelled exactly as written above.
```

> **Nota sobre acentos:** el prompt escribe "ASESORIA", "Imagenes", "si" sin
> acento **a propósito** — los generadores fallan más con acentos y es mejor
> ponerlos tú en Canva que arriesgar una palabra rota. Si tu generación sale
> bien con acentos, mejor.

### 3.2 · Ctrl + Aula — docentes (4:5)

```
Create a vertical 4:5 social media flyer for a live AI course for
teachers. Dark, premium, editorial tech design.

BACKGROUND: deep navy #050A34. Faint texture in the upper area: thin
hand-drawn line art in light blue #AFE9FD at 10% opacity suggesting
stacked notebooks and scattered papers becoming an ordered grid.

LAYOUT, top to bottom:

1. Top left, small: cream #E8E6D8 rounded-square keyboard-key logo with
   "CHAOS" above a thin line and "Ctrl" below.

2. Huge headline, cream #E8E6D8, uppercase, heavy squarish techno
   sans-serif, tight letter spacing, left aligned, three lines:
   "RECUPERA
   TUS
   TARDES"

3. One line in light blue #AFE9FD, monospaced, small:
   "Para maestros que se ahogan en planeaciones"

4. Horizontal row of 4 rounded-square app icons on a #092676 strip:
   ChatGPT, Google Gemini, Claude and Canva. Flat, simple, even.

5. Four list items in cream monospaced text with small electric blue
   #085CF0 arrows:
   "Planeaciones alineadas a tu programa
   Rubricas y examenes en minutos
   Retroalimentacion para 40 alumnos
   Que hacer cuando ellos usan IA"

6. BOLD BADGE, solid electric blue #085CF0 block, dark navy heavy
   uppercase text, one of the two most visible elements:
   "+ 1 MES DE ASESORIA INCLUIDO"
   smaller line under it:
   "Te acompaño hasta que lo apliques en tu grupo"

7. Bottom block, left in monospaced cream:
   "4 sesiones · 8 horas en vivo"
   "Sabados por la manana"
   "Constancia con horas"
   Right, very large in electric blue: "$1,490"

8. Full-width cream button, dark navy text:
   "3 COLEGAS PAGAN 2 · ESCRIBEME"

STYLE: high contrast, generous margins, only three text sizes, calm and
premium, not a busy sales flyer. Only these colors: #050A34, #092676,
#085CF0, #AFE9FD, #E8E6D8. All text in Spanish, exactly as written.
```

### 3.3 · Ctrl + Negocio — emprendedores (4:5)

```
Create a vertical 4:5 social media flyer for a live AI course for small
business owners. Dark, premium, editorial tech design.

BACKGROUND: deep navy #050A34. Faint texture: thin light blue #AFE9FD
line art at 10% opacity showing a tangle of arrows on the left resolving
into a clean automation flow diagram on the right.

LAYOUT, top to bottom:

1. Top left, small: cream #E8E6D8 rounded-square keyboard-key logo with
   "CHAOS" above a thin line and "Ctrl" below.

2. Huge headline, cream #E8E6D8, uppercase, heavy squarish techno
   sans-serif, tight, left aligned, three lines:
   "QUE TU
   NEGOCIO
   TRABAJE SOLO"

3. One line in light blue #AFE9FD, monospaced, small:
   "Sales de clase con una automatizacion corriendo"

4. Horizontal row of 4 rounded-square app icons on a #092676 strip:
   ChatGPT, Claude, WhatsApp and Make (automation). Flat, simple, even.

5. Four list items in cream monospaced text with electric blue #085CF0
   arrows:
   "Un asistente entrenado con tu negocio
   Mensajes que se clasifican y contestan solos
   Cotizaciones automaticas
   Tus ventas analizadas cada lunes"

6. BOLD BADGE, solid electric blue #085CF0 block, dark navy heavy
   uppercase text:
   "+ 1 MES DE ASESORIA INCLUIDO"
   smaller line under it:
   "Hasta que este funcionando de verdad"

7. Bottom block, left in monospaced cream:
   "4 sesiones · 8 horas en vivo"
   "Solo 8 lugares"
   "Trabajamos negocio por negocio"
   Right, very large in electric blue: "$1,500"

8. Full-width cream button, dark navy text:
   "ESCRIBEME POR WHATSAPP"

STYLE: high contrast, generous margins, only three text sizes, premium
and confident. Only these colors: #050A34, #092676, #085CF0, #AFE9FD,
#E8E6D8. All text in Spanish, exactly as written.
```

### 3.4 · Versión historia / Reel (9:16)

Toma cualquiera de los tres de arriba y **cambia solo la primera línea** por:

```
Create a vertical 9:16 story format flyer, same design system.
```

Y añade al final:

```
IMPORTANT for 9:16: keep the top 15% and bottom 20% of the canvas free
of text and logos, because the platform interface covers those areas.
Center the headline and the badge in the middle 60% of the frame.
```

Ese último párrafo es el que evita que Instagram te tape el precio con la
barra de "Enviar mensaje".

### 3.5 · Fondo sin texto — la opción segura

Cuando quieras armar el flyer tú en Canva con texto y logos perfectos:

```
Abstract brand background for a technology education company. Deep navy
#050A34 base. Thin hand-drawn scribble lines in light blue #AFE9FD:
tangled and chaotic in the upper left, gradually resolving into a clean,
precise geometric grid toward the lower right. A few small solid shapes
in electric blue #085CF0 as accents along the transition. Subtle grain,
high contrast, deep blacks, calm and premium.

Absolutely no text, no letters, no numbers, no logos, no watermarks,
no icons.

[Vertical composition, 4:5 aspect ratio]. Keep the entire lower two
thirds visually calm and mostly empty, ready for typography.
```

Este es el que va a salir bien **siempre**, porque no le estás pidiendo texto ni logos. Genera tres o cuatro versiones y guárdalas: te sirven para todo el contenido del mes.

### 3.6 · Solo la fila de iconos

Si prefieres armar el flyer en Canva pero quieres la tira de apps generada:

```
A horizontal row of 5 evenly spaced rounded-square app icons on a solid
deep blue #092676 background strip. The icons are: ChatGPT, Google
Gemini, Claude, Microsoft Copilot and Grok. Flat, simple, clean, all
exactly the same size, evenly spaced, generous padding around the row.
No text, no labels, no shadows. Wide horizontal composition.
```

**Pero honestamente: para esto Canva es mejor.** Busca "ChatGPT logo", "Gemini logo", "Claude logo" en su buscador de elementos, o descarga los iconos oficiales. Quedan perfectos y tardas menos.

---

## Parte 4 · Por qué estos flyers funcionan

Tres decisiones deliberadas, por si quieres cambiarlas con criterio:

**La fila de apps va arriba, junto al titular.** Es tu mejor detenedor de scroll: la gente reconoce esos iconos en un cuarto de segundo y entiende de qué se trata antes de leer una sola palabra. Ponerla abajo desperdicia ese efecto.

**El badge de asesoría es el segundo elemento más visible, no el tercero ni el cuarto.** Es tu único diferenciador que nadie más ofrece. Si compite en tamaño con el temario, se pierde. Por eso va en un bloque sólido de azul eléctrico, con el fondo invertido — es lo único en toda la pieza con ese tratamiento.

**Solo cuatro puntos de temario, no diez.** La tentación es meter todo lo que enseñas para demostrar valor. No funciona: un flyer con diez bullets no se lee, se ignora. Cuatro puntos específicos —"proyectos, archivos y conectores"— comunican más profundidad que diez genéricos, porque el que sabe un poco reconoce inmediatamente que ahí hay algo que no le han enseñado.

## Parte 5 · Qué probar primero

Tres versiones por curso, y déjalas correr 3 días antes de juzgar:

| Versión | Qué es | Qué mides |
|---|---|---|
| **A** | El flyer de la sección 3 | Si el mensaje y el temario funcionan solos |
| **B** | Fondo 3.5 + tu foto real + el titular | Si tu cara sobre la marca convierte |
| **C** | Video vertical tuyo hablando 30 s, sin música ni edición | Tu cara sola contra todo lo demás |

**Apuesta segura: la C gana.** En marca personal, tú en cámara conviertes más que cualquier diseño. Los flyers son para el contenido del feed, para el remarketing y para que la página no se vea vacía — el anuncio de adquisición que mejor funciona casi siempre eres tú hablando.
