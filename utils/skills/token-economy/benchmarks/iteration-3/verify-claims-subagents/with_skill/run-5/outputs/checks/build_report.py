"""Re-runs every check and writes report.md. Usage: python3 checks/build_report.py"""
import glob, json, os, re, subprocess
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(root)
rows = []
for f in sorted(glob.glob("checks/*/[TMDC][0-9].py")):
    r = subprocess.run(["python3", f], capture_output=True, text=True)
    d = json.loads(r.stdout.strip().splitlines()[-1])
    rows.append((d["id"], d["verdict"], d["counterexample"], f))
order = {k: i for i, k in enumerate("TMDC")}
rows.sort(key=lambda r: (order[r[0][0]], int(r[0][1:])))
nf = sum(r[1] == "falsa" for r in rows)
out = ["# Relatório de verificação de `calc/`", "",
       f"{len(rows)} afirmações: {len(rows)-nf} verdadeiras, {nf} falsas. Semente das checagens aleatórias: 20261101 (`checks/common.py`).",
       "Reproduzir tudo: `python3 checks/build_report.py` (reescreve este arquivo).", "",
       "| id | veredito | contraexemplo | comando |", "|---|---|---|---|"]
for i, v, c, f in rows:
    c = (c or "—").replace("|", "\\|").replace("\n", " ")
    out.append(f"| {i} | {v} | {c} | `python3 {f}` |")
open("report.md", "w").write("\n".join(out) + "\n")
