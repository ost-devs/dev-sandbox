# Card (read this, nothing else needed)
Task: verify your module's 6 claims from ../claims.md by RUNNING calc/<module>.py (read it once, it is ~25 lines).
- Write one script per claim: checks/<module>/check_<ID>.py, using checks/harness.py (see its docstring). Fixed inputs, or random ones via rng(tag) (seed is recorded). For "for all" claims: test edge cases (empty, negative, unicode, zero, boundaries) plus ~2000 random inputs; a single counterexample => falsa. For "true" verdicts on small domains, test exhaustively.
- Counterexample must be minimal and concrete (input -> actual vs expected).
- Run each script with `python3 -I checks/<module>/check_<ID>.py` from the repo root (-I is fine since harness path is inserted in the script via sys.path) and confirm running twice gives identical output.
- Write checks/<module>/results.jsonl (one harness line per claim, via a loop over your scripts) and checks/<module>/run.sh that reruns all of them.
- Write only inside checks/<module>/. Don't edit calc/ or harness.py (if something is missing, say so).
- Final reply: max 8 lines: per id verdict + counterexample (short). No code dumps.
