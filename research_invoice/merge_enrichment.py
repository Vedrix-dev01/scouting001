"""Merge email-enrichment results (enrich_*.jsonl: id=<file>#<line>) into research_invoice/leads."""
import json, glob, os, re, sys
D=os.path.dirname(os.path.abspath(__file__)); L=os.path.join(D,"leads")
EM=re.compile(r"^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$")
PERSONAL={"gmail.com","googlemail.com","hotmail.com","outlook.com","yahoo.com","icloud.com","aol.com","gmx.de","web.de","t-online.de","live.com","me.com"}
from urllib.parse import urlparse
def dom(u): return urlparse(u if "://" in u else "http://"+u).netloc.lower().removeprefix("www.")
files={os.path.basename(f):[json.loads(l) for l in open(f)] for f in glob.glob(os.path.join(L,"*.jsonl"))}
used={(r.get("email") or "").lower() for rs in files.values() for r in rs if r.get("email")}
ok=bad=0
ALLOW=set(); SKIP=set()
args=sys.argv[1:]
if "--allow" in args: i=args.index("--allow"); ALLOW=set(x.lower() for x in args[i+1].split(",")); del args[i:i+2]
if "--skip" in args: i=args.index("--skip"); SKIP=set(x.lower() for x in args[i+1].split(",")); del args[i:i+2]
for ef in args:
    for l in open(ef):
        e=json.loads(l); fn,i=e["id"].split("#"); r=files[fn][int(i)]
        em=e["email"].strip(); d=em.split("@")[-1].lower(); wd=dom(r["website"])
        why=None
        if em.lower() in SKIP: why="skipped (source not the company's own page)"
        elif r.get("email"): why="already has email"
        elif not EM.match(em) or d in PERSONAL: why="invalid/personal"
        elif em.lower() in used: why="duplicate email"
        elif em.lower() not in ALLOW and not (d==wd or d.endswith("."+wd) or wd.endswith("."+d)): why=f"domain mismatch {d} vs {wd}"
        if why: bad+=1; print("SKIP",r["company"],em,why); continue
        r["email"]=em; used.add(em.lower())
        r["notes"]=(r.get("notes","").replace("No verified email","").strip(" |")+f" | Email added in enrichment pass from search result: {e.get('source_url','')} ({e.get('evidence','')[:160]})").strip(" |")
        if r.get("research_confidence")=="Low": r["research_confidence"]="Medium"
        ok+=1
for fn,rs in files.items():
    open(os.path.join(L,fn),"w").write("\n".join(json.dumps(r,ensure_ascii=False) for r in rs)+"\n")
print("merged",ok,"skipped",bad)
