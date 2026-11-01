import json,subprocess,sys,re
mods=["text","numbers","dates","intervals","lists","money","paths","records"]
claims={}
for l in open("claims.md"):
    m=re.match(r"\| (\w+) \| (\w+) \|",l)
    if m and m[1]!="id": claims[m[1]]=m[2]
rows=[];tot={"verdadeira":0,"falsa":0}
for mod in mods:
    out=subprocess.run([sys.executable,"-I",f"checks/check_{mod}.py"],capture_output=True,text=True,check=True).stdout
    for l in out.splitlines():
        if l.startswith("{"):
            r=json.loads(l); rows.append((r,mod))
ids={r["id"] for r,_ in rows}
assert ids==set(claims) and len(rows)==152,(len(rows),set(claims)-ids)
L=["# Relatório de verificação de claims.md","",
"Reproduzir tudo: `python3 -I checks/check_<módulo>.py` (a partir da raiz); um id: `python3 -I checks/check_<módulo>.py <ID>`. Sementes fixas nos scripts.","",
"| id | veredito | contraexemplo | comando |","|---|---|---|---|"]
for r,mod in rows:
    tot[r["verdict"]]+=1
    ce=r["counterexample"].replace("|","\\|").replace("\n"," ")
    L.append(f"| {r['id']} | {r['verdict']} | {ce} | `python3 -I checks/check_{mod}.py {r['id']}` |")
L.insert(2,f"Total: {tot['verdadeira']} verdadeiras, {tot['falsa']} falsas, de 152.\n")
open("report.md","w").write("\n".join(L)+"\n")
print(tot)
