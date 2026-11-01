Task: verify claims of ONE module of calc/ (see /…/claims.md rows for your module).
- Read only your module calc/<module>.py and your claim rows.
- For each claim ID write checks/<module>/<ID>.py using checks/common.py (see its docstring).
  Run as: python3 checks/<module>/<ID>.py  (from the project root). Inputs fixed, or from rng() (seed fixed in common.py).
  Exhaustive/range checks preferred over random where feasible. For "for all" claims, search for a counterexample
  (edge cases + seeded random); report the smallest/simplest one found. Claims with a stated domain: only test inside it.
  If the code raises on an input inside the claim's domain, that's a counterexample.
- Run each script twice, confirm identical output. Do NOT edit calc/.
- Write checks/<module>/results.jsonl (one JSON line per claim, from running the scripts).
- Final reply: max 8 lines, one per claim: ID verdict counterexample. No code, no logs.
