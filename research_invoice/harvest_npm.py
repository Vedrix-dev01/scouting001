import json, subprocess, urllib.parse, collections, re
KW=["invoice","invoicing","e-invoice","einvoice","e-invoicing","peppol","xrechnung","zugferd","factur-x","ubl invoice","billing","subscription billing","recurring billing","accounts receivable","accounts payable","ar automation","ap automation","dunning","payment reminder","collections","xero","quickbooks","sage accounting","netsuite","exact online","datev","lexoffice","sevdesk","freshbooks","zoho books","accounting api","bookkeeping","ledger accounting","erp","odoo","dynamics 365 business central","payments api","b2b payments","payment gateway","reconciliation","expense management","spend management","payroll api","cash flow","invoice ocr","receipt ocr","document ai invoice","fintech sdk","open banking","billing api","metered billing","usage based billing","tax api","vat api","sales tax"]
PERSONAL={"gmail.com","googlemail.com","hotmail.com","outlook.com","yahoo.com","icloud.com","me.com","protonmail.com","proton.me","live.com","qq.com","163.com","126.com","gmx.de","web.de","mail.ru","yandex.ru","users.noreply.github.com","github.com","npmjs.com","example.com","aol.com","hey.com","pm.me","fastmail.com","msn.com","yahoo.co.uk","t-online.de","foxmail.com"}
out={}
for kw in KW:
    for frm in (0,250):
        url="https://registry.npmjs.org/-/v1/search?"+urllib.parse.urlencode({"text":kw,"size":250,"from":frm})
        try: d=json.loads(subprocess.run(["curl","-s","-m","30",url],capture_output=True,text=True).stdout)
        except Exception: continue
        for o in d.get("objects",[]):
            p=o["package"]; emails=set()
            if p.get("publisher",{}).get("email"): emails.add(p["publisher"]["email"].lower())
            for m in p.get("maintainers",[]):
                if m.get("email"): emails.add(m["email"].lower())
            for e in emails:
                dom=e.split("@")[-1]
                if dom in PERSONAL or "noreply" in e: continue
                rec=out.setdefault(dom,{"domain":dom,"emails":set(),"packages":[],"repos":set(),"kw":set()})
                rec["emails"].add(e); rec["kw"].add(kw)
                if len(rec["packages"])<8: rec["packages"].append(p["name"]+": "+(p.get("description") or "")[:120])
                r=p.get("links",{}).get("repository")
                if r: rec["repos"].add(r)
for r in out.values():
    for k in ("emails","repos","kw"): r[k]=sorted(r[k])
json.dump(list(out.values()),open("npm_candidates.json","w"),indent=1)
print(len(out))
