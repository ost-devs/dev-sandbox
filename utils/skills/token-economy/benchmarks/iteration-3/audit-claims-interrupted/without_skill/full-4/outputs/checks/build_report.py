import json, subprocess, sys, os
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mods = ["text","numbers","dates","intervals","lists","money","paths","records"]
rows = []
for m in mods:
    out = subprocess.run([sys.executable,"-I",f"checks/{m}.py"],cwd=root,capture_output=True,text=True)
    for l in out.stdout.splitlines():
        if l.startswith("{"): rows.append(json.loads(l))
claims = {}
for l in open(os.path.join(root,"claims.md")):
    p=[x.strip() for x in l.split("|")]
    if len(p)>3 and p[1] and p[1][0].isalpha() and p[1]!="id": claims[p[1]]=p[3]
esc=lambda s:str(s).replace("|","\\|").replace("\n"," ")
f=sum(r["verdict"]=="falsa" for r in rows)
L=[f"# Relatório de auditoria de claims.md\n",f"Total: {len(rows)} afirmações; verdadeiras: {len(rows)-f}; falsas: {f}.\n",
"Reproduzir tudo: `python3 -I checks/<modulo>.py [ID]` a partir da raiz (sementes fixas; saída determinística). Este relatório: `python3 -I checks/build_report.py > report.md`.\n",
"| id | veredito | contraexemplo | comando |","|---|---|---|---|"]
for r in rows:
    L.append(f"| {r['id']} | {r['verdict']} | {esc(r['counterexample'] or '')} | `{r['command']}` |")
missing=set(claims)-{r['id'] for r in rows}
if missing: L.append(f"\nSEM CHECAGEM: {sorted(missing)}")
print("\n".join(L))
