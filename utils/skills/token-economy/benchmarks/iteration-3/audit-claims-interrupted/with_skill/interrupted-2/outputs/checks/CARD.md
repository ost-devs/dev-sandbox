# Card for module agents
Task: for ONE module (your claims = rows in claims.md with that module), verify every claim by running kit code.
- Read only kit/<module>.py and your 19 rows of claims.md.
- Write ONLY checks/check_<module>.py (copy checks/check_text.py skeleton; replace the TODO). Use helpers in checks/lib.py (claim, forall, gen_*, eq, rng). Do not edit lib.py; if something is missing, say so in your report.
- One @claim("ID") function per claim; return None if true, else a counterexample string (concrete inputs + actual output). For "for any/every" claims use forall with generators that can reach edge cases (empty, unicode, negatives, boundaries); a claim is false if a single counterexample exists. Fixed-example claims: call the code and compare exactly (watch types, e.g. 1 vs 1.0 vs True only if the claim implies it).
- Judge the claim as literally written; if ambiguous, state the interpretation in a comment in the check.
- Prefer a minimal, shrunk counterexample for false claims (try small inputs).
- Run `python3 checks/check_<module>.py` from repo root; it writes checks/results/<module>.json. Run twice and confirm identical output.
- Final reply to orchestrator: max 5 lines: counts true/false, any lib gap. No tables (the results json holds them).
