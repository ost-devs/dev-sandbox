"""Harness comum. Cada checagem é uma função registrada com @claim('ID') que
devolve None quando a afirmação se sustenta e uma string (contraexemplo) quando não.
Aleatoriedade: sempre via rng(id) -> random.Random(f'{SEED}:{id}'), determinística."""
import itertools
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

SEED = 20261029
REGISTRY = {}


def claim(cid):
    def deco(f):
        REGISTRY[cid] = f
        return f
    return deco


def rng(cid):
    return random.Random(f'{SEED}:{cid}')


def eq(label, fn, expected):
    try:
        got = fn()
    except Exception as e:
        return f'{label} levantou {e!r}; esperado {expected!r}'
    if got != expected or type(got) is not type(expected) and not (
            isinstance(got, (int, float)) and isinstance(expected, (int, float))):
        return f'{label} = {got!r}; esperado {expected!r}'
    return None


def raises(label, fn, exc):
    try:
        got = fn()
    except exc:
        return None
    except Exception as e:
        return f'{label} levantou {e!r}; esperado {exc.__name__}'
    return f'{label} = {got!r}; esperado {exc.__name__}'


def forall(cases, prop):
    """prop(*case) -> True/None se ok; False ou string (detalhe) se falha. Exceção = falha."""
    n = 0
    for c in cases:
        n += 1
        c = c if isinstance(c, tuple) else (c,)
        try:
            r = prop(*c)
        except Exception as e:
            return f'entrada {c!r} levantou {e!r}'
        if r is not True and r is not None:
            return f'entrada {c!r}' + (f': {r}' if isinstance(r, str) else '')
    assert n > 0, 'nenhum caso gerado (checagem vacua)'
    return None


ALPHA = list('abcXYZ019 -_.,;:!?\t\n/') + ['é', 'ç', 'ã', 'Ç', 'ß', 'ø', 'İ', 'K', 'ñ', 'Ω', '日']
EDGE_STR = ['', ' ', '-', 'a', 'A', 'ab', 'Café Noir', 'ß', 'ßa', 'ø', 'İ', '--a--', 'é', 'a b', '  ', 'Ação']


def strings(cid, n=4000, maxlen=12):
    r = rng(cid)
    out = list(EDGE_STR)
    for _ in range(n):
        out.append(''.join(r.choice(ALPHA) for _ in range(r.randint(0, maxlen))))
    return out


def main(module_globals_marker=None):
    ids = sys.argv[1:] or sorted(REGISTRY)
    bad = 0
    for cid in ids:
        if cid not in REGISTRY:
            print(f'{cid}\tDESCONHECIDO\t')
            bad = 1
            continue
        ce = REGISTRY[cid]()
        print(f'{cid}\t{"VERDADEIRA" if ce is None else "FALSA"}\t{(ce or "").replace(chr(10), " ")}')
    return bad
