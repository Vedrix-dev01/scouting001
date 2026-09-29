import json, glob, re, sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from curation import EXCLUDE, REVIEW
EXL={k.lower():v for k,v in EXCLUDE.items()}; REV={k.lower():v for k,v in REVIEW.items()}
PERSONAL={"gmail.com","protonmail.com","live.com","mac.com","yahoo.com","outlook.com","hotmail.com","icloud.com"}
from urllib.parse import urlparse
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

SP = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(SP, "..", "US_Trading_Bot_Prospects_200.xlsx")
COLS = ["Prospect Name","Company","First Name","Email","Country","State","City","Trading Niche","Trading Platform",
"Trading Product or Project","Buying Intent","Personalization Detail","Personalization Reason","Personalized Opening",
"Subject Line","Email Body","Source URL","Evidence","Evidence Type","Research Confidence","Lead Status","Send Status",
"Date Sent","Notes"]
BANNED = ["tailored solution","seamless","cutting edge","cutting-edge","revolutioni","unlock","transform your workflow",
"leverage","game changing","game-changing","synergy","urgent","act now","guarantee","make money","get rich",
"free money","investment opportunity","crypto profits","100% profit","i hope you're doing well","hope you're having",
"i came across your profile","i noticed you are a trader"]
STATES = {"Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming","District of Columbia","Puerto Rico"}
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")

def norm_co(s):
    s = (s or "").lower()
    s = re.sub(r"\b(llc|inc|corp|corporation|co|ltd|l\.l\.c|the|group|capital|trading|technologies|technology|software)\b","",s)
    return re.sub(r"[^a-z0-9]","",s)

files = sorted(glob.glob(f"{SP}/leads/*.jsonl"))
raw = []
for f in files:
    for i,line in enumerate(open(f)):
        line=line.strip()
        if not line: continue
        try: r=json.loads(line)
        except Exception as e: print("BADJSON",f,i,e); continue
        r["_src"]=f.split("/")[-1]; raw.append(r)

issues=[]; kept=[]; dups=[]; rejected=[]
seen_email={}; seen_co={}; seen_person={}; seen_dom={}
GENERIC_DOM={"gmail.com","yahoo.com","outlook.com","hotmail.com","icloud.com","protonmail.com","proton.me","aol.com","me.com","live.com"}
conf_rank={"High":2,"Medium":1,"Low":0}
for r in raw:
    r={k:(v.strip() if isinstance(v,str) else v) for k,v in r.items()}
    em=(r.get("email") or "").lower()
    probs=[]
    if not EMAIL_RE.match(em): probs.append("bad email")
    if r.get("state") not in STATES: probs.append(f"state? {r.get('state')}")
    if not (r.get("source_url","").startswith("http")): probs.append("no url")
    for fld in ("subject_line","email_body","personalized_opening"):
        t=(r.get(fld) or "").lower()
        for b in BANNED:
            if b in t: probs.append(f"banned '{b}' in {fld}")
    if "bad email" in probs or "no url" in probs or r.get("research_confidence")=="Low" and False:
        rejected.append((r,probs)); continue
    dom=em.split("@")[-1] if "@" in em else ""
    web=urlparse(r.get("source_url","")).netloc.lower().replace("www.","")
    keys=[("e",em),("c",norm_co(r.get("company")) if norm_co(r.get("company")) not in ("","independent") else None),
          ("p",re.sub(r"[^a-z]","",(r.get("prospect_name") or "").lower())),
          ("d",dom if dom and dom not in GENERIC_DOM else None)]
    hit=None
    for kt,kv in keys:
        if kv and (kt,kv) in seen_email: hit=seen_email[(kt,kv)]; break
    if hit is not None:
        old=kept[hit]
        if conf_rank.get(r.get("research_confidence"),0)>conf_rank.get(old.get("research_confidence"),0):
            dups.append(old); kept[hit]=r
        else: dups.append(r)
        for kt,kv in keys:
            if kv: seen_email[(kt,kv)]=hit
        continue
    idx=len(kept); kept.append(r)
    for kt,kv in keys:
        if kv: seen_email[(kt,kv)]=idx
    if probs: issues.append((r.get("prospect_name"),r["_src"],probs))

# subject uniqueness
subs={}
for r in kept:
    s=r.get("subject_line","").lower(); subs.setdefault(s,[]).append(r.get("prospect_name"))
for s,v in subs.items():
    if len(v)>1: issues.append((v,"dup subject",s))
opens={}
for r in kept:
    o=r.get("personalized_opening","")[:60].lower(); opens.setdefault(o,[]).append(r.get("prospect_name"))
for s,v in opens.items():
    if len(v)>1: issues.append((v,"dup opening",s))

print("files",len(files),"raw",len(raw),"kept",len(kept),"dups",len(dups),"rejected",len(rejected))
for x in issues: print("ISSUE",x)
for r,p in rejected: print("REJ",r.get("prospect_name"),p)
for d in dups: print("DUP",d.get("prospect_name"),d.get("email"),d["_src"])


# pull out curated exclusions (and the non-preferred Harden duplicate)
excluded=[]; main=[]
for r in kept+[d for d in dups if d.get("email","").lower() in EXL]:
    em=r["email"].lower()
    if em in EXL:
        if not any(x["email"].lower()==em for x in excluded):
            excluded.append(r)
    else: main.append(r)
# restore harden business-domain record if it was dropped as dup
for d in dups:
    if d["email"].lower()=="contact@harden-ai.com" and not any(x["email"].lower()=="contact@harden-ai.com" for x in main):
        main.append(d)
dups=[d for d in dups if not (d["email"].lower() in EXL or d["email"].lower()=="contact@harden-ai.com")]
for r in main:
    em=r["email"].lower(); dom=em.split("@")[1]
    notes=[r.get("notes","")]
    status="Ready"
    if em in REV: status="Needs Review"; notes.insert(0,"REVIEW: "+REV[em])
    if dom in PERSONAL or dom.endswith(".edu"):
        status="Needs Review"; notes.insert(0,"REVIEW: personal-domain address, published by the prospect on their public profile/README (not a company domain).")
    if not r.get("city") or "not listed" in r.get("city",""): status="Needs Review"
    if r.get("research_confidence")=="Low": status="Needs Review"
    r["_status"]=status; r["_notes"]=" | ".join(n for n in notes if n)
for r in excluded:
    r["_status"]="Excluded"; r["_notes"]="EXCLUDED: "+EXL[r["email"].lower()]+(" | "+r.get("notes","") if r.get("notes") else "")
print("main",len(main),"excluded",len(excluded),"dups",len(dups))
from collections import Counter
print(Counter(r["_status"] for r in main), Counter(r["research_confidence"] for r in main), Counter(r["buying_intent"] for r in main))
print("states",len({r['state'] for r in main}))

if "--write" in sys.argv:
    from openpyxl.worksheet.datavalidation import DataValidation
    order={"High":0,"Medium":1,"Low":2}; st={"Ready":0,"Needs Review":1}
    main.sort(key=lambda r:(st[r["_status"]],order.get(r.get("buying_intent"),3),order.get(r.get("research_confidence"),3),r.get("state",""),r.get("prospect_name","")))
    wb=Workbook()
    hdr_fill=PatternFill("solid",fgColor="1F3864"); thin=Side(style="thin",color="D9D9D9")
    widths=[24,24,12,32,14,14,16,24,22,28,11,45,45,45,32,70,40,60,20,12,12,11,11,45]
    def sheet(ws,rows,tname):
        ws.append(COLS)
        for r in rows:
            ws.append([r.get("prospect_name"),r.get("company"),r.get("first_name",""),r.get("email"),
                "United States",r.get("state"),r.get("city"),r.get("trading_niche"),r.get("trading_platform"),r.get("trading_product"),
                r.get("buying_intent"),r.get("personalization_detail"),r.get("personalization_reason"),r.get("personalized_opening"),
                r.get("subject_line"),r.get("email_body","").replace("\\n","\n"),r.get("source_url"),r.get("evidence"),r.get("evidence_type"),
                r.get("research_confidence"),r["_status"],"Not Sent",None,r["_notes"]])
        for i,w in enumerate(widths,1):
            ws.column_dimensions[get_column_letter(i)].width=w
            c=ws.cell(1,i); c.font=Font(bold=True,color="FFFFFF"); c.fill=hdr_fill
            c.alignment=Alignment(wrap_text=True,vertical="center",horizontal="center")
        ws.row_dimensions[1].height=32
        for row in ws.iter_rows(min_row=2):
            for c in row: c.alignment=Alignment(wrap_text=True,vertical="top"); c.border=Border(bottom=thin)
            ws.row_dimensions[row[0].row].height=150
            u=row[16]
            if u.value: u.hyperlink=u.value; u.font=Font(color="0563C1",underline="single")
        ws.freeze_panes="B2"
        t=Table(displayName=tname,ref=f"A1:{get_column_letter(len(COLS))}{max(ws.max_row,2)}")
        t.tableStyleInfo=TableStyleInfo(name="TableStyleLight9",showRowStripes=True); ws.add_table(t)
        for col,opts in (("U",'"Ready,Needs Review,Excluded"'),("V",'"Not Sent,Sent,Bounced,Replied"'),("T",'"High,Medium,Low"'),("K",'"High,Medium"')):
            dv=DataValidation(type="list",formula1=opts,allow_blank=True); ws.add_data_validation(dv); dv.add(f"{col}2:{col}{ws.max_row}")
    ws=wb.active; ws.title="Prospects"; sheet(ws,main,"Prospects")
    sheet(wb.create_sheet("Excluded"),excluded,"ExcludedLeads")
    n=len(main)+1
    screened=int(sys.argv[sys.argv.index("--write")+1])
    s=wb.create_sheet("Summary")
    P="Prospects!"
    rows=[("Metric","Value"),
      ("Candidates screened (approx., incl. those rejected during research)",screened),
      ("Candidate records returned by research",len(raw)),
      ("Duplicate records removed",len(raw)-len(main)-len(excluded)),
      ("Excluded after quality review (see Excluded sheet)",len(excluded)),
      ("Qualified prospects (Prospects sheet)",len(main)),
      ("Prospects with publicly displayed email",len(main)),
      ("  of which company-domain emails",sum(1 for r in main if r['email'].split('@')[1].lower() not in PERSONAL and not r['email'].lower().endswith('.edu'))),
      ("High confidence",sum(1 for r in main if r.get("research_confidence")=="High")),
      ("Medium confidence",sum(1 for r in main if r.get("research_confidence")=="Medium")),
      ("Low confidence",sum(1 for r in main if r.get("research_confidence")=="Low")),
      ("High buying intent",sum(1 for r in main if r.get("buying_intent")=="High")),
      ("Medium buying intent",sum(1 for r in main if r.get("buying_intent")=="Medium")),
      ("Ready",sum(1 for r in main if r.get("_status")=="Ready")),
      ("Needs Review",sum(1 for r in main if r.get("_status")=="Needs Review")),
      ("Not Sent",len(main)),
      ("Personalized emails",sum(1 for r in main if r.get("email_body"))),
      ("Unique companies",len({norm_co(r.get('company')) if norm_co(r.get('company')) not in ('','independent') else r['prospect_name'] for r in main})),
      ("Unique emails",len({r['email'].lower() for r in main})),
      ("States represented",len({r['state'] for r in main})),
      ("Research limitation","The research environment's network policy blocked most company websites, LinkedIn and forums; emails were verified on public GitHub organization/profile pages and PyPI package pages. Cities marked 'from search results' in Notes were not confirmed on a fetched page."),
      ("Before sending","Replace [Your Name] / [Your Business]. No emails have been sent; Date Sent is blank for all rows.")]
    for r in rows: s.append(r)
    s.column_dimensions["A"].width=62; s.column_dimensions["B"].width=90
    for row in s.iter_rows(min_row=2):
        for c in row: c.alignment=Alignment(wrap_text=True,vertical="top")
    for c in s[1]: c.font=Font(bold=True,color="FFFFFF"); c.fill=hdr_fill
    wb.save(OUT); print("saved",OUT)
