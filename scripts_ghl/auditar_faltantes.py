"""Audita qué existe en la subcuenta vs qué necesitan los bots y workflows."""
import os, sys, pathlib
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
LOC=os.environ["GHL_LOCATION_ID"]

cf=api.get(f"/locations/{LOC}/customFields").get("customFields",[])
print(f"=== CUSTOM FIELDS: {len(cf)} ===")
folders={"R5Aa0kU4gDXkMAlQJUJp":"Identificación","LMLDqpaeMoec2OEeBkyb":"Calificación",
         "bCbLvp8svNbdSyOrZjPQ":"Pago","ZUUUGDgRxbcKyWfdA5yo":"Post-venta"}
for f in sorted(cf,key=lambda x:(folders.get(x.get('parentId'),'zz-HEREDADO'),x['name'])):
    fold=folders.get(f.get('parentId'),'HEREDADO')
    opts=f.get('picklistOptions') or []
    print(f"  [{fold:<14}] {f['fieldKey']:<40} {f['dataType']:<15} {opts if opts else ''}")

cv=api.get(f"/locations/{LOC}/customValues").get("customValues",[])
print(f"\n=== CUSTOM VALUES: {len(cv)} ===")
for v in cv:
    val=v.get('value') or '(vacío)'
    print(f"  {v['name']:<48} = {val[:40]}")

tags=api.get(f"/locations/{LOC}/tags").get("tags",[])
print(f"\n=== TAGS: {len(tags)} ===")
names=sorted(t['name'] for t in tags)
print("  ", names)

# --- lo que NECESITAN bots y workflows ---
NEED_TAGS=["enviar-ficha","lead-calificado","bot-silenciado","recuperacion-enviada",
           "alumno-activo","reintento-60d","origen-meta","matriculado",
           "perdido-precio","perdido-solo-informacion","perdido-ya-se-matriculo",
           "perdido-no-responde","perdido-horario-sede","perdido-sin-presupuesto","perdido-otro"]
have={n.lower() for n in names}
print(f"\n=== TAGS QUE FALTAN ({sum(1 for t in NEED_TAGS if t not in have)}) ===")
for t in NEED_TAGS:
    if t not in have: print("  FALTA:", t)

NEED_CV=["Yape - Número","Plin - Número","Link de pago con tarjeta",
         "Dirección sede Surco","Dirección sede Los Olivos","Dirección sede Arequipa",
         "Link Zoom clases online","Link reseña Google Surco","Link reseña Google Los Olivos",
         "Link reseña Google Arequipa","Link grupo WhatsApp","Link encuesta satisfacción"]
havecv={v['name'].strip().lower() for v in cv}
print(f"\n=== CUSTOM VALUES OPERATIVOS QUE FALTAN ({sum(1 for n in NEED_CV if n.lower() not in havecv)}) ===")
for n in NEED_CV:
    if n.lower() not in havecv: print("  FALTA:", n)
