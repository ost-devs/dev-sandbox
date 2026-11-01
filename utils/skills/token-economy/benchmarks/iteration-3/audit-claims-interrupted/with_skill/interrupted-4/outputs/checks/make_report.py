"""Builds report.md from claims.md + checks/results/*.tsv. Run from repo root: python3 -I checks/make_report.py"""
import glob, re
res = {}
for f in glob.glob('checks/results/*.tsv'):
    mod = f.split('/')[-1][:-4]
    for l in open(f).read().splitlines():
        i, v, *c = l.split('\t'); res[i] = (mod, v, (c[0] if c else ''))
rows = []; claims = {}
for l in open('claims.md'):
    m = re.match(r'\| (\w+) \| (\w+) \| (.*) \|$', l)
    if m and m[1] != 'id': claims[m[1]] = m[3]
esc = lambda s: s.replace('|', '\\|').replace('\n', '\\n')
out = ['# Relatório de verificação de claims.md', '',
       f'{len(claims)} afirmações; verdadeiras: {sum(res[i][1]=="verdadeira" for i in claims)}, falsas: {sum(res[i][1]=="falsa" for i in claims)}.',
       'Checagens em `checks/<módulo>.py` (semente fixa em `checks/lib.py`), rodar da raiz.', '',
       '| id | veredito | contraexemplo | comando |', '|---|---|---|---|']
for i in claims:
    mod, v, c = res[i]
    out.append(f'| {i} | {v} | {"`"+esc(c)+"`" if c else ""} | `python3 -I checks/run.py {mod} {i}` |')
open('report.md', 'w').write('\n'.join(out) + '\n')
