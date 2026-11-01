Task: verify claims for ONE module of calc/ (see /tmp/.../claims.md rows for your module).
- Read your module's source (small). Write ONLY checks/<module>_check.py (no other files).
- Use `from common import run, SEED` (checks/common.py; run it as `python3 -I checks/<module>_check.py` from project root? -I drops script dir, so instead run `python3 checks/<module>_check.py`; the script must do sys.path insert of its own dir itself via common import by adding os.path.dirname(__file__)).
- One function check_<ID>(rng) per claim, returning (True,None) or (False,"counterexample"). Use rng (seeded, from common) for random inputs plus fixed edge cases; exhaustive when the domain is small. A claim is false if any valid input violates it; give the minimal concrete counterexample (repr). Exceptions on valid inputs count as falsification.
- Run it twice, confirm identical output. Reply with ONLY: per-claim lines `ID verdict counterexample` and the run command. No code dump.
