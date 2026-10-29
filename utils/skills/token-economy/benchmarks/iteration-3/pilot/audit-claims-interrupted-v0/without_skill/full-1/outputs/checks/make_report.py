"""Gera report.md a partir de claims.md + results.tsv (rode run_all.py antes)."""
import os, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
res = {}
for line in open(os.path.join(root, 'checks/results.tsv')):
    cid, v, ce = (line.rstrip('\n').split('\t') + [''])[:3]
    res[cid] = (v, ce)
mod = {}
for line in open(os.path.join(root, 'claims.md')):
    m = re.match(r'\| ([A-Z]\d\d) \| (\w+) \|', line)
    if m:
        mod[m.group(1)] = m.group(2)
assert set(mod) == set(res), set(mod) ^ set(res)
esc = lambda t: t.replace('|', '\\|')
nf = sum(v == 'FALSA' for v, _ in res.values())
out = ['# Relatório de verificação de `claims.md`', '',
       f'- Afirmações: {len(res)} — verdadeiras: {len(res) - nf}, falsas: {nf}.',
       '- Cada checagem está em `checks/check_<módulo>.py`; reproduzir uma: `python3 checks/check_<módulo>.py <ID>`; todas: `python3 checks/run_all.py` (grava `checks/results.tsv`), depois `python3 checks/make_report.py`.',
       '- Determinismo: sem rede nem relógio; entradas fixas ou geradas com `random.Random(f"{SEED}:{ID}")`, `SEED = 20261029` (em `checks/harness.py`). Duas execuções completas produziram saídas idênticas.',
       '- Alcance do "verdadeira": para afirmações com domínio finito (ex.: N12, N15, D02, D08, M08, M15, M18, P11) a checagem é exaustiva. Para "qualquer string/lista/dict" é teste com casos limite fixos + amostra de milhares de casos com semente; ausência de contraexemplo não é prova.',
       '- Interpretações de domínio: D17/D19 consideram só resultados representáveis como `date` (fora disso o próprio `datetime` levanta `OverflowError`); M19 usa taxas finitas; I05/I06/I13/I14 usam intervalos com início < fim.',
       '', '| id | veredito | contraexemplo | comando |', '|---|---|---|---|']
for cid in sorted(res, key=lambda c: (list(dict.fromkeys(mod.values())).index(mod[c]), c)):
    v, ce = res[cid]
    out.append(f'| {cid} | {"falsa" if v == "FALSA" else "verdadeira"} | {esc(ce) if v == "FALSA" else ""} | `python3 checks/check_{mod[cid]}.py {cid}` |')
open(os.path.join(root, 'report.md'), 'w').write('\n'.join(out) + '\n')
