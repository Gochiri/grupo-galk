"""SP08, SP09, SP10, SP11, SP12. Todos DRAFT."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path("/home/user/grupo-galk/scripts_ghl")))
from wf_lib import *

res=[]

# ---------- SP08 | Recuperación fuera de ventana ----------
w,t2 = nid(), nid()
t=arbol(
  ramas=[("Ya lo tomó un asesor → STOP", [cond_tag("bot-silenciado")], [])],
  none_next=[ n_wa(w,"[PLANTILLA galk_recuperacion_sin_respuesta] Hola {{contact.first_name}} 👋 "
                     "Te escribimos de Grupo GALK, quedó pendiente tu consulta sobre "
                     "{{contact.curso_de_inters}}. ¿Seguimos? 😊", nxt=t2),
              n_tag(t2, ["recuperacion-enviada"]) ])
res.append(("SP08 | Recuperación fuera de ventana",)+crear("SP08 | Recuperación fuera de ventana","GALK 2.0 · 04 Sales Pipeline",t))

# ---------- SP09 | Envío de datos de pago ----------
YAPE="{{custom_values.yape__nmero}}"; PLIN="{{custom_values.plin__nmero}}"; TARJ="{{custom_values.link_de_pago_con_tarjeta}}"
wa_pack, wa_std, op1, nt1 = nid(), nid(), nid(), nid()
msg_pack=("¡Perfecto {{contact.first_name}}! 🎉 Para el *Pack x2* (Desde Cero + Avanzado) el precio es *S/890* "
          f"y reservas tu cupo con *S/200* 🙌\n\n💳 *Medios de pago*\n📱 Yape: {YAPE}\n📱 Plin: {PLIN}\n"
          f"💳 Tarjeta: {TARJ}\n\nCuando hagas el pago, mándame la captura por aquí 📸")
msg_std=("¡Perfecto {{contact.first_name}}! 🎉 Para reservar tu cupo en *{{contact.curso_de_inters}}*:\n\n"
         f"💳 *Medios de pago*\n📱 Yape: {YAPE}\n📱 Plin: {PLIN}\n💳 Tarjeta: {TARJ}\n\n"
         "Cuando hagas el pago, mándame la captura por aquí 📸")
t=arbol(
  ramas=[("Pack x2 = Sí", [cond_field("contact.pack_x2","Sí")], [ n_wa(wa_pack, msg_pack, name="Datos de pago (pack)") ])],
  none_next=[ n_wa(wa_std, msg_std, nxt=op1, name="Datos de pago (estándar)"),
              n_opp(op1, ST["pago_enviado"], nxt=nt1, name="Oportunidad → Datos de pago enviados"),
              n_notif(nt1, "💰 Datos de pago enviados",
                      "Se enviaron los datos de pago a {{contact.name}} ({{contact.phone}}) — {{contact.curso_de_inters}}") ])
res.append(("SP09 | Envío de datos de pago",)+crear("SP09 | Envío de datos de pago","GALK 2.0 · 05 Pagos y Cierres",t))

# ---------- SP10 | Validación de pago (parte A) ----------
u,o,nt = nid(), nid(), nid()
t=[
 n_update(u,[("contact.comprobante_recibido","Sí")], nxt=o, name="Comprobante recibido = Sí"),
 n_opp(o, ST["pago_validacion"], nxt=nt, name="Oportunidad → Pago en validación"),
 n_notif(nt, "🧾 Comprobante por validar",
         "{{contact.name}} ({{contact.phone}}) envió comprobante de {{contact.curso_de_inters}}. Validar en la conversación.",
         usuario=SUPERVISORA, tipo_user="user"),
]
res.append(("SP10 | Validación de pago (A)",)+crear("SP10 | Validación de pago · comprobante recibido","GALK 2.0 · 05 Pagos y Cierres",t))

# ---------- SP10-B | Pago validado → Matriculado ----------
u2,o2 = nid(), nid()
t=[
 n_update(u2,[("contact.validado_por","{{user.name}}"),
              ("contact.fecha_de_validacin","{{right_now}}")], nxt=o2, name="Validado por + fecha"),
 n_opp(o2, ST["matriculado"], name="Oportunidad → Matriculado"),
]
res.append(("SP10-B | Pago validado",)+crear("SP10-B | Pago validado → Matriculado","GALK 2.0 · 05 Pagos y Cierres",t))

# ---------- SP11 | Cierre ganado ----------
o3,t3 = nid(), nid()
t=[
 n_opp(o3, ST["matriculado"], nxt=t3, status="won", name="Oportunidad → Won",
       extra={"monetary_value":"{{contact.precio_cotizado}}"}),
 n_tag(t3, ["matriculado","alumno-activo"]),
]
res.append(("SP11 | Cierre ganado",)+crear("SP11 | Cierre ganado (Won)","GALK 2.0 · 05 Pagos y Cierres",t))

# ---------- SP12 | Cierre perdido (7 razones) ----------
RAZONES=[("Precio","perdido-precio"),("Solo información","perdido-solo-informacion"),
         ("Ya se matriculó","perdido-ya-se-matriculo"),("No responde","perdido-no-responde"),
         ("Horario/sede","perdido-horario-sede"),("Sin presupuesto","perdido-sin-presupuesto"),("Otro","perdido-otro")]
ramas=[]
for etiqueta, tag in RAZONES:
    tg, op, rt = nid(), nid(), nid()
    ramas.append((f"Perdido: {etiqueta}", [cond_field("contact.razn_de_prdida", etiqueta)],
                  [ n_tag(tg,[tag], nxt=op),
                    n_opp(op, ST["perdido"], nxt=rt, status="lost", name="Oportunidad → Lost"),
                    n_tag(rt,["reintento-60d"]) ]))
nt2=nid()
t=arbol(ramas, none_next=[ n_notif(nt2,"⚠️ Cierre perdido sin razón",
        "La oportunidad de {{contact.name}} se marcó como perdida sin razón de pérdida. Completar el campo.",
        usuario=SUPERVISORA, tipo_user="user") ])
res.append(("SP12 | Cierre perdido",)+crear("SP12 | Cierre perdido (7 razones)","GALK 2.0 · 05 Pagos y Cierres",t))

for r in res: print(f"  {r[0]:<38} {r[2]}   id={r[1]}")
