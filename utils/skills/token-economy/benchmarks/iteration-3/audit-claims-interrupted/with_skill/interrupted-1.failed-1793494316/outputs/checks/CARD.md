# Card for module auditors
Project dir: cwd. Claims: `claims.md` (rows with your module's prefix/module name). Code: `kit/<module>.py` (read it; small).
Write ONLY in `checks/<module>/`. Create `checks/<module>/run.py` using `checks/lib.py` (read it first):
  import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')); from lib import *
  from kit import <module>; R=Runner('<module>'); R.claim('T01', lambda: expect(lambda: ..., ...)); ...; R.main()
- Example claims: `expect(fn, expected)`. Universal claims ("for any s"): `find_counterexample(id, gen, pred)` with generators from lib (seeded, N=2000, fixed alphabet incl. unicode/edge cases). Choose generators that can actually reach the edge cases the claim covers (empty, negatives, zero, unicode, duplicates...); read the code to aim them. Interpret the claim literally; state-domain exactly as written (e.g. "n >= 0").
- A claim is 'verdadeira' only if no counterexample found; 'falsa' needs a concrete minimal-ish counterexample (shrink by hand to a short input).
- Run: `python3 -I checks/<module>/run.py` (all 19 claims, writes results.json). Must be deterministic: run twice, results.json must be identical.
- Do not edit kit/, lib.py or claims.md. If lib is missing something, report it in your final message instead.
- Final message (<=6 lines): path to results.json, count true/false, and list of FALSE ids only. No tables, no code.
