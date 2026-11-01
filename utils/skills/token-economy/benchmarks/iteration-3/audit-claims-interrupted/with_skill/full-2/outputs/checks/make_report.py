"""Rebuilds report.md from checks/*/results.json (run all check_*.py first). Usage: python3 checks/make_report.py"""
import json, os, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mods = ["text","numbers","lists","dates","intervals","money","paths","records"]
rows = []
for m in mods:
    cmd = f"python3 checks/{m}/check_{m}.py"
    for o in json.load(open(f"{R}/checks/{m}/results.json")):
        rows.append((o["id"], o["verdict"], o["counterexample"], cmd, m))
ids = re.findall(r"^\| ([A-Z]\d\d) \|", open(f"{R}/claims.md").read(), re.M)
assert sorted(ids) == sorted(r[0] for r in rows), "ids mismatch"
order = {i: k for k, i in enumerate(ids)}
rows.sort(key=lambda r: order[r[0]])
f = sum(r[1] == "falsa" for r in rows)
out = ["# Relatório de verificação de claims.md\n",
 f"{len(rows)} afirmações: {len(rows)-f} verdadeiras, {f} falsas. Semente: 20261101 (checks/lib.py). "
 "Cada comando roda da raiz do projeto, é determinístico e regrava `checks/<módulo>/results.json`. "
 "`python3 checks/make_report.py` regenera este relatório.\n",
 "| id | veredito | contraexemplo | comando |", "|---|---|---|---|"]
for i, v, c, cmd, m in rows:
    c = c.replace("|", "\\|").replace("\n", " ")
    out.append(f"| {i} | {v} | {'`'+c.replace('`','')+'`' if c else ''} | `{cmd}` |")
open(f"{R}/report.md", "w").write("\n".join(out) + "\n")
print(len(rows), "rows,", f, "falsa")
