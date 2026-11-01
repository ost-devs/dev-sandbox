"""Shared helper for checks. Usage in checks/<module>/check.py:
    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    from common import rng, report
    r = rng('T1')            # deterministic random.Random, seeded by SEED + claim id
    report('T1', True)                       # verdadeira
    report('T1', False, "slugify('-')=...")  # falsa + counterexample
Output line: `<id>\t<VERDADEIRA|FALSA>\t<counterexample>`; also exit code 0 always.
"""
import os, sys, random, zlib
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT)
SEED = 20261101  # registered seed

def rng(claim_id):
    return random.Random(SEED * 1000003 + zlib.crc32(claim_id.encode()))

def report(claim_id, ok, counterexample=''):
    print(f"{claim_id}\t{'VERDADEIRA' if ok else 'FALSA'}\t{counterexample}")
