"""Cambia entre el flujo DEMO (asesor da horarios) y el ORIGINAL (bot manda ficha).

    .venv/bin/python scripts_ghl/toggle_flujo.py demo      # 3 datos, asesor da horarios
    .venv/bin/python scripts_ghl/toggle_flujo.py original  # 4 datos, bot manda ficha

Solo toca lo que se puede tocar por API:
  · el texto de la notificación de SP06 al asesor
  · el bloque "## Horarios" de las 3 Knowledge Base

Lo demás es UI y va a mano (prompts, acción Contact Info, publicar SP05).
Ver `ROLLBACK-flujo-ficha.md` para la lista completa.
"""
import sys, re, pathlib

ROOT = pathlib.Path("/home/user/grupo-galk")
sys.path.insert(0, str(ROOT / "scripts_ghl"))
import wf_lib
from wf_lib import C, LOC

SP06 = "84811c16-30d8-4c08-a05d-0c12fa46567d"

NOTIF = {
    "demo": ("🎯 Lead perfilado — pásale horarios",
             "Lead perfilado y listo para cerrar: {{contact.name}} ({{contact.phone}})\n"
             "📚 {{contact.curso_de_inters}} · {{contact.modalidad}} · {{contact.sede}}\n"
             "Vino de: {{contact.fuente}}\n\n"
             "Entra a la conversación y pásale los horarios y fechas disponibles de su sede. "
             "Ya viene perfilado: no le preguntes de nuevo qué curso quiere."),
    "original": ("🎯 Lead calificado asignado",
                 "Nuevo lead calificado asignado: {{contact.name}} ({{contact.phone}}) — "
                 "{{contact.curso_de_inters}} / {{contact.sede}} / {{contact.horario_de_inters}}"),
}

HORARIOS = {
    "demo": ("Los horarios, las fechas de inicio y los cupos **te los da tu asesor**. No están en esta "
             "base de conocimiento y cambian, así que **nunca inventes ni prometas un horario, una "
             "fecha de inicio ni un cupo disponible**.\n\nSi la persona pregunta por horarios o fechas, "
             "dile que un asesor se los pasa enseguida con las opciones de su sede, y sigue con lo tuyo: "
             "confirmar **curso, modalidad y sede**. Con esos tres datos ya puedes pasarlo al asesor."),
    "original": ("Los horarios y las fechas de inicio **cambian cada semana y NO están en esta base de "
                 "conocimiento**. Al lead se le envía una ficha con los horarios actualizados de su sede. "
                 "Tu trabajo es preguntarle cuál de esos horarios le acomoda, **nunca inventar uno**."),
}

KBS = ["knowledge-base/KB-BOT-01-talleres.md",
       "knowledge-base/KB-BOT-02-software.md",
       "knowledge-base/KB-BOT-03-gestion.md"]


def main(modo):
    titulo, cuerpo = NOTIF[modo]
    d = C.request("GET", f"/workflow/{LOC}/{SP06}")
    tpl = (d.get("workflowData") or {}).get("templates") or []
    for n in tpl:
        if n["type"] == "internal_notification" and \
           n["attributes"]["notification"].get("userType") == "assigned_user":
            n["attributes"]["notification"].update({"title": titulo, "body": cuerpo})
    r = C.request("PUT", f"/workflow/{LOC}/{SP06}",
                  {"name": d["name"], "version": d["version"], "parentId": d.get("parentId"),
                   "status": "draft", "workflowData": {"templates": tpl}})
    print("SP06 notificación:", "OK" if r and not r.get("_error") else r)

    for p in KBS:
        f = ROOT / p
        t = f.read_text()
        nuevo = re.sub(r"(## Horarios\n\n).*?(\n\n---)", r"\1" + HORARIOS[modo] + r"\2", t, flags=re.S)
        f.write_text(nuevo)
        print(f"  {p}: {'OK' if HORARIOS[modo][:40] in nuevo else 'NO CAMBIÓ'}")

    print(f"\nModo '{modo}' aplicado. Falta lo de UI — ver ROLLBACK-flujo-ficha.md")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else ""
    if modo not in ("demo", "original"):
        sys.exit(__doc__)
    main(modo)
