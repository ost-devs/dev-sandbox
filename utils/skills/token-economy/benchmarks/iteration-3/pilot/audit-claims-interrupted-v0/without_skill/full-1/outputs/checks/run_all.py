"""Roda as checagens de todos os módulos (cada uma via CLI, como na tabela do report) e grava results.tsv."""
import os, subprocess, sys
here = os.path.dirname(os.path.abspath(__file__))
rows = []
for m in ['text', 'numbers', 'dates', 'lists', 'money', 'intervals', 'paths', 'records']:
    p = subprocess.run([sys.executable, os.path.join(here, f'check_{m}.py')], capture_output=True, text=True)
    if p.returncode or p.stderr:
        sys.exit(f'erro em {m}: {p.stderr}')
    rows += p.stdout.splitlines()
open(os.path.join(here, 'results.tsv'), 'w').write('\n'.join(rows) + '\n')
print(len(rows), 'veredictos;', sum('\tFALSA\t' in r for r in rows), 'falsas')
