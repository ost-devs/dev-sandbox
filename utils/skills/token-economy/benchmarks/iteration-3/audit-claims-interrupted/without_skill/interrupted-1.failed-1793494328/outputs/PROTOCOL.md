# Audit protocol (shared by all module agents)

Root: /tmp/dev-home/.cache/token-economy-runs/audit-claims-interrupted-without_skill-1fb58fa5
Task: for ONE module of `kit/`, verify each of its 19 claims in `claims.md` (rows whose module column matches) by RUNNING the code. Do not edit `kit/` or `claims.md`. Only write inside `checks/`, and only your own module's files.

## Deliverables
1. `checks/check_<module>.py` — python3 stdlib only. Usage from root:
   - `python3 -I checks/check_<module>.py` runs all 19 claims;
   - `python3 -I checks/check_<module>.py <ID>` runs one.
   Each claim prints one line: `<ID>\tTRUE` or `<ID>\tFALSE\t<counterexample as repr, with actual vs expected>`. Exit code 0 always (the verdict is in the output). Must be deterministic: fixed inputs, exhaustive enumeration over the stated domain when it is finite and reasonable, or `random.Random(SEED)` with the SEED constant written at the top of the file/claim. Import kit via sys.path insertion of the root computed from `__file__` (so it works from any cwd; run with `-I`, so do not rely on cwd).
2. `checks/results_<module>.tsv` — header `id\tverdict\tcounterexample\tcommand`; verdict is `verdadeira` or `falsa`; command is `python3 -I checks/check_<module>.py <ID>`. Generate it from the script's actual output, not by hand.

## Rules for verdicts
- A claim is FALSE if you find any input within the claim's stated domain where it fails (including exceptions raised where the claim says it returns a value). Report a minimal concrete counterexample. Read the source to hunt for edge cases (empty, negative, unicode, zero, huge, boundary), then confirm by running. Random testing alone is not enough; combine with targeted edge cases.
- A claim is TRUE only if it held on the full check (exhaustive where stated finite, otherwise adversarial + seeded random with substantial volume, e.g. >=2000 cases). Judge the claim as literally written, including its stated domain; do not "fix" the claim's wording.
- For a FALSE verdict, the check must reproduce the counterexample deterministically (fixed input in the script).
- Run the script twice and confirm identical output.

## Final reply
Short: path of files written, and the list `ID verdict` for the 19 claims (counterexamples in one short line each for the false ones). No long prose.
