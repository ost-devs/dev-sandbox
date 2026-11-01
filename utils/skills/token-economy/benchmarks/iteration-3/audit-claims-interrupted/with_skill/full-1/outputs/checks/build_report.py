"""Runs every checks/<mod>/checks.py (twice, to confirm determinism) and writes report.md. Usage: python3 -I checks/build_report.py"""
import os, subprocess, sys, re
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mods = sorted(d for d in os.listdir(os.path.join(R, "checks")) if os.path.isfile(os.path.join(R, "checks", d, "checks.py")))
rows = {}
for m in mods:
    cmd = [sys.executable, "-I", f"checks/{m}/checks.py"]
    a = subprocess.run(cmd, cwd=R, capture_output=True, text=True).stdout
    b = subprocess.run(cmd, cwd=R, capture_output=True, text=True).stdout
    assert a == b, f"non-deterministic: {m}"
    for line in a.splitlines():
        cid, v, ce = (line.split("\t") + [""])[:3]
        rows[cid] = (m, v, ce)
claims = {}
for l in open(os.path.join(R, "claims.md"), encoding="utf-8"):
    p = [x.strip() for x in l.strip().strip("|").split("|", 2)]
    if re.fullmatch(r"[A-Z]+\d+", p[0]): claims[p[0]] = p[2]
assert set(claims) == set(rows), (set(claims) ^ set(rows))
esc = lambda s: s.replace("|", "\\|").replace("\n", "\\n")
nf = sum(v == "falsa" for _, v, _ in rows.values())
out = [f"# Relatório de verificação de claims.md\n",
       f"{len(rows)} afirmações: {len(rows)-nf} verdadeiras, {nf} falsas. Semente das checagens: ver `checks/_lib.py` (SEED, derivada por id).",
       "Reproduzir tudo: `python3 -I checks/build_report.py` (regenera este arquivo). Um módulo: `python3 -I checks/<módulo>/checks.py [ID ...]`.\n",
       "| id | veredito | contraexemplo | comando |", "|---|---|---|---|"]
for cid in sorted(rows, key=lambda c: (list(claims).index(c))):
    m, v, ce = rows[cid]
    out.append(f"| {cid} | {v} | {('`'+esc(ce)+'`') if ce else ''} | `python3 -I checks/{m}/checks.py {cid}` |")
open(os.path.join(R, "report.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(rows), "ok;", nf, "falsas")
