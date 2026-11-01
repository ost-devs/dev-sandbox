"""Gera report.md a partir de checks/*.out.txt (rode da raiz: python3 -I checks/build_report.py)."""
import os, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mods = ['text', 'numbers', 'dates', 'lists', 'money', 'intervals', 'paths', 'records']
rows, nt, nf = [], 0, 0
for m in mods:
    for line in open(f'{root}/checks/{m}.out.txt', encoding='utf-8').read().splitlines():
        i, v, *c = line.split('\t')
        c = (c[0] if c else '').replace('|', '\\|')
        if v == 'verdadeira': nt += 1
        else: nf += 1
        rows.append(f'| {i} | {v} | {c} | `python3 -I checks/{m}.py {i}` |')
out = ['# Relatório de verificação de claims.md', '',
       f'{nt + nf} afirmações: **{nt} verdadeiras**, **{nf} falsas**.', '',
       'Rode da raiz do projeto. Tudo: `python3 -I checks/<módulo>.py` (módulos: ' + ', '.join(mods) + '). '
       'Entradas fixas ou geradas com `random.Random(SEED)` (SEED no topo de cada script); a saída é idêntica entre execuções. '
       'Regenerar este relatório: `python3 -I checks/build_report.py`.', '',
       'Obs.: afirmações universais sobre domínios infinitos são verificadas por busca exaustiva quando o domínio é finito e por amostragem seeded + casos de borda caso contrário; "verdadeira" nesses casos significa "nenhum contraexemplo encontrado".', '',
       '| id | veredito | contraexemplo | comando |', '|---|---|---|---|'] + rows
open(f'{root}/report.md', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
