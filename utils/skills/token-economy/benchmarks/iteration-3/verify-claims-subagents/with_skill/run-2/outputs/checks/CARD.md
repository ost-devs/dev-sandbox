Task: verify the claims of ONE module of calc/ (project root = parent of checks/).
Write ONLY checks/<module>_checks.py (and nothing else). Use checks/harness.py:
  from harness import claim, rng, run ; import calc.<module> ; @claim('T1') def f(): ... return None if true else 'counterexample string'
  end the file with: if __name__ == '__main__': run('<module>')
Rules: for each claim, actually execute the code. "for all" claims: exhaustive over a
meaningful domain when feasible, plus rng()-generated inputs (never unseeded random);
a single concrete counterexample suffices for false; for a true "for all" claim, also
include edge cases (empty, negatives, unicode, etc.). Counterexample string = the call and
actual result, minimal. A claim whose literal wording is true only if you read it
charitably: judge the literal wording. Run `python3 checks/<module>_checks.py` twice, confirm identical output.
Final reply to orchestrator: at most 1 line per claim: "ID verdict | counterexample". Nothing else.
