"""Run every check; write checks/results.jsonl and report.md. Usage: python3 checks/run_all.py (from project root)."""
import subprocess, sys, json, os, re
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
mods = {'T': 'text', 'N': 'numbers', 'D': 'dates', 'L': 'lists', 'M': 'money', 'I': 'intervals', 'P': 'paths', 'R': 'records'}
res = {}
for p, m in mods.items():
    out = subprocess.run([sys.executable, os.path.join(here, f'check_{m}.py')], capture_output=True, text=True, cwd=root, check=True).stdout
    for line in out.splitlines():
        r = json.loads(line); res[r['id']] = r
open(os.path.join(here, 'results.jsonl'), 'w').write(''.join(json.dumps(res[k], ensure_ascii=False) + '\n' for k in res))
claims = {}
for line in open(os.path.join(root, 'claims.md')):
    m = re.match(r'\| (\w\d\d) \| (\w+) \| (.*) \|$', line.rstrip())
    if m: claims[m[1]] = m[3]
assert set(claims) == set(res) and len(res) == 152, (len(claims), len(res))
nf = sum(not r['holds'] for r in res.values())
md = ['# Auditoria de claims.md', '',
      f'{len(res)} afirmações: {len(res) - nf} verdadeiras, {nf} falsas. Semente das gerações aleatórias: `20261029` (`checks/common.py`; cada claim deriva seu gerador de `SEED:id`).', '',
      'Reproduzir tudo: `python3 checks/run_all.py` (regera este arquivo). Uma claim: o comando da última coluna, a partir da raiz do projeto.', '',
      'Alcance: claims universais ("para todo...") são verificadas exaustivamente quando o domínio é finito e pequeno, senão por amostra com semente fixa (mais casos de borda). "Verdadeira" nesses casos = nenhum contraexemplo encontrado; "falsa" = contraexemplo concreto e reproduzível.', '',
      '| id | veredito | contraexemplo | comando |', '|---|---|---|---|']
for cid, r in res.items():
    mod = mods[cid[0]]
    ce = '' if r['holds'] else '`' + r['counterexample'].replace('|', '\\|').replace('`', "'") + '`'
    md.append(f"| {cid} | {'verdadeira' if r['holds'] else 'falsa'} | {ce} | `python3 checks/check_{mod}.py {cid}` |")
open(os.path.join(root, 'report.md'), 'w').write('\n'.join(md) + '\n')
print(len(res), 'claims;', nf, 'false')
