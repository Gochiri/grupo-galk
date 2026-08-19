# Acuerdos — reunión 19-ago-2026 (Lucía, Gomer, Francisco, Henry, Oliver, Germán)

> Demo en vivo del ecosistema nuevo. Salió bien (la ficha llegó como link por el plugin SMS,
> se explicó que con el API oficial sale la imagen). El cliente pidió UN cambio grande de flujo
> y varios menores. **Nada construido aún** — este doc captura lo acordado antes de tocar nada.

## 1. El cambio grande: la ficha se envía al detectar el CURSO, no al confirmar sede

Así vende Lucía hoy por WhatsApp (36:43): llega "hola, vengo por el taller de electricidad" y
le disparan de frente la secuencia completa, sin perfilar nada más:

```
1. Texto de apertura   (saludo + explicación chiquita + oferta + sedes + qué incluye)
2. Imagen 1 + texto corto      ┐
3. Imagen 2 + texto corto      │ 4 imágenes seguiditas, EN ORDEN
4. Imagen 3 + texto corto      │ (cada imagen DEBE llevar texto, si no la plantilla no sale)
5. Imagen 4 + texto corto      ┘
6. Texto final: "¿Te interesa la sede Surco, Los Olivos o provincia Arequipa?"
```

- Las imágenes llevan el temario, herramientas, proyecto final, horas, sedes, alianzas —
  "las personas no leen texto; con imágenes captas y demuestras que es real" (Lucía, 16:00).
- **Las fichas son por CURSO, no por sede** (36:06: "¿hay imágenes exclusivas de una sede? No").
  Los horarios por sede los maneja el asesor humano.
- La secuencia es **automatización, no IA** (37:00, Oliver): mensajes mecanizados por workflow.
- **La IA se enciende justo al final de la secuencia** (37:40): cuando el lead responde la
  pregunta de sede, el bot de familia guarda la sede, resuelve dudas, deriva al asesor y a los
  3 minutos se apaga. El perfilamiento de sede/modalidad del bot ANTES de dar info desaparece.
- Melamina: Lucía envía **una ficha del taller desde cero y con la promoción engancha el
  avanzado** (Pack) — no dos fichas separadas, "si los separo no cierro dos ventas en un
  cliente" (18:00). Electricidad: los dos niveles van en una sola ficha. ⚠️ Confirmar con el
  contenido real que mande Lucía/Francisco cómo quedan drywall y melamina.

## 2. Cambios menores acordados

| Qué | Detalle |
|---|---|
| Vocabulario BOT-00 | "software" → **"programas de modelado en 3D"** (11:46) |
| Prioridad | **TALLERES primero** — es el volumen de la empresa (31:00). Software/gestión después |
| Plantillas WABA | Se crean **NUEVAS en carpeta aparte**; las de Francisco NO se tocan ni se editan (42:16). Meta tarda ~1 día en aprobar |
| Texto por imagen | Texto corto alusivo al contenido de cada imagen (39:13, aprobado por Lucía); el orden lo manda ella |
| Deadline | Contenido de Lucía → Francisco hoy mismo; **todo listo con plantillas aprobadas el VIERNES** (41:30) y pauta chiquita de prueba |
| Bloqueos de número | Resuelto de raíz con el API oficial de Meta (29:00) |
| Reactivación del bot | Para matriculados/remarketing (26:00): definir en qué etapa o tiempo se re-enciende el bot (ej. al marcar "curso cumplido"). El mismo asesor atiende todos los cursos del mismo cliente — no hay conflicto. **Pendiente de diseño, ligado a P1** |

## 3. Qué implica en lo construido (evaluación, pendiente de aprobar)

**Se queda igual:** SP06 (calificación por datos, guarda, gracia 3 min, asignación, notificación),
WF-MOD, WF-SEDE, WF-NORM-1..4, WF-SWITCH, LS01, pipeline, campos, la infraestructura de pruebas.

**Cambia:**

1. **SP05 → v2 "secuencia de ficha"**: árbol por CURSO (≈10 ramas, ya no 24 curso×sede),
   cada rama = 6 nodos de mensaje (texto intro, 4 imágenes con texto, pregunta final) +
   marcador + **activar el bot de familia** al final. Trigger: solo `Curso de interés` cambió.
2. **BOT-00 recupera la captura de `Curso de interés`** (se le quitó cuando calificaba al
   instante; ese problema muere con el flujo nuevo: detectar curso = disparar ficha, no calificar).
3. **Prompts v4 de BOT-01/02/03**: dejan de presentar el curso (la ficha lo hace). Nuevo rol:
   capturar la sede de la respuesta a la pregunta final, resolver dudas puntuales con su KB,
   derivar. Las KB se quedan como fuente de respuestas correctas.
4. **Custom values de ficha**: se remodelan por curso (4 imágenes + textos por curso), ya no
   por curso+sede.
5. **WF-SWITCH debe quitar también el tag `ficha-enviada`**: si el lead cambia de curso, la
   ficha del curso nuevo tiene que poder salir (hoy la guarda la bloquearía).
6. **Plantillas WABA nuevas** (1 por mensaje: imagen+texto), carpeta propia, aprobación Meta.
   Mientras, las pruebas siguen por el gateway SMS con `image - <url>`.

## 4. Contenido pendiente de recibir (Lucía → Francisco → Oliver)

Por cada curso: texto de apertura · 4 imágenes EN ORDEN con su texto corto · texto final.
Las imágenes de talleres ya están en `FICHAS WHATSAPP` del media store (Melamina 4+4,
Drywall 4+4, Electricidad 4). Faltan software y gestión (después, por prioridad).

Se irá guardando en `contenido-fichas/<curso>.md` conforme llegue.

## 5. Preguntas abiertas antes de construir

1. ¿Ficha unificada por taller (desde cero + avanzado con promo Pack, como vende Lucía) o
   una por nivel? Define cuántas ramas y qué imágenes van (el store tiene 4 por nivel).
2. ¿Qué pregunta final llevan los cursos online (software/gestión), donde no hay sede?
3. ¿El WhatsApp API oficial ya está conectado a la subcuenta? (bloqueante para crear
   plantillas y para el viernes)
4. Confirmar con Lucía los textos cortos por imagen (ella manda el orden y el lenguaje).
