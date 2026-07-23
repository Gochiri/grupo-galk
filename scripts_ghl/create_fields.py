"""SETUP-03: create the NEW custom fields (contact model) via GHL public API.
Idempotent (skips names that already exist). Additive. Folder assignment is
done in a later step (public API can't target UI-created folders)."""
import os, sys, json, time, pathlib, requests
ROOT=pathlib.Path("/home/user/grupo-galk")
for l in (ROOT/".env").read_text().splitlines():
    l=l.strip()
    if l and not l.startswith("#") and "=" in l:
        k,v=l.split("=",1); os.environ.setdefault(k.strip(),v.strip())
sys.path.insert(0,str(ROOT))
from cli_anything.gohighlevel.utils import ghl_client as api
LOC=os.environ["GHL_LOCATION_ID"]
h=api._headers(path=f"/locations/{LOC}/customFields")
BASE="https://services.leadconnectorhq.com"

# (folder_label, name, dataType, options)
FIELDS=[
 ("Identificación del lead","Familia de interés","SINGLE_OPTIONS",["Talleres","Software","Gestion"]),
 ("Identificación del lead","Curso de interés","TEXT",None),
 ("Identificación del lead","Fuente","SINGLE_OPTIONS",["Meta Ads","Manual","Referido","Reactivación"]),
 ("Identificación del lead","Fecha de primer contacto","DATE",None),
 ("Identificación del lead","UTM Source","TEXT",None),
 ("Identificación del lead","UTM Medium","TEXT",None),
 ("Identificación del lead","UTM Campaign","TEXT",None),
 ("Identificación del lead","Anuncio (Ad Name)","TEXT",None),
 ("Identificación del lead","Ad ID","TEXT",None),
 ("Calificación","Sede","SINGLE_OPTIONS",["Surco","Los Olivos","Arequipa","No aplica"]),
 ("Calificación","Horario de interés","TEXT",None),
 ("Calificación","Calificado","SINGLE_OPTIONS",["Sí","No"]),
 ("Calificación","Fecha de calificación","DATE",None),
 ("Calificación","Asesor asignado (nuevo)","TEXT",None),
 ("Calificación","Fecha de asignación","DATE",None),
 ("Calificación","Pack x2","SINGLE_OPTIONS",["Sí","No"]),
 ("Pago y matrícula","Precio cotizado","NUMERICAL",None),
 ("Pago y matrícula","Comprobante recibido","SINGLE_OPTIONS",["Sí","No"]),
 ("Pago y matrícula","Comprobante validado","SINGLE_OPTIONS",["Sí","No"]),
 ("Pago y matrícula","Validado por","TEXT",None),
 ("Pago y matrícula","Fecha de validación","DATE",None),
 ("Pago y matrícula","Fecha de inicio","DATE",None),
 ("Pago y matrícula","Grupo WhatsApp asignado","TEXT",None),
 ("Post-venta","Nota encuesta (1-5)","NUMERICAL",None),
 ("Post-venta","Fecha fin de taller","DATE",None),
 ("Post-venta","Razón de pérdida","SINGLE_OPTIONS",
    ["Precio","Solo información","Ya se matriculó en otro lugar","No responde",
     "Horario/sede no disponible","Sin presupuesto ahora","Otro"]),
]

existing={f["name"].strip().lower() for f in api.get(f"/locations/{LOC}/customFields").get("customFields",[])}
results=[]
for folder,name,dtype,opts in FIELDS:
    if name.strip().lower() in existing:
        results.append((folder,name,"SKIP(existe)","")); continue
    body={"name":name,"dataType":dtype,"model":"contact"}
    if opts: body["options"]=opts
    try:
        r=requests.post(f"{BASE}/locations/{LOC}/customFields", headers=h, json=body, timeout=30)
        if r.status_code in (200,201):
            cf=r.json().get("customField",{})
            results.append((folder,name,"OK",cf.get("fieldKey","")))
        else:
            msg=r.json().get("message") or r.text
            results.append((folder,name,f"ERR {r.status_code}",str(msg)[:80]))
    except Exception as e:
        results.append((folder,name,"EXC",str(e)[:80]))
    time.sleep(0.25)

print(f"{'CARPETA':<24} {'CAMPO':<28} {'ESTADO':<14} KEY/NOTA")
for folder,name,status,key in results:
    print(f"{folder:<24} {name:<28} {status:<14} {key}")
ok=sum(1 for *_,s,_ in [(r) for r in results] if False)  # placeholder
n_ok=sum(1 for r in results if r[2]=="OK")
n_skip=sum(1 for r in results if r[2].startswith("SKIP"))
n_err=len(results)-n_ok-n_skip
print(f"\nOK={n_ok}  SKIP={n_skip}  ERR={n_err}  (+ Modalidad ya creada antes = {n_ok+1+n_skip} nuevos totales)")
