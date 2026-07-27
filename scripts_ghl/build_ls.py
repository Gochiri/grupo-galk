"""LS01, LS02, LS03 — Lead Sources. Todos DRAFT."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path("/home/user/grupo-galk/scripts_ghl")))
from wf_lib import *

res=[]

# ---------- LS01 | Captura Meta CTWA ----------
a,b,c_,d = nid(), nid(), nid(), nid()
t=[
 n_update(a,[("contact.fuente","Meta Ads"),
             ("contact.fecha_de_primer_contacto","{{right_now}}")], nxt=b, name="Fuente + fecha primer contacto"),
 n_update(b,[("contact.utm_source","{{contact.attributionSource.utmSource}}"),
             ("contact.utm_medium","{{contact.attributionSource.medium}}"),
             ("contact.utm_campaign","{{contact.attributionSource.campaign}}"),
             ("contact.anuncio_ad_name","{{contact.attributionSource.adName}}"),
             ("contact.ad_id","{{contact.attributionSource.adId}}")], nxt=c_, name="Atribución Meta (5 campos)"),
 n_tag(c_, ["origen-meta"], nxt=d),
 n_opp(d, ST["nuevo"], name="Crear oportunidad → Nuevo Lead"),
]
res.append(("LS01 | Captura Meta CTWA",)+crear("LS01 | Captura Meta CTWA","GALK 2.0 · 03 Lead Sources",t))

# ---------- LS02 | Alta manual / referido ----------
u1,o1 = nid(), nid()
t=arbol(
  ramas=[("Ya vino de Meta → no tocar", [cond_tag("origen-meta")], [])],
  none_next=[ n_update(u1,[("contact.fuente","Manual"),
                           ("contact.fecha_de_primer_contacto","{{right_now}}")], nxt=o1, name="Fuente = Manual"),
              n_opp(o1, ST["nuevo"], name="Crear oportunidad → Nuevo Lead") ])
res.append(("LS02 | Alta manual / referido",)+crear("LS02 | Alta manual / referido","GALK 2.0 · 03 Lead Sources",t))

# ---------- LS03 | Reactivación base histórica (FASE 6) ----------
w1,g1,t1 = nid(), nid(), nid()
t=[
 n_wa(w1,"[PLANTILLA galk_reactivacion_frio] Hola {{contact.first_name}} 👋 Somos Grupo GALK. "
        "Tenemos nuevas fechas y promociones en nuestros talleres y cursos. ¿Te interesa que te cuente? 😊", nxt=g1),
 n_wait(g1, 5, "days", nxt=t1),
 n_tag(t1, ["recuperacion-enviada"]),
]
res.append(("LS03 | Reactivación base histórica",)+crear("LS03 | Reactivación base histórica (FASE 6 - NO ACTIVAR)","GALK 2.0 · 03 Lead Sources",t))

for r in res: print(f"  {r[0]:<45} {r[2]}   id={r[1]}")
