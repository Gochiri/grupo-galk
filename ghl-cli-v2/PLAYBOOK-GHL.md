# PLAYBOOK GHL — todo lo aprendido a golpes (proyecto Grupo GALK, jul-ago 2026)

> Léelo ANTES de tocar una subcuenta nueva. Cada regla de aquí costó un bug real en
> producción. Las formas de nodo ya vienen empaquetadas en
> `gohighlevel/utils/wf_toolkit.py`; este documento explica el porqué.

## 0 · La regla de oro

**GHL guarda y muestra nodos malformados que después NO ejecutan, sin error alguno.**
Pasó 5 veces: el clear de campos que ejecutaba vacío, las notificaciones que no avisaban,
el body del SMS invisible, los attachments en [null], el canvas colapsado. Por eso:

1. **Nunca fabriques atributos de un nodo.** Crea uno igual A MANO en la UI, léelo por
   API y clona su forma exacta (los "moldes").
2. **"Se guardó" no es "funciona".** La única prueba real es una ejecución en vivo con un
   contacto de prueba, verificada por API (el panel de contacto cachea; la API es la verdad).
3. Todo script que escriba debe ser **idempotente** (verificar si ya existe y saltar) y
   tener **dry-run por defecto** con flag `--aplicar`.

## 1 · Las dos APIs y la autenticación

| Vía | Sirve para | Auth |
|---|---|---|
| Pública `services.leadconnectorhq.com` | pipelines, campos, custom values, contactos, usuarios, media store, conversaciones (lectura) | PIT (`pit-...`), header `Authorization: Bearer` + `Version: 2021-07-28` |
| Interna `backend.leadconnectorhq.com` | **workflows y triggers (CRUD completo)** | token Firebase, header `token-id` (NO Bearer). Rota seguido: en 401, pedir uno nuevo de la extensión de Chrome |
| Solo UI | **bots de Conversation AI** (prompts, acciones, canales), carpetas de campos | — |

## 2 · Workflows por API — los 6 gotchas mortales

1. **El PUT de workflow resetea a default todo campo raíz omitido.** El más doloroso:
   `allowMultiple` (Reingreso). Inclúyelo SIEMPRE en el body (`put_workflow()` del toolkit
   lo hace solo).
2. **`allowMultiple` apagado = el contacto entra UNA vez EN SU VIDA.** Los workflows con
   guarda de entrada ("salir si faltan datos") lo NECESITAN encendido, o el contacto entra
   incompleto, la guarda lo saca, y jamás puede volver. No activarlo en workflows que hacen
   algo hacia afuera al entrar, salvo con marcador de "ya hecho".
3. **`targetActionId` (el nodo por donde entra el trigger) vive en OTRO endpoint** y no se
   actualiza al regenerar nodos: queda apuntando a un nodo muerto y el workflow no corre ni
   avisa. Si el PUT preserva los IDs de nodos, no se rompe; si los regenera, reapunta el
   trigger. `targetActionId: null` es VÁLIDO (entrada por defecto). Verifica siempre con
   `verificar_triggers()`.
4. **Condiciones de trigger sobre campos: formato DOBLE.** `field: "contact.<ID>"` **y**
   `id: "<ID>"`. Con el ID pelado se guarda, la UI muestra "Seleccionar" y nunca dispara.
   Usa `cond_trigger_campo()`.
5. **Publicado ≠ funcionando.** Al terminar: `status == published` **y** cada trigger
   `active == true` **y** target válido **y** condiciones bien formadas.
6. **Mandar `active: true` en el PUT de un trigger PUBLICA el workflow.** Cuidado al
   editar triggers de borradores.

## 3 · Convención de nodos que el canvas renderiza (y ejecuta)

- **Header if/else**: `nodeType: "condition-node"`, SIN `parent`, `next` = **LISTA** con
  los ids de todas sus ramas. Sus `attributes.branches` definen id/nombre/segments.
- **Ramas**: `nodeType: "branch-yes"/"branch-no"`, `parent` = header,
  `sibling` = [ids de las otras ramas], `next` = primer nodo de su cadena.
- **If anidado**: se cuelga SOLO por el `next` de la rama contenedora — SIN parent propio.
- **Nodos de cadena**: `parent`/`parentKey` = **el id de la RAMA** (no el nodo anterior),
  encadenados por `next`.
- `whatsapp_v2`, `whatsapp_media` y `update_conversation_ai_status` llevan además
  `workflowsActionType: "INTERNAL"` a nivel de nodo (sin él, el PUT rechaza con
  "corrupted type").
- Romper cualquiera de estas reglas colapsa el canvas (se ve "trigger → yes → FINAL").
  La forma más segura de armar un árbol nuevo: reutilizar como esqueleto los nodos
  estructurales de un workflow que ya renderiza.

## 4 · Formas de nodo con trampa (todas resueltas en `wf_toolkit.py`)

| Nodo | Trampa | Forma buena |
|---|---|---|
| SMS inline | el cuerpo NO va en `message` | `body`; `attachments` con URL ejecuta `[null]` — imagen como línea `image - <url>` si el gateway lo soporta |
| WhatsApp free-form | la UI lo crea multipath (Delivered/Undelivered) | `toggle_branch:false, transitions:[]` para cadena recta; requiere sesión de 24h abierta |
| WhatsApp media | la UI no acepta URL | el JSON sí: `media_url:[{name,url,size}]` con URL del propio media store; `media_type: "image"` o `"document"` (PDF validado, hasta 7+MB) |
| Notificación interna | `userType` inventado no avisa a NADIE | dueño: `assign`+`assignedOwners:["contact_owner"]` · concreto: `user`+`selectedUser` |
| Clear de campos | sin `value`/`date`/type correcto ejecuta `customFields: []` (no-op) | cada campo: `field,value:"",date:"",title,type` (`select` para dropdowns) |
| Oportunidad | sin `monetary_value` falla/queda coja | incluir siempre (merge field vale) |
| Wait | — | acepta `{"type":"seconds"}` (pausas de 3s entre mensajes se sienten humanas) |
| update_conversation_ai_status | **REASIGNA** la conversación, no solo enciende/apaga | pausar: `keep-same`+`inactive` · activar bot: `<botId>`+`active` (esto puede DESPERTAR una conversación silenciada) |

## 5 · Conversation AI (bots) — todo es UI, y tiene sus leyes

- **Campos de texto de acciones: límite 500 caracteres** (Transfer: 10-500). El prompt no
  tiene ese límite (2000 palabras). **Cuenta SIEMPRE los caracteres antes de entregar** un
  texto para pegar.
- **Contact Info solo llena campos VACÍOS** y extrae de lo que dice LA PERSONA. No
  sobreescribe ni corrige. Los bots NO pueden escribir en dropdowns (SINGLE_OPTIONS):
  usa campos de texto "gemelos" + workflow normalizador al dropdown real.
- **El "Ejemplo de Salida" es el molde del VALOR guardado**, no de lo que dice el lead:
  ponlo con el nombre oficial y bien escrito.
- **Las descripciones de captura deben cubrir TODOS los casos.** Una descripción anclada
  en un área ("guarda Melamina o Drywall") hace que el modelo no escriba nada con cursos
  de otra área. Ante la duda el modelo se abstiene (que es lo que se le pide).
- **Un Transfer Bot con condición agresiva ("apenas identifiques la familia") roba el
  primer turno**: el bot original no ejecuta sus capturas y el dato clave no se escribe —
  a veces sí, a veces no (LLM = ruleta). Si una automatización depende de la captura del
  primer turno, las condiciones de Transfer deben prohibir transferir en el primer mensaje.
- **Transfer Bot reasigna Y ACTIVA el bot destino** — puede despertar una conversación
  que un workflow ya había silenciado.
- Prompts largos = bots desobedientes. Un prompt de ~500 palabras con prohibiciones claras
  obedece mejor que uno de 1,200.
- **Implementar/Canales**: solo UN agente puede reclamar un canal+número; el conflicto se
  resuelve con filtros de etiqueta complementarios ("Has tags: X" en uno, "Doesn't have
  tags: X" en el otro). Es la base del aislamiento de pruebas.
- KB "subida" ≠ KB "asociada al bot" (dos pasos). Reemplaza el archivo, no lo dupliques.

## 6 · Arquitectura probada: "secuencia de ficha"

Patrón validado E2E (texto + 4 imágenes + PDF + activación de bots):

```
Lead escribe → bot router responde UNA línea y captura Curso (Contact Info)
→ trigger contact_changed(Curso) dispara el workflow de secuencia:
   guarda de entrada (salir si marcador presente o curso vacío)
   → árbol por curso → [pausar bot · apertura · (wait 3s · media)×N · pregunta final
                        · tag marcador · activar bot especialista]
→ el lead responde → el bot especialista captura el dato final (sede/modalidad)
→ workflows derivados (normalizadores) completan → workflow de calificación
   (guarda por datos completos + reingreso) califica, asigna y silencia.
```

Claves del patrón: el marcador va DESPUÉS del envío; el workflow de limpieza por cambio de
familia debe QUITAR el marcador; los triggers de datos redundantes (sede/modalidad) se
eliminan para evitar dobles envíos por carrera; ramas "atrapadoras" para cursos cuyo nombre
contiene el de otro (p.ej. "Supervisión de Melamina" contiene "melamina").

Los mensajes free-form NO necesitan plantillas WABA mientras el lead inicie la conversación
(sesión de 24h). Las plantillas solo hacen falta para mensajes iniciados por la empresa.

## 7 · Protocolo de pruebas sin ensuciar producción

- **1 prueba = 1 contacto nuevo.** Crear el contacto CON sus etiquetas ANTES de escribir
  (los triggers evalúan la etiqueta en el momento del mensaje).
- Aislamiento por etiquetas: una etiqueta-llave que abre los flujos nuevos (filtro en el
  trigger de entrada y en los canales del bot) + una etiqueta de exclusión para los flujos
  heredados del cliente.
- Verificar por API, nunca por el panel del contacto (cachea). El registro de auditoría
  ("ojito") muestra las escrituras reales de campos.
- El Registro de ejecución solo pinta el trigger por donde entró y no renderiza todos los
  dropdowns: audita la configuración desde el Creador, no desde el registro.
- Round Robin marca error si el contacto ya tiene dueño (en pruebas se asigna a mano) —
  en producción no pasa.

## 8 · Reglas de proyecto que evitan desastres

- **Reconstrucción total = todo aditivo**: lo heredado del cliente no se edita ni se
  reutiliza; se archiva al final.
- Workflows nuevos SIEMPRE como draft hasta revisión humana (y ojo con el gotcha del
  `active:true` que publica).
- Nada de URLs hardcodeadas de contenido en workflows definitivos: custom values.
- Documenta cada decisión y cada bug en un archivo de acuerdos con fecha; lleva un
  PENDIENTES.md vivo de quién debe qué. La info del cliente se contradice entre fuentes
  (texto vs imagen vs plataforma): registra la inconsistencia, decide una política
  ("la ficha manda") y no la re-litigues.
- El `.env` (PIT + location + token Firebase) NUNCA se commitea.
