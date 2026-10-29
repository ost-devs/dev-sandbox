"""Generate 200 deterministic inputs, run csvline.old/new.parse, write diffs.jsonl."""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from csvline import old, new

SEED, N = 20261029, 200

HAND = [
    '', ',', ',,', 'a', 'a,b,c', 'a,b,', ',a', 'a,,b',
    '"a,b"', '"a,b",c', 'a,"b,c"', '"a""b"', '"a""b",c', '""', '"",x', 'x,""',
    '"abc', 'a,"bc', 'ab"c', 'a"b"c', '"a"b', '"a"b,c', '"a" ,b', ' "a",b',
    ' a , b ', 'a , b', '  ', ' , ', '\ta\t,b', 'a b,c d', '"  a  ",b',
    '"a" "b"', '"a""', '"""', '""""', 'a,"', '"', ',"', '"a",', '"a",,"b"',
    'a\\,b', 'a;b', 'a\nb', '"a\nb"', 'é,ü', '"é,ü"',
]
ALPHABET = ['a', 'b', 'x', '1', ' ', ',', ',', '"', '"', '""', '\t', 'é']

def gen():
    rnd = random.Random(SEED)
    cases = list(HAND)
    seen = set(cases)
    while len(cases) < N:
        s = ''.join(rnd.choice(ALPHABET) for _ in range(rnd.randint(1, 10)))
        if s not in seen:
            seen.add(s); cases.append(s)
    return cases

def run(fn, s):
    try:
        return fn(s)
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}

CATS = [
    ("quote-unbalanced", "Aspa sem par (campo não fechado ou aspa solta)",
     "old: aspa abre campo quoted que vai até o fim da linha (vírgulas viram texto); new: aspa vira caractere literal e a linha continua sendo dividida nas vírgulas."),
    ("quote-escaped", 'Aspa escapada `""` dentro de campo entre aspas',
     'old: `""` vira uma aspa literal; new: o regex `[^"]*` não aceita `""`, então o campo inteiro (com as aspas) sai como texto literal.'),
    ("whitespace", "Espaço/tab nas bordas de campo",
     "old: preserva espaços; new: remove espaços/tabs antes e depois de cada campo (inclusive depois da aspa de fechamento)."),
    ("trailing-comma", "Campo vazio final removido",
     "old: `a,` dá `['a', '']`; new: o último campo vazio depois de vírgula final desaparece."),
    ("quote-misplaced", "Aspa no meio de campo ou texto fora das aspas",
     "old: tira toda aspa não escapada, esteja onde estiver (`a\"b\"c` vira `abc`); new: só reconhece aspas no início do campo, o resto fica literal."),
]

def classify(inp, o, n):
    if inp.count('"') % 2:
        return "quote-unbalanced"
    if any('"' in f for f in o):
        return "quote-escaped"
    strip = lambda l: [f.strip() for f in l]
    def norm(l):
        l = strip(l)
        while len(l) > 1 and l[-1] == '':
            l.pop()
        return l
    if strip(o) == n:
        return "whitespace"
    if norm(o) == norm(n):
        return "trailing-comma"
    return "quote-misplaced"

def report(diffs, total, path):
    groups = {k: [] for k, _, _ in CATS}
    for d in diffs:
        groups[classify(d["input"], d["old"], d["new"])].append(d)
    L = ["# Diferenças entre `csvline.old.parse` e `csvline.new.parse`", "",
         f"{total} entradas geradas (seed `{SEED}`), {len(diffs)} com resultado diferente (detalhe em `diffs.jsonl`).",
         "Cada diferença cai em um único tipo (o primeiro que se aplica na ordem abaixo); entradas com várias causas",
         "aparecem só no tipo de maior prioridade. Exemplo = a menor entrada do grupo.", "",
         "| Tipo | Casos |", "|---|---|"]
    for k, title, _ in CATS:
        L.append(f"| {title} | {len(groups[k])} |")
    for k, title, why in CATS:
        g = sorted(groups[k], key=lambda d: (len(d["input"]), d["input"]))
        L += ["", f"## {title} ({len(g)})", "", why, ""]
        if g:
            e = g[0]
            L += [f"Exemplo mínimo: `{json.dumps(e['input'], ensure_ascii=False)}`", "",
                  f"- old: `{json.dumps(e['old'], ensure_ascii=False)}`",
                  f"- new: `{json.dumps(e['new'], ensure_ascii=False)}`"]
    L += ["", "## Como reproduzir", "", "```", "python3 -I gen_diffs.py diffs.jsonl diff-report.md", "```", "",
          "Determinístico: lista fixa de casos escritos à mão + casos aleatórios com `random.Random(SEED)`; rodar de novo gera arquivos idênticos."]
    open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(L) + '\n')

def main(out, rep=None):
    cases = gen()
    n, diffs = 0, []
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        for s in cases:
            o, w = run(old.parse, s), run(new.parse, s)
            if o != w:
                n += 1
                diffs.append({"input": s, "old": o, "new": w})
                f.write(json.dumps({"input": s, "old": o, "new": w}, ensure_ascii=False) + '\n')
    if rep:
        report(diffs, len(cases), rep)
    print(f"{len(cases)} cases, {n} differences -> {out}")

if __name__ == '__main__':
    main(*(sys.argv[1:3] or ['diffs.jsonl', 'diff-report.md']))
