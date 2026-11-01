"""Builds report.md by running every checks/<module>.py. Run from repo root: python3 checks/make_report.py"""
import json, subprocess, sys, os
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
mods = ['text','numbers','dates','money','lists','records','paths','intervals']
claims = {}
for l in open(os.path.join(root,'claims.md')):
    p = [x.strip() for x in l.strip().strip('|').split('|', 2)]
    if len(p)==3 and p[0][:1].isalpha() and p[0]!='id': claims[p[0]] = p[2]
rows = []
for m in mods:
    out = subprocess.run([sys.executable, os.path.join('checks', m+'.py')], cwd=root, capture_output=True, text=True, check=True).stdout
    for l in out.splitlines():
        r = json.loads(l); r['mod']=m; rows.append(r)
ids = [r['id'] for r in rows]
assert len(rows)==152 and set(ids)==set(claims), (len(rows), set(claims)^set(ids))
esc = lambda s: s.replace('|','\\|').replace('\n','\\n')
f = sum(r['verdict']=='falsa' for r in rows)
o = ['# Relatório de auditoria de claims.md','',
 f'Total: {len(rows)} afirmações — {len(rows)-f} verdadeiras, {f} falsas.','',
 f'Semente registrada: 20261101 (checks/_lib.py); propriedades "para qualquer" testadas com 5000 casos gerados. Cada script é determinístico (rodado duas vezes, saída idêntica).',
 'Regerar este relatório: `python3 checks/make_report.py`. Verdadeira em propriedade aleatória = nenhum contraexemplo em 5000 casos (evidência, não prova).','',
 '| id | veredito | contraexemplo | comando |','|---|---|---|---|']
for r in rows:
    cex = '`'+esc(r['counterexample'])+'`' if r['counterexample'] else ''
    o.append(f"| {r['id']} | {r['verdict']} | {cex} | `python3 checks/{r['mod']}.py {r['id']}` |")
open(os.path.join(root,'report.md'),'w').write('\n'.join(o)+'\n')
print(len(rows), f)
