# Card for module-check agents
Task: for EVERY claim of your module in /…/claims.md (19 each), write a reproducible check and run it.
- Work ONLY in checks/<module>/ (create it). Single file: checks/<module>/check_<module>.py, plus results.json it generates.
- Start the file with: `import sys,os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..')); from lib import *; from kit.<module> import *` and end with `if __name__=='__main__': main('<module>')`.
- One `@claim("X01")` function per claim. Fixed inputs for example claims (assert ==); for "for any/every" claims use `forall(id, gen, pred)` with the seeded generators in checks/lib.py (read it, ~60 lines). Do not use unseeded randomness. Claim states a domain (e.g. n>=0, non-empty)? Respect exactly that domain.
- A claim is falsa only with a concrete counterexample; make Counter messages show the minimal-ish input and actual vs expected. Property claims: also try edge cases (empty, unicode, negatives, zero, large) in the generator so a false claim is found.
- Read kit/<module>.py to understand, but the verdict comes from running. Read claim text literally (e.g. exact return values, types, 'never', 'always').
- Run from project root: `python3 checks/<module>/check_<module>.py`. Do NOT modify kit/ or lib.py (if lib lacks something, put a local helper in your file, and mention it).
- Final reply (≤5 lines): count verdadeira/falsa, ids of false ones, anything odd. No tables, no code.
