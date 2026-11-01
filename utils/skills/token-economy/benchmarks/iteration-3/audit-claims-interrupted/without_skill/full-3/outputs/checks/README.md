# Convention for checks/check_<module>.py
- stdlib only; run as `python3 checks/check_<module>.py [ID ...]` from the repo root (must also work with `-I`: insert repo root into sys.path from `__file__`).
- One function per claim ID. Fixed inputs, or random.Random(SEED) with SEED a module constant (property claims: >= 2000 cases plus hand-picked edge cases: '', unicode, negatives, zero, empty lists, etc.).
- Stdout: exactly one JSON line per claim: {"id":..., "verdict":"verdadeira"|"falsa", "counterexample": "<repr of minimal concrete input and actual vs claimed output>" or "", "note": ""}.
- An exception raised by the code on an input inside the claim's stated domain => the claim is falsa (counterexample = input + exception).
- Exit code 0 always when the script itself ran; nonzero only on harness error.
