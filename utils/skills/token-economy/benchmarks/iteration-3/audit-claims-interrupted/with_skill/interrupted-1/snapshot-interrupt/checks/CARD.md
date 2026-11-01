# Card for module-audit agents
Project root: /tmp/dev-home/.cache/token-economy-runs/audit-claims-interrupted-with_skill-361eb7dc
Your job: for your module M, verdict each of the 19 claims in claims.md (rows with module M) by RUNNING code.
1. Read kit/M.py and your 19 claim rows only (grep `| M |` claims.md). Don't read other modules.
2. Write ONLY in checks/M/ : check_M.py, using checks/common.py (read it first; it's short). Layout:
   import os,sys; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
   from common import *; from kit import M
   define one function per claim id returning None (holds) or a counterexample string; then `run('M', {'X01': f1, ...})`.
   - Fixed-input claims: use eq(lambda: ..., expected). Property claims ("for any/every ..."): use forall(tag, gen, pred) with
     generators respecting the claim's stated domain (e.g. n>=0, non-empty) but covering edge cases (empty, unicode, negatives, zero, duplicates, boundaries). Add targeted edge inputs too, since random may miss them.
   - Read the claim literally (types, equality strictness, stated domain). A claim is 'falsa' if any input in its domain violates it; the counterexample must be a concrete minimal input shown.
   - Verdicts must come from the run, not from reading the code. If the code crashes on a valid-domain input, that is a counterexample.
3. Run `python3 checks/M/check_M.py` from project root (writes checks/M/results.json, prints id/verdict/counterexample). Run it twice and confirm identical output.
4. Final reply to orchestrator: ONE line, e.g. "M: 19 done, N false: ids" — nothing else. Don't paste tables; results.json is the record.
Reproduce command for each claim in the report: `python3 checks/M/check_M.py ID`.
