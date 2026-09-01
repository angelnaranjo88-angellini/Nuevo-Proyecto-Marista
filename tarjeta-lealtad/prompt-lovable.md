# Santa Nails — App de tarjetas de lealtad

## Qué es

Una app web para **Santa Nails**, un estudio de uñas en México. Sustituye la
tarjeta de lealtad de papel: las tarjetas viven aquí. Cuando una clienta termina
su cita, yo abro la app en el mostrador y le registro el sello.

**Qué NO es:** no imprime nada, no cobra, no agenda citas, no tiene app móvil
nativa. Es una web app que uso desde mi teléfono.

## Quién la usa

Yo y quien atienda en el estudio. **Una sola cuenta.** Las clientas no se
registran ni tienen contraseña — yo las doy de alta.

Hay una excepción, en la Fase 3: cada tarjeta tiene un enlace público de solo
lectura para que la clienta vea cómo va su tarjeta desde su celular.

## Stack

React + Vite + Tailwind + shadcn/ui + Supabase. Todo lo que se guarda va en
Supabase, nada en `localStorage`.

**Mobile-first.** La voy a usar de pie, con una clienta enfrente esperando, con
una mano. Los botones principales de mínimo 48px de alto. Que se vea bien en
un iPhone; el escritorio es secundario.

---

## Las reglas del programa

Esta es la parte que más importa. **La app tiene que hacer cumplir estas reglas,
no solo mostrarlas.** Si una regla no se cumple, el botón se bloquea y dice
exactamente por qué.

Ponlas todas como constantes en un solo archivo `src/config/programa.ts`, para
que yo pueda cambiarlas después sin tocar el resto del código:

```ts
export const PROGRAMA = {
  SELLOS_PARA_PREMIO: 5,
  MONTO_MINIMO_SELLO: 400,        // MXN para ganar un sello
  MONTO_MINIMO_CANJE: 500,        // MXN de la cuenta al canjear
  PORCENTAJE_DESCUENTO: 0.20,
  TOPE_DESCUENTO: 150,            // MXN
  VIGENCIA_TARJETA_MESES: 8,      // desde el primer sello
  DIAS_PARA_USAR_PREMIO: 60,      // desde el 5º sello
  VISITAS_PAGADAS_MINIMAS: 4,     // aunque tenga sellos de referido
  MAX_SELLOS_REFERIDO: 2,         // por tarjeta
  DESCUENTO_BIENVENIDA: 50,       // MXN para la clienta referida
  MONTO_MINIMO_BIENVENIDA: 400,
  DIAS_VIGENCIA_BIENVENIDA: 60,
  // Fechas donde NO se puede canjear (alta demanda)
  FECHAS_BLOQUEADAS: {
    meses: [12],                  // diciembre completo
    dias: ['05-10', '02-14']      // 10 de mayo, 14 de febrero
  }
};
```

### Para AGREGAR UN SELLO, todo esto debe cumplirse

1. La tarjeta está activa y no vencida (menos de 8 meses desde el primer sello).
2. La tarjeta tiene menos de 5 sellos.
3. **No hay ya un sello registrado hoy para esa clienta.** Un sello por cita y
   por persona.
4. Si es sello de visita: el monto capturado es de **$400 o más**.
5. Si es sello de referido: esa tarjeta tiene menos de 2 sellos de referido.

Si algo falla, el botón se deshabilita y aparece el motivo exacto. Nada de
"error"; quiero leer *"Ya registraste un sello hoy para Ana"* o
*"$380 no alcanza — el mínimo es $400"*.

### Para CANJEAR EL PREMIO, todo esto debe cumplirse

1. Tiene exactamente 5 sellos.
2. Tiene **mínimo 4 visitas pagadas** (los sellos de referido no cuentan aquí).
3. No pasaron más de 60 días desde el quinto sello.
4. La tarjeta no está vencida.
5. El monto de la cuenta es de **$500 o más**.
6. **Hoy no es fecha bloqueada** (diciembre, 10 de mayo, 14 de febrero).

El descuento es `min(monto * 0.20, 150)`. La app me lo calcula y me muestra:

> Cuenta: $650 · Descuento: $130 · **A cobrar: $520**

Al confirmar el canje: la tarjeta pasa a `completada` y **se abre una tarjeta
nueva vacía automáticamente**. La visita del canje **no genera sello**.

### Referidos

Cuando doy de alta una clienta nueva puedo marcar **quién la refirió**.

- La clienta nueva queda con un **descuento de bienvenida de $50**, disponible
  solo en su primera visita, en servicios desde $400, vigente 60 días.
- Cuando le registro su **primer servicio de $400 o más**, la app hace dos cosas
  sola, sin que yo tenga que acordarme:
  1. Marca su descuento de bienvenida como usado.
  2. **Le da el sello extra de referido a quien la refirió** — siempre que esa
     tarjeta no tenga ya 2 sellos de referido.
- Si la referidora ya llegó al tope, no se lo da y me avisa por qué.

---

## Modelo de datos (Supabase)

```
clientas
  id                            uuid pk
  nombre                        text not null
  telefono                      text not null          -- índice para buscar
  referida_por                  uuid null → clientas.id
  bienvenida_estado             text  -- 'no_aplica' | 'disponible' | 'usada' | 'expirada'
  bienvenida_vence_en           date null
  notas                         text null
  creada_en                     timestamptz default now()

tarjetas
  id                            uuid pk
  clienta_id                    uuid → clientas.id
  estado                        text  -- 'activa' | 'completada' | 'vencida'
  abierta_en                    date null   -- fecha del PRIMER sello, null si vacía
  creada_en                     timestamptz default now()
  -- una clienta tiene como máximo UNA tarjeta 'activa' a la vez

sellos
  id                            uuid pk
  tarjeta_id                    uuid → tarjetas.id
  tipo                          text  -- 'visita' | 'referido'
  monto                         numeric null   -- null en los de referido
  referida_id                   uuid null → clientas.id   -- quién fue la invitada
  fecha                         date not null
  creado_en                     timestamptz default now()

canjes
  id                            uuid pk
  tarjeta_id                    uuid → tarjetas.id
  monto_cuenta                  numeric not null
  descuento                     numeric not null
  fecha                         date not null
```

**Nada de campos calculados guardados.** El número de sellos, las visitas
pagadas y las fechas de vencimiento se derivan de `sellos` en el momento. Si
guardas un contador, se va a desincronizar.

Pon la lógica de "¿puede sellar?" y "¿puede canjear?" en **un solo módulo**
`src/lib/reglas.ts` que reciba la tarjeta con sus sellos y devuelva
`{ puede: boolean, motivo: string | null }`. Las pantallas solo consultan eso —
no repartas la lógica entre componentes.

---

## Pantallas

### 1. Entrar

Login de Supabase con correo y contraseña. Una sola cuenta. Sin registro
público, sin "crear cuenta".

### 2. Hoy (pantalla principal)

Lo primero que veo al entrar:

- **Buscador grande hasta arriba**, con foco automático. Busca por nombre o
  teléfono conforme escribo. Es lo que más uso: llega la clienta, la busco,
  le sello.
- Botón **+ Nueva clienta**.
- **Listas cortas que me dicen dónde actuar**, cada una con su chip de color:
  - `Listas para canjear` — tienen 5 sellos y pueden canjear hoy.
  - `Su premio vence pronto` — menos de 15 días para que se les venza.
  - `Tarjeta por vencer` — menos de 30 días de los 8 meses.
  - `Sin venir hace 6+ semanas` — con botón para copiar su teléfono. Ésta es la
    lista que me hace ganar dinero: son clientas que se están yendo.

Si una lista está vacía, no la muestres.

### 3. Ficha de la clienta

Lo más importante de la app. De arriba a abajo:

1. **Nombre y teléfono.** El teléfono con botón para copiar y para abrir WhatsApp.
2. **El carnet.** Cinco círculos en fila, igual que la tarjeta física:
   los sellos ganados se llenan con **el hada** (voy a subir el PNG); los que
   faltan quedan como círculo vacío con borde punteado. Debajo de cada uno, la
   fecha en que se puso. Si un sello fue por referido, marca ese círculo con un
   detalle distinto y el nombre de la invitada.
3. **Estado en una línea**, en lenguaje humano:
   *"3 de 5 sellos · Tarjeta vence el 14 de marzo"*
   o *"¡Puede canjear! · El premio vence en 12 días"*.
4. **Botones de acción**, grandes:
   - **Agregar sello** → pide el monto en un teclado numérico. Si es menor a
     $400, el botón de confirmar queda bloqueado con el motivo visible.
   - **Canjear premio** → solo aparece si tiene 5 sellos. Pide el monto de la
     cuenta, calcula el descuento y me muestra el total a cobrar antes de
     confirmar.
   - **Registrar referido** → busco a la invitada entre las clientas y le doy
     el sello extra.
5. **Historial**: cada sello y cada canje, con fecha y monto. También las
   tarjetas anteriores ya completadas, colapsadas.

Toda acción que modifique algo pide una confirmación de un paso, y se puede
**deshacer durante 30 segundos** con un toast. Me voy a equivocar de clienta
alguna vez y necesito arreglarlo sin entrar a la base de datos.

### 4. Nueva clienta

Nombre, teléfono y, opcional, **quién la refirió** (buscador entre las clientas
existentes). Al guardar, se le crea su tarjeta vacía. Si viene referida, se le
activa el descuento de bienvenida de $50 y se muestra en su ficha.

Valida que el teléfono no esté repetido. Si ya existe, me lleva a esa ficha en
lugar de crear una duplicada.

---

## Diseño

### Colores

Éstos son los de mi marca. Úsalos tal cual, en `index.css` bajo `:root`:

```css
:root {
  --sn-black:      #0B0B0B;   /* fondo del logo, tinta principal */
  --sn-cream:      #F5E9DA;   /* crema del logo */
  --sn-cream-soft: #FBF4EA;   /* fondo de la app */
  --sn-green:      #A8CEA2;   /* verde salvia */
  --sn-green-deep: #6E9A6A;   /* verde legible sobre crema */
  --sn-pink:       #F9A8B5;   /* rosa */
  --sn-pink-deep:  #C9707F;   /* rosa legible sobre crema */
  --sn-ink-soft:   #4A4640;
  --sn-muted:      #8A857F;
  --sn-rule:       #DDD6CF;
}
```

Reglas de uso:

- **Negro y crema son la base.** Verde y rosa son acentos.
- Para **texto** de color sobre crema usa siempre los tonos `-deep`. El verde y
  el rosa claros no alcanzan contraste legible para texto.
- Verde = confirmación y progreso. Rosa = alerta suave y referidos. Para
  bloqueos y errores usa un rojo neutro, **no el rosa de marca** — si el rosa
  significa error y también significa referido, deja de significar nada.
- Nada de degradados ni sombras de colores.

### Tipografía

- **Títulos y el número de sellos:** `Prata` (Google Fonts). Es lo más cercano
  a mi logo.
- **Todo lo demás:** `Jost` (Google Fonts).

### El carnet

Es el corazón de la app: es lo que le enseño a la clienta en la pantalla. Los
cinco círculos con el hada tienen que verse **bonitos y grandes**, no como una
barra de progreso genérica. Cuando se agrega un sello, que el hada aparezca con
una animación corta (300ms, escala + opacidad). Un solo momento, sin confeti ni
exageraciones.

Voy a subir el logo de Santa Nails y el PNG del hada. Úsalos como assets;
**no redibujes el logo con tipografía web.**

---

## Seguridad

Esto guarda nombres y teléfonos de mis clientas, así que no lo dejes abierto:

- **Activa RLS en las cuatro tablas.** Sin excepción.
- Todas las lecturas y escrituras requieren usuario autenticado.
- No expongas ninguna tabla a `anon` en la Fase 1.
- Las claves de Supabase van en variables de entorno, nunca en el código.

---

## Fases

Constrúyelo en este orden y no empieces la siguiente hasta que la anterior
funcione:

**Fase 1 — El núcleo.** Login, alta de clientas, buscador, ficha con el carnet,
agregar sello con sus validaciones, canjear premio con el cálculo del descuento.
Con esto ya puedo dejar el papel.

**Fase 2 — Referidos y recuperación.** Descuento de bienvenida, sello automático
a quien refiere, y las listas de la pantalla "Hoy" (por vencer, sin venir).

**Fase 3 — Vista para la clienta.** Ruta pública `/t/:codigo` de **solo lectura**
donde la clienta ve su carnet desde su celular. El código es un token aleatorio
largo por tarjeta, no un id secuencial. Requiere una política de RLS que permita
leer **solo esa tarjeta por su código**, y que no exponga el teléfono ni el
historial de montos.

---

## Qué NO quiero

- Nada de cobros, pasarelas de pago ni agenda de citas.
- Nada de registro público de clientas ni login para ellas.
- Nada de notificaciones push, correos automáticos ni SMS.
- Nada de dashboards con gráficas de ingresos, "insights" ni métricas que no
  pedí. Las únicas listas son las cuatro de la pantalla "Hoy".
- No guardes contadores de sellos en la base de datos: calcúlalos.
- No inventes reglas del programa. Están todas en `programa.ts`.
- No uses emoji en la interfaz.
- Nada de modo oscuro.
