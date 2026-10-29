"""Gera casos, roda csvline.old e csvline.new e grava diffs.jsonl + diff-report.md.

Uso: python3 difftool.py   (determinístico: seed fixa, sem dependência de ambiente)
"""
import json, os, random, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from csvline import old, new

SEED, N = 20261029, 200

HAND = [
    '', ',', ',,', 'a', 'a,b', 'a,b,', ',a', '"a,b"', '"a,b",c', '"a""b"', '"a""b",c',
    '""', '"",""', '"', '"abc', 'a"b', 'a"b"c', '"a"b', '"a"b,c', '"a" ,b', ' "a",b',
    ' a , b ', 'a, b', 'a ,b', '  ', ' ,', '"a\nb"', 'a\tb', '\ta,\tb', '"a",', '"a","b"',
    '"a""', '""""', 'a,"b', 'a,"b,c', '"a,b', 'x,"y""z",w', '"  a  "', '  "a"  ',
    'é,ü', '"é,ü"', 'a;b', "a,'b,c'", '\\,a', 'a\\"b',
]
ALPHABET = ['a', 'b', 'c', '1', ',', ',', '"', '"', ' ', ' ', '\t', '""', '","', 'é']


def cases():
    rng = random.Random(SEED)
    seen, out = set(), []
    for s in HAND:
        if s not in seen:
            seen.add(s); out.append(s)
    while len(out) < N:
        s = ''.join(rng.choice(ALPHABET) for _ in range(rng.randint(1, 8)))
        if s not in seen:
            seen.add(s); out.append(s)
    return out


def run(fn, line):
    try:
        return fn(line)
    except Exception as e:  # registrar, não abortar
        return {"error": f"{type(e).__name__}: {e}"}


def _trail(o):
    return o[:-1] if len(o) > 1 and o[-1] == '' else o


def classify(inp, o, n):
    """Causa primária, testada por hipóteses sobre a saída de old (ordem = prioridade)."""
    if isinstance(o, dict) or isinstance(n, dict):
        return "exceção em um dos parsers"
    if _trail(o) == n:
        return "campo vazio final descartado (`a,b,` -> 2 campos em vez de 3)"
    stripped = [f.strip() for f in o]
    if stripped == n:
        return "espaços/tabs ao redor do campo são removidos (new faz strip)"
    if _trail(stripped) == n:
        return "campo vazio final descartado + espaços removidos"
    if '"' in inp:
        if inp.count('"') % 2:
            return "aspa sem fechar: new mantém a aspa literal e quebra nas vírgulas internas"
        if any('"' in f for f in o):
            return 'escape `""` dentro de aspas não é desescapado (new devolve o texto cru)'
        return "aspas no meio do campo / texto após aspa de fechamento: new mantém as aspas, old as remove"
    return "outro"


def main():
    rows = []
    for c in cases():
        o, n = run(old.parse, c), run(new.parse, c)
        if o != n:
            rows.append({"input": c, "old": o, "new": n})
    with open(os.path.join(HERE, "diffs.jsonl"), "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    groups = {}
    for r in rows:
        groups.setdefault(classify(r["input"], r["old"], r["new"]), []).append(r)
    L = ["# Diferenças entre `csvline.old.parse` e `csvline.new.parse`", "",
         f"- Casos gerados: {len(cases())} (seed `{SEED}`; {len(HAND)} escritos à mão + aleatórios)",
         f"- Casos com diferença: {len(rows)} (detalhe em `diffs.jsonl`)", "",
         "Regerar tudo (determinístico):", "", "```", "python3 difftool.py", "```", ""]
    for k, rs in sorted(groups.items(), key=lambda kv: -len(kv[1])):
        ex = min(rs, key=lambda r: (len(r["input"]), r["input"]))
        L += [f"## {k} — {len(rs)} caso(s)", "",
              f"Exemplo mínimo: input `{ex['input']!r}`", "",
              f"- old: `{ex['old']!r}`", f"- new: `{ex['new']!r}`", ""]
    with open(os.path.join(HERE, "diff-report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(len(rows), "diffs;", {k: len(v) for k, v in groups.items()})


main()
