import json,os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows=[];ids={}
for l in open(f"{root}/claims.md"):
    p=[x.strip() for x in l.split("|")]
    if len(p)>3 and p[1][:1].isalpha() and p[1]!="id": ids[p[1]]=(p[2],p[3])
tot=f=0;out=[]
for m in "text dates intervals lists money numbers paths records".split():
    for r in json.load(open(f"{root}/checks/{m}/results.json")):
        c=(r["counterexample"] or "").replace("|","\\|").replace("\n","\\n")
        cmd=f"`python3 checks/{m}/check_{m}.py` ({r['how']})"
        out.append(f"| {r['id']} | {r['verdict']} | {('`'+c+'`') if c else ''} | {cmd} |");tot+=1;f+=r["verdict"]=="falsa"
assert tot==len(ids)==152,(tot,len(ids))
open(f"{root}/report.md","w").write(f"# Relatório de verificação de claims.md\n\n{tot} afirmações: {tot-f} verdadeiras, {f} falsas.\n\nTudo reproduzível: `checks/run_all.sh` (ou o comando de cada linha, a partir da raiz). Amostras aleatórias usam semente = crc32 do id (campo seed=). \"Verdadeira\" em propriedades universais = nenhum contraexemplo em n amostras semeadas.\n\n| id | veredito | contraexemplo | comando |\n|---|---|---|---|\n"+"\n".join(out)+"\n")
print(tot,f)
