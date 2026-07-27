"""AP01-AP04 y PS01-PS03. Todos DRAFT."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path("/home/user/grupo-galk/scripts_ghl")))
from wf_lib import *

res=[]
CV={"surco":"{{custom_values.direccin_sede_surco}}","olivos":"{{custom_values.direccin_sede_los_olivos}}",
    "arequipa":"{{custom_values.direccin_sede_arequipa}}","zoom":"{{custom_values.link_zoom_clases_online}}",
    "grupo":"{{custom_values.link_grupo_whatsapp}}","encuesta":"{{custom_values.link_encuesta_satisfaccin}}",
    "g_surco":"{{custom_values.link_resea_google_surco}}","g_olivos":"{{custom_values.link_resea_google_los_olivos}}",
    "g_arequipa":"{{custom_values.link_resea_google_arequipa}}"}

# ---------- AP01 | Confirmación de matrícula ----------
base=("[PLANTILLA galk_confirmacion_matricula] ¡Bienvenido {{contact.first_name}}! 🎉 "
      "Ya estás matriculado en *{{contact.curso_de_inters}}*.\n"
      "📅 Inicio: {{contact.fecha_de_inicio}}\n🕐 Horario: {{contact.horario_de_inters}}\n")
ramas=[]
for nombre, key, extra in [("Surco","Surco",f"📍 Dirección: {CV['surco']}"),
                           ("Los Olivos","Olivos",f"📍 Dirección: {CV['olivos']}"),
                           ("Arequipa","Arequipa",f"📍 Dirección: {CV['arequipa']}")]:
    ramas.append((f"Presencial {nombre}", [cond_field("contact.sede", key)],
                  [ n_wa(nid(), base+extra+"\n\n¡Nos vemos! 🙌", name=f"Confirmación {nombre}") ]))
t=arbol(ramas, none_next=[ n_wa(nid(), base+f"💻 Link de Zoom: {CV['zoom']}\n\n¡Nos vemos! 🙌", name="Confirmación Online") ])
res.append(("AP01 | Confirmación de matrícula",)+crear("AP01 | Confirmación de matrícula","GALK 2.0 · 06 Post-venta",t))

# ---------- AP02 | Recordatorios T-48 y T-24 ----------
w1,m1,w2,m2 = nid(), nid(), nid(), nid()
rec=("[PLANTILLA galk_recordatorio_taller] ¡Hola {{contact.first_name}}! ⏰ Te recordamos que "
     "*{{contact.curso_de_inters}}* inicia el {{contact.fecha_de_inicio}} — {{contact.horario_de_inters}}. ")
t=[
 n_wait(w1, 1, "days", nxt=m1),
 n_wa(m1, rec+"Faltan 2 días 🙌", nxt=w2, name="Recordatorio T-48h"),
 n_wait(w2, 1, "days", nxt=m2),
 n_wa(m2, rec+"¡Es mañana! 🎒 No olvides llegar 10 min antes.", name="Recordatorio T-24h"),
]
res.append(("AP02 | Recordatorios T-48/T-24",)+crear("AP02 | Recordatorios de inicio (T-48 y T-24)","GALK 2.0 · 06 Post-venta",t))

# ---------- AP03 | Alta en grupo privado ----------
w3,nt3 = nid(), nid()
t=[
 n_wait(w3, 1, "days", nxt=nt3),
 n_notif(nt3, "👥 Alta en grupo privado",
         "Agregar a {{contact.name}} ({{contact.phone}}) al grupo de WhatsApp de {{contact.curso_de_inters}}. "
         f"Link: {CV['grupo']} — al terminar, completar el campo 'Grupo WhatsApp asignado'.",
         usuario=SUPERVISORA, tipo_user="user"),
]
res.append(("AP03 | Alta en grupo privado",)+crear("AP03 | Alta en grupo privado de WhatsApp","GALK 2.0 · 06 Post-venta",t))

# ---------- AP04 | Aviso de reprogramación ----------
wa4=nid()
t=arbol(
  ramas=[("Alumno activo", [cond_tag("alumno-activo")],
          [ n_wa(wa4,"[PLANTILLA galk_aviso_reprogramacion] Hola {{contact.first_name}} 👋 "
                     "Te avisamos que *{{contact.curso_de_inters}}* cambió de fecha. "
                     "Nueva fecha de inicio: {{contact.fecha_de_inicio}} — {{contact.horario_de_inters}}. "
                     "Cualquier duda, escríbenos por aquí 🙌", name="Aviso reprogramación") ])])
res.append(("AP04 | Aviso de reprogramación",)+crear("AP04 | Aviso de reprogramación","GALK 2.0 · 06 Post-venta",t))

# ---------- PS01 | Encuesta de satisfacción ----------
w5,m5 = nid(), nid()
t=[
 n_wait(w5, 2, "days", nxt=m5),
 n_wa(m5, "¡Hola {{contact.first_name}}! 😊 ¿Cómo te fue en *{{contact.curso_de_inters}}*? "
          f"Cuéntanos en 1 minuto 👉 {CV['encuesta']}\nTu opinión nos ayuda un montón 🙌", name="Enviar encuesta"),
]
res.append(("PS01 | Encuesta de satisfacción",)+crear("PS01 | Encuesta de satisfacción","GALK 2.0 · 07 Reviews y Recompra",t))

# ---------- PS01-B | Reseña Google según nota ----------
ramas=[]
for nombre, key, link in [("Surco","Surco",CV['g_surco']),("Los Olivos","Olivos",CV['g_olivos']),
                          ("Arequipa","Arequipa",CV['g_arequipa'])]:
    ramas.append((f"Nota alta · {nombre}", [cond_field("contact.nota_encuesta_15","4"), cond_field("contact.sede",key)],
                  [ n_wa(nid(), f"¡Gracias por tu nota {{{{contact.nota_encuesta_15}}}}! ⭐ "
                                f"¿Nos dejarías una reseña? Nos ayuda muchísimo 🙏\n👉 {link}", name=f"Reseña {nombre}") ]))
nt5=nid()
t=arbol(ramas, none_next=[ n_notif(nt5,"⚠️ Encuesta con nota baja",
        "{{contact.name}} calificó con {{contact.nota_encuesta_15}} el curso {{contact.curso_de_inters}}. Contactar.",
        usuario=SUPERVISORA, tipo_user="user") ])
res.append(("PS01-B | Reseña o alerta",)+crear("PS01-B | Reseña Google o alerta por nota baja","GALK 2.0 · 07 Reviews y Recompra",t))

# ---------- PS02 | Venta cruzada ----------
w6=nid(); ramas=[]
for fam, curso, oferta in [("Melamina","Melamina Desde Cero","Melamina Avanzado"),
                           ("Drywall","Drywall Desde Cero","Drywall Avanzado")]:
    ramas.append((f"{fam} Desde Cero", [cond_field("contact.curso_de_inters", curso)],
                  [ n_wa(nid(), f"¡Hola {{{{contact.first_name}}}}! 🙌 Ya que llevaste *{curso}*, "
                                f"¿te animas con *{oferta}*? Es el siguiente nivel y te da el paquete completo 💪 "
                                "¿Te paso los detalles?", name=f"Oferta {oferta}") ]))
t=arbol(ramas)
res.append(("PS02 | Venta cruzada",)+crear("PS02 | Venta cruzada · Desde Cero → Avanzado","GALK 2.0 · 07 Reviews y Recompra",t))

# ---------- PS03 | Reintento de perdidos a 60 días ----------
w7,wa7 = nid(), nid()
t=arbol(
  ramas=[("Ya se matriculó en otro lado → STOP", [cond_tag("perdido-ya-se-matriculo")], [])],
  none_next=[ n_wait(w7, 60, "days", nxt=wa7),
              n_wa(wa7, "[PLANTILLA galk_reactivacion_frio] ¡Hola {{contact.first_name}}! 👋 "
                        "Pasó un tiempo desde tu consulta por *{{contact.curso_de_inters}}*. "
                        "Tenemos nuevas fechas y promociones 🎉 ¿Le damos una segunda mirada?",
                   name="Reintento a 60 días") ])
res.append(("PS03 | Reintento perdidos 60d",)+crear("PS03 | Reintento de perdidos a 60 días","GALK 2.0 · 07 Reviews y Recompra",t,
            tag_trigger="reintento-60d", trigger_name="Reintento 60 días"))

for r in res: print(f"  {r[0]:<38} {r[2]}   id={r[1]}")
