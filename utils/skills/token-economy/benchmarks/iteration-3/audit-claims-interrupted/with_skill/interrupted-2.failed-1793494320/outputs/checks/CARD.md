# Card: auditing one module's claims
Repo root = cwd (/tmp/dev-home/.cache/token-economy-runs/audit-claims-interrupted-with_skill-a5c48fea).
1. Read `kit/<module>.py` and your 19 rows in `claims.md` (grep `| <module> |`). Do not read other modules.
2. Write ONLY `checks/<module>/check_<module>.py` using `checks/claimlib.py` (read its docstring; it has seeded generators, `claim`, `expect`, `main`). One @claim per id, all 19.
   - Judge each claim by RUNNING kit code, never by reading alone. Example claims: one fixed-input check. "For any ..." claims: search the generators (plus targeted edge cases you think of: empty, unicode, negatives, zero, boundaries); a single counterexample makes it falsa. Literal text of the claim is the spec; read it precisely (types, `n >= 0` ranges, `is True` vs truthy, int vs float).
   - Counterexample must be minimal-ish and concrete (inputs and actual output). Do not "fix" kit.
   - Randomness only via `rng(id)`; no time/network/global state.
3. Run `python3 checks/<module>/check_<module>.py` twice from repo root; outputs must be identical. It writes `checks/<module>/results.json`.
4. Sanity: for each claim you judged verdadeira, be sure the check could actually fail (not vacuous); for falsa, confirm the counterexample by hand once.
5. If claimlib lacks something you need, add a helper inside your own check file; do not edit claimlib.py. Report only if it's a general gap.
Final reply (<=5 lines): count verdadeira/falsa, ids of falsa, anything ambiguous in a claim's wording and how you read it. No tables, no code.
