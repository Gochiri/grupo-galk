"""SP06 deja de confiar en quien lo llama.

QUÉ PASÓ (15-ago, contacto x6H97utgqcqKL7tlbzcR)
------------------------------------------------
BOT-01 tiene una acción *Trigger a Workflow* llamada "Marcar lead calificado", con esta
condición de inicio escrita a mano:

    "Cuando ya tengas guardados los tres datos: curso, modalidad y sede. No antes.
     Si falta alguno, no ejecutes: sigue conversando hasta completarlos."

El bot la ejecutó igual, con los tres campos VACÍOS. Y es esperable: esa condición no es
una validación, es una frase que interpreta el modelo. El bot creía tener los datos porque
él mismo los había dicho en su texto — pero *Contact Info* extrae de lo que dice la
persona, no de lo que escribe el bot, así que nunca se guardó nada.

Además la acción usa `add_to_workflow`, o sea que **entra por la puerta de atrás**: se
salta el trigger de SP06 (`Tag Added: galk-bot-calificado`) por completo.

POR QUÉ NO HUBO DAÑO ESTA VEZ
-----------------------------
De pura casualidad. SP06 arranca con un if/else que corta si el contacto **ya tiene
asesor**, y los workflows viejos de Francisco (WF2 Round Robin) ya le habían puesto uno a
las 10:09. Se cumplió la rama y SP06 murió ahí. Prueba: `Calificado` quedó vacío, y ese es
el primer nodo de la rama buena, antes de un wait de 5 segundos.

En un contacto limpio, etiquetado `equipo-interno` y sin los workflows viejos encima, esa
guarda NO se cumple y SP06 corre entero: marca Calificado = Sí, crea la oportunidad, la
mueve a Asignado, notifica al asesor y **silencia al bot**. Un lead sin curso, sin sede y
sin modalidad aterrizando en la bandeja de un vendedor, con el bot mudo.

EL ARREGLO
----------
La misma guarda de arriba pasa de `and` a `or` y se le suman los tres campos. Queda:

    NO calificar si:  ya tiene asesor
                  O   Curso de interés está vacío
                  O   Modalidad está vacía
                  O   Sede está vacía

Cero cambios de estructura: se tocan las condiciones de un if/else que ya existe. Los 18
nodos y el árbol quedan igual.

Se comprueban los campos **canónicos** (`Curso de interés`, `Modalidad`, `Sede`), no los
gemelos de texto que llena el bot. Así la guarda también verifica que WF-NORM y WF-MOD ya
hicieron su parte antes de dar el lead por bueno.
"""
import sys, json, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC, nid

WID = "84811c16-30d8-4c08-a05d-0c12fa46567d"
RAMA = "No calificar (ya asignado o faltan datos)"

# Canónicos, no los gemelos de texto del bot.
REQUERIDOS = ["contact.curso_de_inters", "contact.modalidad", "contact.sede"]


def cond_vacio(field_key):
    """has_no_value va SIN conditionValue. Verificado en WF1 de Francisco y en LS01/SP05."""
    return {"conditionType": "contact_detail", "conditionSubType": wf_lib.FID(field_key),
            "conditionOperator": "has_no_value", "__conditionId": nid(), "ifElseNodeId": "",
            "__customFieldType__": "standard", "isWait": False,
            "nestedDropdownTypes": wf_lib.NESTED, "allowIsOperatorTypes": wf_lib.ALLOWIS}


def main():
    d = C.request("GET", f"/workflow/{LOC}/{WID}")
    if not d or d.get("_error"):
        sys.exit(f"ABORT: no pude leer SP06 -> {d}")
    tpl = (d.get("workflowData") or {}).get("templates") or []
    estado = d.get("status")
    print(f"SP06: {len(tpl)} nodos · status={estado}")

    # El primer condition-node es la guarda de entrada.
    head = next((n for n in tpl if n.get("nodeType") == "condition-node"), None)
    if not head:
        sys.exit("ABORT: no encontré el if/else de entrada, no invento la estructura")
    brs = (head.get("attributes") or {}).get("branches") or []
    if len(brs) != 1:
        sys.exit(f"ABORT: esperaba 1 rama en la guarda, hay {len(brs)}. Revisar a mano.")

    seg = brs[0]["segments"][0]
    ya = {c.get("conditionSubType") for c in seg["conditions"]}
    if "assigned_to" not in ya:
        sys.exit("ABORT: la guarda no es la de 'ya tiene asesor'. Revisar a mano.")

    nuevas = [cond_vacio(k) for k in REQUERIDOS if wf_lib.FID(k) not in ya]
    if not nuevas:
        print("Ya estaba puesta la guarda de los 3 campos. Nada que hacer (idempotencia §3).")
        return

    seg["operator"] = "or"          # ya-asignado O falta-curso O falta-modalidad O falta-sede
    seg["conditions"].extend(nuevas)
    brs[0]["name"] = RAMA
    brs[0]["operator"] = "or"

    r = C.request("PUT", f"/workflow/{LOC}/{WID}",
                  {"name": d.get("name"), "version": d.get("version"),
                   "parentId": d.get("parentId"),
                   "status": estado,                 # se respeta como estaba, no se despublica
                   "workflowData": {"templates": tpl}})
    print("PUT:", "OK" if r and not r.get("_error") else r)

    v = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    vt = (v.get("workflowData") or {}).get("templates") or []
    vh = next(n for n in vt if n.get("nodeType") == "condition-node")
    vs = vh["attributes"]["branches"][0]["segments"][0]
    byid = {f["id"]: f["name"] for f in wf_lib._cf.values()}
    print(f"VERIFY: {len(vt)} nodos · status={v.get('status')}")
    print(f"  rama '{vh['attributes']['branches'][0]['name']}'  (operador: {vs['operator']})")
    for c in vs["conditions"]:
        st = c.get("conditionSubType")
        print(f"    · {byid.get(st, st)} {c.get('conditionOperator')}")


if __name__ == "__main__":
    main()
