"""SP06 deja de depender de que el bot decida cuándo entrar.

EL PROBLEMA (prueba del 15-ago, contacto sY28puGtTWNbotsatp6j)
--------------------------------------------------------------
La única puerta viva de SP06 era la acción *Trigger a Workflow* del bot. Y el bot la
dispara **en el mismo turno** en que la acción *Contact Info* extrae los datos, así que
llega antes de que el campo se escriba. Con la guarda puesta, SP06 entra, ve `Sede` todavía
vacía, corta y se acaba. Segundos después la sede sí se guarda — pero ya no hay nadie que
vuelva a intentarlo.

Resultado: los 3 campos quedan completos, `Calificado` vacío, sin asesor y sin oportunidad
movida. **El lead se pierde en silencio.** La guarda hizo lo correcto; lo que falta es el
reintento.

LA SOLUCIÓN
-----------
Que SP06 entre por los datos y no por la opinión del bot. Se le agregan tres triggers
`contact_changed`, uno por cada campo canónico. Así el último dato en llegar es el que
enrola al contacto, y para entonces los tres ya existen.

La guarda pasa a ser lo que sostiene todo el diseño:
  · si el campo que cambió no era el último, faltan datos → corta, sin efecto
  · cuando llega el último, los tres están → califica
  · cualquier cambio posterior encuentra `Calificado` con valor → corta

Por eso los reintentos son gratis: entrar de más no cuesta nada.

FALTAN DOS COSAS DE UI, SIN ELLAS ESTO NO SIRVE
-----------------------------------------------
1. **Activar el reingreso** en SP06 → Configuración. Si un contacto solo puede entrar una
   vez, el primer campo que cambie lo gasta y los otros dos ya no lo enrolan.
2. **Quitar la acción "Marcar lead calificado" del bot.** Es la que compite con los
   triggers y la que mete la carrera. Quitarla ANTES de que existan estos triggers deja a
   SP06 sin puerta de entrada, así que el orden importa: primero esto, después la UI.
"""
import sys, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC

WID = "84811c16-30d8-4c08-a05d-0c12fa46567d"
CAMPOS = ["contact.curso_de_inters", "contact.modalidad", "contact.sede"]


def main():
    d = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    tpl = (d.get("workflowData") or {}).get("templates") or []
    head = next((n["id"] for n in tpl if n.get("nodeType") == "condition-node"), None)
    if not head:
        sys.exit("ABORT: no encontré el nodo de entrada de SP06")
    print(f"SP06 {d.get('status')} · entrada = {head[:8]}")

    ya = C.request("GET", f"/workflow/{LOC}/trigger?workflowId={WID}") or []
    puestos = {str(c.get("field")).split(".")[-1]
               for t in ya for c in (t.get("conditions") or [])}

    for k in CAMPOS:
        fid, titulo = wf_lib.FID(k), wf_lib.TITLE(k)
        if fid in puestos:                                   # idempotencia (§3)
            print(f"  SKIP  {titulo} — ya tenía trigger")
            continue
        tipo = "select" if wf_lib._cf[k]["dataType"] == "SINGLE_OPTIONS" else "text"
        C.request("POST", f"/workflow/{LOC}/trigger", {
            "status": d.get("status"), "workflowId": WID, "schedule_config": {},
            "conditions": [{"operator": "has-changed", "field": fid,
                            "title": titulo, "type": tipo}],
            "type": "contact_changed", "masterType": "highlevel",
            "name": f"{titulo} cambió", "allowMultiple": "yes",
            "actions": [{"workflow_id": WID, "type": "add_to_workflow"}],
            # SP06 ya está publicado; active=True aquí no lo publica de nuevo.
            "active": True, "triggersChanged": True, "location_id": LOC,
            "targetActionId": head,
            "advanceCanvasMeta": {"position": {"x": 57.5, "y": -73}}})
        print(f"  +     {titulo}")

    v = C.request("GET", f"/workflow/{LOC}/{WID}") or {}
    print(f"\nVERIFY: SP06 {v.get('status')} · triggers:")
    for t in C.request("GET", f"/workflow/{LOC}/trigger?workflowId={WID}") or []:
        tgt = t.get("targetActionId")
        print(f"   [{t.get('type'):16}] {str(t.get('name')):26} active={t.get('active')} "
              f"entrada={'OK' if tgt == head else 'ROTA ' + str(tgt)[:8]}")


if __name__ == "__main__":
    main()
