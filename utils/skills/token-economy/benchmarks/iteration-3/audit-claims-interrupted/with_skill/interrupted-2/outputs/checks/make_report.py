"""Builds report.md from checks/results/*.json. Run from repo root: python3 checks/make_report.py"""
import json, os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = []
for l in open(os.path.join(ROOT, "claims.md"), encoding="utf-8"):
    m = re.match(r"\| (\w+) \| (\w+) \|", l)
    if m and m.group(1) != "id":
        rows.append((m.group(1), m.group(2)))
res = {}
for mod in {m for _, m in rows}:
    p = os.path.join(ROOT, "checks", "results", f"{mod}.json")
    if os.path.exists(p):
        res[mod] = json.load(open(p, encoding="utf-8"))
esc = lambda s: str(s).replace("|", "\\|").replace("\n", "\\n")
out = ["# Relatório de verificação de claims.md\n",
       "Reproduzir tudo: `python3 checks/check_<modulo>.py` (a partir da raiz; semente fixa em `checks/lib.py`). "
       "Um id isolado: `python3 checks/check_<modulo>.py ID`. Regenerar este relatório: `python3 checks/make_report.py`.\n",
       "| id | veredito | contraexemplo | comando |", "|---|---|---|---|"]
nt = nf = nm = 0
for cid, mod in rows:
    r = res.get(mod, {}).get(cid)
    if not r:
        nm += 1; out.append(f"| {cid} | **sem checagem** | | |"); continue
    if r["verdict"] == "falsa": nf += 1
    else: nt += 1
    cex = f"`{esc(r['counterexample'])}`" if r["counterexample"] else ""
    out.append(f"| {cid} | {r['verdict']} | {cex} | `python3 checks/check_{mod}.py {cid}` |")
out.insert(1, f"\nTotal: {len(rows)} — verdadeiras {nt}, falsas {nf}, sem checagem {nm}.\n")
open(os.path.join(ROOT, "report.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
print(nt, nf, nm)
