import json, os, re
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
mods = ['text','numbers','dates','intervals','lists','money','paths','records']
claims = {}
for l in open(os.path.join(root,'claims.md'), encoding='utf-8'):
    m = re.match(r'\| (\w+) \| (\w+) \|', l)
    if m and m.group(1) != 'id': claims[m.group(1)] = m.group(2)
rows, nf = [], 0
for mod in mods:
    for r in json.load(open(os.path.join(root,'checks',mod,'results.json'), encoding='utf-8')):
        assert claims.pop(r['id']) == mod
        ce = r['contraexemplo'].replace('|','\\|').replace('\n','\\n')
        nf += r['veredito']=='falsa'
        rows.append(f"| {r['id']} | {r['veredito']} | {('`'+ce+'`') if ce else ''} | `python3 -I checks/{mod}/check_{mod}.py {r['id']}` |")
assert not claims, claims
out = ["# Relatório de auditoria de claims.md", "",
 f"{len(rows)} afirmações: {len(rows)-nf} verdadeiras, {nf} falsas. Rodar tudo: `for m in text numbers dates intervals lists money paths records; do python3 -I checks/$m/check_$m.py; done` (a partir desta pasta; entradas aleatórias usam semente fixa em `checks/harness.py`).", "",
 "| id | veredito | contraexemplo | comando |", "|---|---|---|---|"] + rows
open(os.path.join(root,'report.md'),'w',encoding='utf-8').write('\n'.join(out)+'\n')
print(len(rows), nf)
