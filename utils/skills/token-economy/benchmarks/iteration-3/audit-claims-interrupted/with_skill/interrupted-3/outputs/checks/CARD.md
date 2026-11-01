# Card for module-audit agents
Repo root = cwd. Your module: given in prompt. Read `kit/<module>.py` and your 19 rows in `claims.md` (grep `| <module> |`). Do NOT read other modules or other agents' folders.
Read `checks/_lib.py` docstring (helpers: Checker, rand_strings/ints/floats/lists with seed). 
Write ONLY `checks/<module>/check_<module>.py` (one `@c.claim` per id, all 19 ids). Run it: `python3 -I checks/<module>/check_<module>.py` (cwd = repo root; stdlib only, no hypothesis/pytest).
Rules:
- Every verdict comes from running code. Fixed inputs, or generated with a seed literal in the file. Same output every run (run twice, confirm identical).
- A claim is "verdadeira" only if no counterexample is found over fixed edge cases + seeded random; for universal claims ("for any s") include edge cases (empty, unicode, whitespace, negatives, 0, boundaries). If the code reading suggests a counterexample, construct it and make the check fail with it.
- Interpret each claim literally as written; if ambiguous, take the literal reading and put the note in `note`.
- Counterexample must be minimal, concrete and shown in the output (the repr).
- Don't modify kit/. If a helper is missing in _lib.py, report it instead of editing it.
- Results are written to checks/<module>/results.json by c.main(). Write the file early (stub then fill) so a crash loses little.
Final reply (<=6 lines): module, count true/false, list of false ids with one-line counterexample, any issue. No other prose.
