# Proyecto <CLIENTE> — contexto para Claude Code

> **Lee `PLAYBOOK-GHL.md` antes de tocar nada.** Ahí están todos los gotchas de GHL
> aprendidos en proyectos anteriores. Las formas de nodos validadas están en
> `gohighlevel/utils/wf_toolkit.py` — úsalas, no fabriques atributos.

## 1. Arranque de sesión

Necesitas el archivo `.env` en la raíz (NO está en git, contiene secretos):

```
GHL_API_KEY=pit-...                  # Private Integration Token
GHL_LOCATION_ID=<location>
GHL_FIREBASE_REFRESH_TOKEN=AMf-...   # token interno; si da 401, pedir uno nuevo
```

Los valores los tiene el usuario. Pídeselos si falta el `.env`.

## 2. Reglas al escribir en GHL

- **Subcuenta EN PRODUCCIÓN**: todo lo nuevo es aditivo; lo heredado del cliente no se
  edita ni se reutiliza.
- **Idempotencia obligatoria**: todo script verifica si ya existe y salta. Dry-run por
  defecto, `--aplicar` para escribir.
- **Workflows como DRAFT** hasta revisión humana. Ojo: `active:true` en el PUT de un
  trigger PUBLICA el workflow.
- **Después de cada PUT de workflow**: correr `verificar_triggers()` (targetActionId,
  active, formato doble de condiciones) y confirmar `allowMultiple` (el PUT lo resetea
  si no va en el body — `put_workflow()` lo maneja).
- **Textos para la UI de bots: contar caracteres SIEMPRE** (límite 500 en campos de
  acciones; el conteo se entrega junto al texto).
- **Nada de URLs de contenido hardcodeadas** en workflows definitivos: custom values.
- La verdad está en la API, no en el panel del contacto (cachea) ni en el Registro de
  ejecución (solo pinta el trigger de entrada).

## 3. Protocolo de pruebas

- 1 prueba = 1 contacto nuevo, creado CON etiquetas ANTES de escribir.
- Etiqueta-llave para los flujos nuevos: `<pruebas-tag>` (filtro en trigger de entrada y
  en los canales del bot). Etiqueta de exclusión para los flujos heredados: `<exclusion-tag>`.
- Aislamiento de canal WhatsApp: agente heredado con "Doesn't have tags: <pruebas-tag>",
  bot nuevo con "Has tags: <pruebas-tag>".

## 4. Gestión

- Registro vivo `PENDIENTES.md`: lo confirmado como hecho se tacha y no se vuelve a pedir.
- Acuerdos y bugs con fecha en `ACUERDOS-*.md`. Las inconsistencias en la info del cliente
  se registran con la política acordada (p. ej. "la ficha oficial manda") y no se re-litigan.
- Al mencionar un documento del repo, incluir el link directo.

## 5. IDs del proyecto (llenar conforme se construya)

| Qué | ID |
|---|---|
| Location | |
| Pipeline | |
| Bots (Conversation AI, de la URL) | |
| Workflows principales | |
| Campos custom clave | |
