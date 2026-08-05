# SP06 · Calificación y asignación — estructura v2

> Construido el 5-ago. Workflow `84811c16-30d8-4c08-a05d-0c12fa46567d`, **draft**,
> carpeta `GALK 2.0 · 04 Sales Pipeline`. Trigger: tag `galk-bot-calificado` (inactivo).
>
> Este documento existe porque ClickUp estaba con rate limit el día del cambio.
> **Pendiente: subirlo a la tarjeta de SP06 cuando ClickUp vuelva.**

## Qué estaba mal en la v1

La v1 tenía 7 nodos, todos lineales. Tres problemas:

1. **Dos movimientos de etapa seguidos.** `create_opportunity` a "Calificado" y, milisegundos
   después, otro a "Asignado a asesor". Nadie ve nunca la oportunidad en Calificado, y el
   tiempo-en-etapa de esa etapa da ~0 para todos los leads → el reporte del pipeline queda inútil.

2. **El segundo movimiento borraba la atribución.** El primer nodo seteaba
   `opportunity_source = {{contact.fuente}}`; el segundo lo omitía. Como `create_opportunity` es
   en realidad *create-or-update* y reescribe con lo que le mandes, la segunda pasada dejaba la
   fuente vacía — justo lo que LS01 se toma el trabajo de capturar desde Meta.

3. **No había rama de fallo.** Si el round robin no asignaba a nadie, el flujo igual escribía el
   campo vacío, igual movía la oportunidad a "Asignado", igual notificaba a nadie e igual ponía
   `bot-silenciado`. Resultado: **el lead quedaba marcado como atendido, con el bot mudo y sin
   dueño humano**. Se perdía en silencio, que es exactamente el problema que este proyecto vino
   a resolver.

## Estructura v2

```
TRIGGER · tag "galk-bot-calificado"
   │
   ├─ 1  Update contact ····· Calificado = Sí · Fecha de calificación
   │
   ├─ 2  Opportunity ········ etapa "Calificado"    status=open
   │                          name={{contact.name}} source={{contact.fuente}}
   │
   ├─ 3  Assign user ········ Round Robin · 6 asesores · equally
   │
   ├─ 4  Wait ··············· 1 minuto        ← seguro, ver nota
   │
   ├─ 5  Update contact ····· Asesor asignado = {{user.name}}
   │                          Fecha de asignación = hoy
   │
   └─ 6  IF/ELSE ············ ¿"Asesor asignado" tiene valor?  (has_value)
          │
          ├── SÍ ─┬─ 7  Opportunity ····· etapa "Asignado a asesor"
          │       │                        source={{contact.fuente}}   ← NO omitir
          │       │
          │       ├─ 8  Notificación ···· al assigned_user
          │       │                        "🎯 Lead calificado asignado"
          │       │
          │       └─ 9  Add tag ········· bot-silenciado
          │
          └── NO ─┬─ 10 Notificación ···· a Lucía Galvez (specific_user)
                  │                        "⚠️ Round robin no asignó — lead sin dueño"
                  │
                  └─ 11 Add tag ········· asignacion-fallida

                     La oportunidad se QUEDA en "Calificado".
                     Y el bot NO se silencia: sigue vivo por si el lead
                     escribe de nuevo, en vez de dejarlo hablando solo.
```

## Por qué así

**"Calificado" pasa a significar algo real:** *calificado y todavía sin dueño*. Es donde se queda
la oportunidad cuando la asignación falla. Deja de ser una etapa fantasma por la que todos pasan
sin detenerse.

**Las dos actualizaciones dejan de ser lineales** porque la segunda cuelga del if/else. Ese era
el reclamo original y es correcto: dos movimientos seguidos sin nada que los separe no aportan nada.

**El orden importa.** El `update contact` del asesor va ANTES del if/else, no dentro de la rama
SÍ. Es lo que permite ramificar: si el round robin no asignó, `{{user.name}}` resuelve vacío, el
campo queda vacío y `has_value` manda el flujo a la rama de fallo. Si el update estuviera dentro
de la rama, no habría nada sobre lo cual condicionar.

**El Wait de 1 minuto** es un seguro para que `{{user.name}}` resuelva después de que el round
robin materialice la asignación. Cuesta un minuto de retraso en la notificación al asesor. Se
puede quitar: el if/else igual protege, solo que el campo podría quedar vacío en una condición
de carrera y mandar a la rama de fallo un lead que sí tenía dueño.

## Detalles de esquema verificados contra la subcuenta

- `has_value` / `has_no_value` van **sin clave `conditionValue`**. Confirmado en el WF1 de
  Francisco y en LS01/SP05. Los operadores que existen en esta subcuenta son exactamente:
  `contain`, `index-of-true`, `is`, `has_value`, `has_no_value`.
- Los `wait` en minutos usan `{"type":"minutes","value":N,"when":"after"}`.
- `internal_notification` sí acepta `next` (la nota vieja del handoff decía que no; en SP06 v1
  ya lo tenía y funciona). Para notificar a alguien concreto: `userType:"specific_user"` +
  `selectedUser`.

## Tag nuevo

`asignacion-fallida` — creado el 5-ago. Verificado contra los workflows **publicados** de
Francisco: cero colisiones.
