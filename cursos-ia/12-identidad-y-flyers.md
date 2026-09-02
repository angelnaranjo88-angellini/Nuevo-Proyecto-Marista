# 12 · Identidad Chaos Ctrl y prompts para flyers

## Parte 1 · La identidad visual

### El concepto
**Chaos Ctrl** ya trae la historia adentro: *del caos al control*. Ese es el
antes y después que vive tu cliente — el maestro ahogado en planeaciones, el
dueño de negocio con 12 horas de trabajo, la persona que siente que el tema se le
escapó. Toda la identidad visual debe contar esa transición.

**La regla visual, en una frase:** *desorden a la izquierda, orden a la derecha.*
Líneas enredadas que se resuelven en una retícula limpia. Fragmentos dispersos
que se alinean. Ruido que se convierte en señal. Si una pieza no cuenta esa
transición, no es Chaos Ctrl.

### Paleta

| Rol | Nombre | Hex | Uso |
|---|---|---|---|
| Fondo dominante | Carbón | `#0E1214` | El 70% de cada pieza |
| Texto principal | Blanco hueso | `#F2F3F0` | Titulares y cuerpo |
| Acento — el "Ctrl" | Cian eléctrico | `#14D6C4` | Orden, retícula, lo resuelto |
| Acento — el "Chaos" | Naranja señal | `#FF6B2C` | Precio, cupos, urgencia, botones |
| Apoyo | Gris humo | `#6B7A78` | Texto secundario, líneas |

**Regla de uso del naranja:** solo para lo que quieres que se vea primero — el
precio, "quedan 4 lugares", el botón. Si lo usas en todo, deja de funcionar.

### Tipografía

| Rol | Fuente | Alternativa en Canva |
|---|---|---|
| Titular | Archivo Black | Anton, Bebas Neue |
| Cuerpo | IBM Plex Sans | Inter, Work Sans |
| Datos y precios | IBM Plex Mono | Space Mono, Roboto Mono |

Titulares en **mayúsculas, muy apretados** (interletrado negativo). El mono para
precios y horarios hace que los datos se lean como datos.

### La regla que te va a ahorrar horas

> **Los generadores de imagen todavía escriben mal el texto en español.** Se
> equivocan con acentos, con la ñ, e inventan letras. No pierdas tiempo pidiendo
> flyers completos.
>
> **El flujo correcto: la IA genera el ARTE sin nada de texto, y el texto lo
> pones tú en Canva.** Tarda menos, se ve mejor, y puedes cambiar la fecha y el
> precio en diez segundos sin regenerar nada.

Los prompts de abajo están escritos para eso. El único caso donde vale la pena
pedir texto integrado es una palabra corta en inglés sin acentos.

### Por qué los prompts están en inglés
Los generadores de imagen entienden mucho mejor el inglés: más precisión en
estilo, luz y encuadre. Cópialos tal cual. Lo que va entre `[corchetes]` es lo
que tú cambias.

---

## Parte 2 · Prompts de marca

### 2.1 Isotipo / logo

Para ChatGPT, Ideogram o Midjourney. Genera varias y llévala a un diseñador o a
Canva para vectorizarla.

```
Minimal logo mark for a brand called Chaos Ctrl. A single keyboard key
viewed at a slight three-quarter angle. The lower half of the key is a
precise, sharp geometric square; the upper half dissolves upward into
scattered pixel fragments and thin broken lines. Flat vector illustration,
two colors only: off-white #F2F3F0 on deep charcoal #0E1214. Bold,
geometric, confident, no gradients, no shading, no text, no letters.
Centered on a square canvas with generous margin.
```

**Variante con acento de color** — cambia la última parte por:
```
Three colors only: off-white #F2F3F0 and electric teal #14D6C4 on deep
charcoal #0E1214. The ordered lower half in teal, the dissolving fragments
in off-white.
```

### 2.2 Fondos de marca (el caballo de batalla)

Estos son los que más vas a usar: arte abstracto de marca, sin texto, listo para
que le pongas el titular encima en Canva.

**Fondo A — la transición caos→orden (el principal)**
```
Abstract brand background for a technology education company. Left side:
a chaotic tangle of thin luminous lines, scattered fragments, digital
glitch artifacts, visual noise, disorder. Right side: the same lines
resolved into a clean, precise, calm geometric grid. A smooth transition
between the two halves across the center. Deep charcoal background
#0E1214, electric teal #14D6C4 lines, small accents of signal orange
#FF6B2C. Cinematic side lighting, subtle film grain, high contrast, deep
blacks. Absolutely no text, no letters, no numbers, no logos, no
watermarks. [FORMATO]. Generous empty negative space in the [lower
third / left half] for typography.
```

**Fondo B — la retícula que respira**
```
Abstract dark background: a precise geometric grid of thin electric teal
#14D6C4 lines on deep charcoal #0E1214, with a few nodes glowing softly
in signal orange #FF6B2C. Depth of field, the grid fading into darkness
toward the edges. Minimal, technical, calm, premium. Subtle film grain.
No text, no letters, no logos. [FORMATO]. Large empty dark area in the
center-left for typography.
```

**Fondo C — el escritorio de noche**
```
Overhead photograph of a dark wooden desk at night, lit only by the cool
glow of a laptop screen and a small warm desk lamp at the edge of frame.
On the desk: an open notebook with handwritten notes, a pen, a coffee
cup, reading glasses. Deep shadows, teal screen glow, warm lamp
highlights. Moody, intimate, real — not a staged stock photo. Shallow
depth of field, 35mm, subtle grain. No text, no visible screen content,
no logos. [FORMATO]. The upper third mostly dark and empty for
typography.
```

**Sustituye `[FORMATO]` por lo que necesites:**

| Dónde va | Formato | Qué escribir |
|---|---|---|
| Feed de Facebook e Instagram | 4:5 | `Vertical composition, 4:5 aspect ratio` |
| Publicación cuadrada | 1:1 | `Square composition, 1:1 aspect ratio` |
| Historias y Reels | 9:16 | `Vertical composition, 9:16 aspect ratio` |
| Portada de la página | 16:9 | `Wide horizontal composition, 16:9 aspect ratio` |

---

## Parte 3 · Prompts por curso

Estos son fotografías editoriales. **Funcionan mejor que el arte abstracto para
vender**, porque el cliente se ve a sí mismo en la imagen. Úsalos como creativo
principal del anuncio y deja los fondos abstractos para las piezas de marca.

### 3.1 Ctrl + Inicio

```
Editorial documentary photograph of a [Mexican woman in her late 30s] at
a small kitchen table at night, laptop open, taking handwritten notes in
a notebook. Focused and calm, looking at the screen — not at the camera,
not smiling. A warm desk lamp is the only strong light; cool blue night
light comes through the window behind. Modest, real Mexican home
interior. Shot on 50mm, shallow depth of field, natural skin texture,
visible grain. Documentary style, absolutely no stock-photo gloss, no
staged perfection. Deep charcoal shadows, warm highlights, a hint of teal
in the screen glow. Vertical 4:5. Subject on the right third, leaving
clean dark negative space on the left for text. No text, no logos, no
readable screen content.
```

**Variantes para probar** — cambia solo la parte entre corchetes:
- `Mexican man in his early 30s`
- `Mexican woman in her 50s`
- `young Mexican man in his mid 20s`

Genera las cuatro y prueba cuál convierte mejor. **La edad del modelo en el
anuncio es la variable que más mueve el costo por mensaje.**

### 3.2 Ctrl + Aula (docentes)

```
Editorial documentary photograph of a [Mexican woman teacher in her
mid-40s] at a dining table at night, surrounded by tall stacks of student
notebooks and loose papers, a laptop open beside her. She is closing one
notebook with a small look of relief, shoulders relaxed. Warm lamp light
from the left, cool blue window light behind. Real Mexican home interior,
lived-in, not styled. Shot on 50mm, shallow depth of field, natural skin
texture, film grain. Documentary, honest, warm. Deep shadows. Vertical
4:5, subject on the right, dark empty space upper left for a headline.
No text, no logos, no readable writing.
```

**Variante "el antes"** — para la mitad izquierda de un antes/después:
```
Same setting and same woman, but overwhelmed: stacks of notebooks
towering, papers scattered, hand on forehead, tired. Cold blue-grey
light, no warmth. Same documentary style. Vertical 4:5.
```

### 3.3 Ctrl + Negocio (emprendedores)

```
Editorial documentary photograph of a [Mexican man in his mid-30s], owner
of a small business, standing inside his own shop after closing hours.
Lights partly off, shelves and merchandise softly out of focus behind
him. He is looking at his phone with a calm, satisfied expression. Warm
practical lighting from a single overhead lamp, teal shadows in the
background. Real small Mexican business interior — a papelería, a
refaccionaria, a small workshop. Shot on 35mm, shallow depth of field,
natural texture, film grain. Documentary, grounded, no corporate
stock-photo feel. Vertical 4:5, subject on the left, dark empty space on
the right for text. No text, no logos, no readable screen.
```

---

## Parte 4 · Consistencia entre imágenes

Para que todas tus piezas se vean de la misma marca, **pega este bloque al final
de cualquier prompt**:

```
Style reference: dark editorial documentary photography, deep charcoal
#0E1214 shadows, electric teal #14D6C4 in screen and cool light, signal
orange #FF6B2C only as a small warm accent. High contrast, deep blacks,
visible film grain, natural skin texture, single dominant light source,
no HDR, no glossy stock-photo look, no lens flare, no artificial smiles.
```

**Truco adicional:** cuando una imagen te quede bien, guárdala y en las
siguientes súbela como referencia diciendo *"same lighting, same color grading,
same photographic style as this reference"*. Es la forma más rápida de mantener
la línea sin repetir el prompt entero.

---

## Parte 5 · El flyer armado en Canva

Con la imagen generada, el armado toma cinco minutos. Estructura fija:

```
┌─────────────────────────────┐
│  CHAOS CTRL          ← logo pequeño, arriba izquierda
│                             │
│  TITULAR EN            ← Archivo Black, mayúsculas,
│  DOS O TRES              interletrado apretado,
│  LÍNEAS                  blanco hueso, 3 líneas máx.
│                             │
│  Subtítulo de una línea  ← IBM Plex Sans, gris humo
│  que dice para quién es     │
│                             │
│  ─────────────────          │
│  ⬛ 5 sesiones · 10 horas ← mono, blanco
│  ⬛ Grupos de 10 máximo     │
│  ⬛ 1 mes de asesoría       │
│  ─────────────────          │
│                             │
│  $1,290          ← naranja señal, mono, GRANDE
│  Inicia [FECHA] · quedan [N] lugares  ← naranja
│                             │
│  [ ESCRÍBEME POR WHATSAPP ] ← botón naranja sólido
└─────────────────────────────┘
```

**Las cinco reglas del armado:**
1. **El fondo va oscurecido.** Ponle una capa negra al 40–55% de opacidad encima
   de la foto. Sin eso el texto no se lee y el anuncio no funciona.
2. **Máximo tres tamaños de letra** en toda la pieza.
3. **Un solo elemento naranja dominante.** El precio o el botón, no los dos al
   mismo tamaño.
4. **Poco texto.** Facebook penaliza las imágenes saturadas de letras y la gente
   no las lee. Si no se entiende en dos segundos, sobra texto.
5. **Guárdalo como plantilla.** Cambias titular, fecha y precio para los otros
   dos cursos y ya tienes las tres piezas.

### Titulares que puedes usar

**Ctrl + Inicio**
- NO USES CHATGPT / COMO BUSCADOR
- LO QUE NADIE / TE ENSEÑA / DE LA IA
- 10 HORAS / Y DEJAS DE / IR ATRÁS

**Ctrl + Aula**
- RECUPERA / TUS TARDES
- LA IA NO / TE VA A / QUITAR TU / TRABAJO
- TUS ALUMNOS / YA LA USAN

**Ctrl + Negocio**
- QUE TU / NEGOCIO / TRABAJE SOLO
- 12 HORAS / AL DÍA / NO SON / NORMALES
- AUTOMATIZA / O TE / ALCANZAN

---

## Parte 6 · Texto del anuncio

El creativo detiene el scroll; el texto cierra. Estos van en el campo de texto
principal, con el objetivo **Mensajes a WhatsApp**.

### Ctrl + Inicio
> Llevo un año usando inteligencia artificial todos los días para operar mis
> negocios. Y me di cuenta de algo: casi todos los cursos que veo enseñan menos
> de lo que ya sabe cualquiera que la haya usado dos semanas.
>
> Por eso armé Chaos Ctrl.
>
> 10 horas en vivo, de lunes a viernes de 7 a 9 de la noche — porque sé que sales
> de trabajar a las 6. Máximo 10 personas, cada quien trabajando con su caso
> real. No solo ChatGPT: te enseño qué herramienta sirve para cada tarea y cómo
> usar la aplicación completa, no el 10% que usa todo el mundo.
>
> Y cuando termina, me quedo un mes contigo resolviéndote dudas.
>
> $1,290. Inicia el [FECHA]. Quedan [N] lugares.
>
> Escríbeme y te digo si es para ti o no — con honestidad, porque no me sirve un
> alumno que no lo va a aprovechar.

### Ctrl + Aula
> Si eres maestro, esto es para ti.
>
> No te voy a enseñar "qué es la inteligencia artificial". Te voy a enseñar a
> recuperar entre 4 y 8 horas a la semana de planeaciones, rúbricas,
> retroalimentación e informes. Y qué hacer cuando tus alumnos entreguen trabajos
> hechos con IA — porque ya lo están haciendo y los detectores no funcionan.
>
> 8 horas en vivo, cuatro sábados por la mañana. Máximo 12 personas. Un mes de
> asesoría conmigo después del curso. Constancia con horas.
>
> $1,490 — y si vienen tres colegas de tu escuela, pagan dos.
>
> Escríbeme y platicamos.

### Ctrl + Negocio
> Si tienes un negocio y trabajas 12 horas al día, no necesitas otro curso de
> ChatGPT.
>
> Necesitas salir con algo funcionando.
>
> En Chaos Ctrl construimos en clase, con los datos de tu negocio, al menos una
> automatización corriendo de verdad: mensajes que se clasifican y contestan
> solos, cotizaciones que se generan y envían, tu reporte de ventas llegándote
> cada lunes al WhatsApp.
>
> Yo lo uso todos los días en mis empresas. Eso es lo que enseño.
>
> 8 horas en vivo, cuatro sábados. Solo 8 lugares, porque trabajamos negocio por
> negocio. $1,500.
>
> Escríbeme y te digo si tu negocio es candidato.

---

## Parte 7 · Qué probar primero

No hagas 20 creativos. Haz **tres por curso** y déjalos correr:

| Versión | Qué cambia | Qué estás midiendo |
|---|---|---|
| **A** | Foto editorial del cliente ideal | La conexión con el público |
| **B** | Fondo abstracto de marca + titular grande | Si el mensaje solo, sin rostro, funciona |
| **C** | Video vertical tuyo hablando a cámara, 30 s, sin música | Tu cara contra todo lo demás |

**Apuesta segura: la C gana.** En marca personal, tu cara conviene más que
cualquier diseño. Los flyers sirven para el resto del contenido y para el
remarketing; el anuncio de adquisición que mejor convierte casi siempre eres tú
hablando, sin producción.
