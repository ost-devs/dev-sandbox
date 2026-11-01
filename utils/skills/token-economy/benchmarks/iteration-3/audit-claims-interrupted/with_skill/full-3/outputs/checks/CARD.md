# Card for module agents
Task: for ONE module, verify all 19 claims in /tmp/dev-home/.cache/token-economy-runs/audit-claims-interrupted-with_skill-d36c213e/claims.md (rows whose module column matches) by RUNNING kit/<module>.py.
Write ONLY in checks/<module>/ . Do not edit kit/, claims.md or checks/lib.py (if lib lacks something, say so in your final message).
1. Read kit/<module>.py and your 19 claim rows (grep the module; nothing else).
2. Write checks/<module>/check_<module>.py using `from lib import Checker` (add `sys.path.insert(0, <checks dir>)` via __file__). One c.fixed or c.prop per claim id, exactly 19 results. Universal claims ("for any s") -> c.prop with a generator (seeded automatically from the id) AND, if you suspect falsity, a hand-picked fixed case; claims about specific values -> c.fixed. Read the claim literally; do not "fix" a claim's wording in your favor. Look in the code for the edge case a claim overlooks, then confirm by running.
3. Run: `python3 checks/<module>/check_<module>.py` (cwd = repo root). It writes checks/<module>/results.json. Run it twice; output must be identical.
4. Write results incrementally (create the script early, extend it). Final message to orchestrator: max 5 lines — count true/false, the ids that are false, any problem. No tables, no code.
