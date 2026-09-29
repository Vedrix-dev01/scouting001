import json, glob, re, sys, os
from collections import Counter
from urllib.parse import urlparse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo
D = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[sys.argv.index("--out")+1] if "--out" in sys.argv else os.path.join(D,"Germany_Real_Estate_Social_Media_Prospects_200.xlsx")
COLS = ["Prospect Name","Company","First Name","Email","Country","State","City","Real Estate Business Type","Property Focus",
"Number or Evidence of Active Listings","Website","Instagram","Facebook","LinkedIn","YouTube","Buying Intent",
"Personalization Detail","Personalization Reason","Personalized Opening","Subject Line","Email Body","Source URL",
"Evidence","Evidence Type","Research Confidence","Lead Status","Send Status","Date Sent","Notes"]
STATES={"Baden-Württemberg","Bayern","Berlin","Brandenburg","Bremen","Hamburg","Hessen","Mecklenburg-Vorpommern","Niedersachsen",
"Nordrhein-Westfalen","Rheinland-Pfalz","Saarland","Sachsen","Sachsen-Anhalt","Schleswig-Holstein","Thüringen"}
BANNED=["garantiert","garantie","dringend","mehr umsatz","mehr leads","revolution","limited","urgent","100%","sofort handeln",
"jetzt zugreifen","exklusives angebot","nur heute"]
EXCL={}  # email -> reason (filled by curation)
if os.path.exists(os.path.join(D,"curation_de.py")):
    sys.path.insert(0,D); from curation_de import EXCLUDE as EXCL
EXCL={k.lower():v for k,v in EXCL.items()}
EM=re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
def dom(u): return urlparse(u if u.startswith("http") else "http://"+u).netloc.lower().replace("www.","")
def nco(s): return re.sub(r"[^a-z0-9]","",re.sub(r"\b(gmbh|co|kg|ug|haftungsbeschränkt|immobilien|e\.k\.|ek|ohg|gbr|ag|mbh)\b","",(s or "").lower()))
raw=[]
for f in sorted(glob.glob(os.path.join(D,"leads","*.jsonl"))):
    for l in open(f):
        l=l.strip()
        if l:
            r=json.loads(l); r["_f"]=os.path.basename(f); raw.append(r)
main=[];excl=[];dups=[];seen={}
for r in raw:
    r={k:(v.strip() if isinstance(v,str) else v) for k,v in r.items()}
    em=r.get("email","").lower(); probs=[]
    if not EM.match(em): probs.append("invalid email")
    if r.get("state") not in STATES: probs.append("state not a Bundesland: %s"%r.get("state"))
    if not r.get("source_url","").startswith("http"): probs.append("no source url")
    if not r.get("city"): probs.append("no city")
    for fld in ("subject_line","email_body","personalized_opening"):
        for b in BANNED:
            if b in (r.get(fld) or "").lower(): probs.append("banned '%s' in %s"%(b,fld))
    if "Oseni Ibrahim" not in r.get("email_body",""): probs.append("missing signature")
    if r.get("research_confidence")=="Low" or r.get("buying_intent")=="Low" and False: pass
    keys=[("e",em),("w",dom(r.get("website","")) or None),("c",nco(r.get("company")) or None)]
    ed=em.split("@")[-1]
    if ed not in ("t-online.de","gmx.de","web.de","gmail.com","googlemail.com","outlook.de","yahoo.de","freenet.de","arcor.de"): keys.append(("d",ed))
    hit=next((seen[k] for k in keys if k[1] and k in seen),None)
    if hit is not None: dups.append(r); continue
    for k in keys:
        if k[1]: seen[k]=True
    if em in EXCL: probs.append(EXCL[em])
    if probs: r["_why"]="; ".join(probs); excl.append(r)
    else: main.append(r)
print("raw",len(raw),"main",len(main),"excluded",len(excl),"dups",len(dups))
for r in excl: print("EXCL",r["_f"],r.get("company"),"|",r["_why"])
for r in dups: print("DUP",r["_f"],r.get("company"),r.get("email"))
subs=Counter(r["subject_line"] for r in main); print("dup subjects",[s for s,c in subs.items() if c>1])
ops=Counter(r["personalized_opening"][:70] for r in main); print("dup openings",[s for s,c in ops.items() if c>1])
if "--write" not in sys.argv: sys.exit()
o={"High":0,"Medium":1,"Low":2}
main.sort(key=lambda r:(o.get(r.get("buying_intent"),3),o.get(r.get("research_confidence"),3),r.get("state",""),r.get("city",""),r.get("company","")))
wb=Workbook(); hf=PatternFill("solid",fgColor="1F3864"); thin=Side(style="thin",color="D9D9D9")
W=[26,28,12,30,11,18,16,22,26,40,30,30,30,30,24,11,45,45,50,36,80,40,60,24,12,11,11,11,45]
def row(r,status,note):
    g=lambda k:r.get(k,"") or ""
    return [g("prospect_name"),g("company"),g("first_name"),g("email"),"Germany",g("state"),g("city"),g("business_type"),g("property_focus"),
      g("listings_evidence"),g("website"),g("instagram"),g("facebook"),g("linkedin"),g("youtube"),g("buying_intent"),g("personalization_detail"),
      g("personalization_reason"),g("personalized_opening"),g("subject_line"),g("email_body").replace("\\n","\n"),g("source_url"),g("evidence"),
      g("evidence_type"),g("research_confidence"),status,"Not Sent",None,note]
def sheet(ws,rows,name):
    ws.append(COLS)
    for x in rows: ws.append(x)
    for i,w in enumerate(W,1):
        ws.column_dimensions[get_column_letter(i)].width=w
        c=ws.cell(1,i); c.font=Font(bold=True,color="FFFFFF"); c.fill=hf; c.alignment=Alignment(wrap_text=True,vertical="center",horizontal="center")
    ws.row_dimensions[1].height=32
    for rr in ws.iter_rows(min_row=2):
        for c in rr: c.alignment=Alignment(wrap_text=True,vertical="top"); c.border=Border(bottom=thin)
        ws.row_dimensions[rr[0].row].height=170
        for idx in (10,11,12,13,14,21):
            c=rr[idx]
            if c.value and str(c.value).startswith("http"): c.hyperlink=c.value; c.font=Font(color="0563C1",underline="single")
    ws.freeze_panes="A2"
    t=Table(displayName=name,ref="A1:%s%d"%(get_column_letter(len(COLS)),max(ws.max_row,2)))
    t.tableStyleInfo=TableStyleInfo(name="TableStyleLight9",showRowStripes=True); ws.add_table(t)
ws=wb.active; ws.title="Prospects"
sheet(ws,[row(r,"Ready",r.get("notes","")) for r in main],"Prospects")
sheet(wb.create_sheet("Excluded"),[row(r,"Excluded","EXCLUDED: "+r["_why"]+(" | "+r.get("notes","") if r.get("notes") else "")) for r in excl],"Excluded")
has=lambda k:sum(1 for r in main if (r.get(k) or "").startswith("http"))
screened=int(sys.argv[sys.argv.index("--screened")+1]) if "--screened" in sys.argv else len(raw)
stats=[("Total prospects found (qualified, Prospects sheet)",len(main)),
("High intent",sum(r.get("buying_intent")=="High" for r in main)),("Medium intent",sum(r.get("buying_intent")=="Medium" for r in main)),
("Low intent",sum(r.get("buying_intent")=="Low" for r in main)),("With verified public business email",len(main)),
("With Instagram",has("instagram")),("With Facebook",has("facebook")),("With LinkedIn",has("linkedin")),("With YouTube",has("youtube")),
("With multiple active listings",sum(r.get("multiple_listings")=="Yes" for r in main)),
("High research confidence",sum(r.get("research_confidence")=="High" for r in main)),("Medium research confidence",sum(r.get("research_confidence")=="Medium" for r in main)),
("Excluded after validation (Excluded sheet)",len(excl)),("Duplicates removed",len(dups)),("Candidates screened (approx.)",screened),
("Bundesländer represented",len({r["state"] for r in main})),("Unique emails",len({r["email"].lower() for r in main})),
("Verification method","Company websites, Instagram, Facebook and LinkedIn could not be opened directly from the research environment (network policy). Every email, location, listing and social-profile fact was confirmed from search-engine results quoting the company's own pages (Impressum/Kontakt/listing pages). Spot-check a sample before sending."),
("Send status","No emails sent. Send Status = Not Sent, Date Sent blank for all rows.")]
s=wb.create_sheet("Summary"); s.append(("Metric","Value"))
for x in stats: s.append(x)
s.column_dimensions["A"].width=50; s.column_dimensions["B"].width=100
for c in s[1]: c.font=Font(bold=True,color="FFFFFF"); c.fill=hf
for rr in s.iter_rows(min_row=2):
    for c in rr: c.alignment=Alignment(wrap_text=True,vertical="top")
wb.save(OUT); print("saved",OUT); [print(a,"=",str(b)[:60]) for a,b in stats]
