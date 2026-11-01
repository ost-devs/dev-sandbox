"""Builds report.md from claims.md + checks/*/results.json. Run from project root: python3 checks/make_report.py"""
import json, os, re
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
claims = {}
for line in open(os.path.join(root, 'claims.md'), encoding='utf-8'):
    m = re.match(r'\| ([A-Z]\d+) \| (\w+) \|', line)
    if m: claims[m[1]] = m[2]
rows, nf = [], 0
esc = lambda s: s.replace('|', '\\|').replace('\n', '\\n')
for i, mod in claims.items():
    p = os.path.join(root, 'checks', mod, 'results.json')
    r = json.load(open(p, encoding='utf-8')).get(i) if os.path.exists(p) else None
    if not r: rows.append(f'| {i} | **sem checagem** | | |'); continue
    f = r['verdict'] == 'falsa'; nf += f
    ce = f"`{esc(r['counterexample'])}`" if f else ''
    rows.append(f'| {i} | {r["verdict"]} | {ce} | `python3 checks/{mod}/check_{mod}.py {i}` |')
out = ['# Relatório de verificação de claims.md', '',
 f'{len(claims)} afirmações: {len(claims)-nf} verdadeiras, {nf} falsas. Entradas fixas ou geradas com semente registrada (`SEED` em `checks/common.py`). '
 'Rode a partir da raiz do projeto; sem argumento, `python3 checks/<módulo>/check_<módulo>.py` roda o módulo inteiro.', '',
 '| id | veredito | contraexemplo | comando |', '|---|---|---|---|'] + rows
open(os.path.join(root, 'report.md'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
