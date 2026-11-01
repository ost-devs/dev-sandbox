"""Builds report.md from checks/*/results.json and claims.md (run from repo root)."""
import json, re
mods = ['dates','intervals','lists','money','numbers','paths','records','text']
claims, text = {}, {}
for line in open('claims.md', encoding='utf-8'):
    m = re.match(r'\| (\w+) \| (\w+) \| (.*) \|$', line.rstrip('\n'))
    if m and m.group(1) != 'id': claims[m.group(1)] = m.group(2); text[m.group(1)] = m.group(3).replace('|', '\\|')
rows, nf = [], 0
for mod in mods:
    for r in json.load(open(f'checks/{mod}/results.json', encoding='utf-8')):
        cex = (r['counterexample'] or '').replace('|', '\\|').replace('\n', '\\n')
        nf += r['verdict'] == 'falsa'
        rows.append(f"| {r['id']} | {text[r['id']]} | {r['verdict']} | {'`'+cex+'`' if cex else ''} | `python3 -I checks/{mod}/check_{mod}.py` |")
ids = {r.split('|')[1].strip() for r in rows}
assert ids == set(claims), (set(claims) ^ ids)
out = ["# Relatório de verificação de claims.md", "",
       f"{len(rows)} afirmações: {len(rows)-nf} verdadeiras, {nf} falsas. Rodar tudo: `sh checks/run_all.sh` (cwd = raiz; regenera este relatório).",
       "Cada comando imprime `id<TAB>veredito<TAB>contraexemplo` e é determinístico (entradas fixas ou sementes literais no script).", "",
       "| id | afirmação | veredito | contraexemplo | comando |", "|---|---|---|---|---|"] + rows
open('report.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
