"""Gera report.md: python3 checks/build_report.py  (roda cada check_<modulo>.py)."""
import json, os, re, subprocess, sys
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
mods = "text numbers dates lists money records paths intervals".split()
claims = {}
for l in open(os.path.join(root, "claims.md"), encoding="utf-8"):
    m = re.match(r"\| (\w\d\d) \| (\w+) \| (.*) \|$", l.rstrip("\n"))
    if m: claims[m[1]] = m[3]
esc = lambda s: s.replace("|", "\\|").replace("\n", " ")
rows, nf = [], 0
for mod in mods:
    out = subprocess.run([sys.executable, f"checks/check_{mod}.py"], cwd=root, capture_output=True, text=True, check=True).stdout
    for r in json.loads(out):
        f = r["verdict"] == "falsa"; nf += f
        ce = f"`{esc(r['counterexample'])}`" if f else ""
        rows.append(f"| {r['id']} | {r['verdict']} | {ce} | `python3 checks/check_{mod}.py` (linha `{r['id']}`) |")
assert len(rows) == len(claims) == 152, (len(rows), len(claims))
with open(os.path.join(root, "report.md"), "w", encoding="utf-8") as fh:
    fh.write(f"# Relatório de verificação de claims.md\n\nTotal: {len(rows)} afirmações — {len(rows)-nf} verdadeiras, {nf} falsas.\n\n"
             "Reprodução: cada comando roda do diretório raiz, é determinístico (sem dependências, semente fixa em `checks/_common.py`) "
             "e imprime JSON com o veredito de todos os ids do módulo. `python3 checks/build_report.py` regenera este relatório.\n\n"
             "| id | veredito | contraexemplo | comando |\n|---|---|---|---|\n" + "\n".join(rows) + "\n")
