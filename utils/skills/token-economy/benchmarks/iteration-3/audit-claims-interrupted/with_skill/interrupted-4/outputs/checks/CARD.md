Task: verify claims of ONE module of kit/ by running code. Repo root = cwd.
1. Read kit/<module>.py and your 19 claims (grep '| <module> |' claims.md). Interpret each claim literally, including "for any/every" quantifiers.
2. Write checks/<module>.py with CHECKS = {'ID': fn} (one fn per claim), using checks/lib.py (seeded generators strings/ints/int_lists, first_fail, eq; read it, don't edit it). fn returns None if claim holds, else a short counterexample string. Universal claims: use generators (+ hand-picked edge cases) and report the concrete minimal-looking counterexample; a claim is 'verdadeira' only if sampled properly, 'falsa' needs a concrete counterexample. Fixed-value claims: eq().
3. Run `python3 -I checks/run.py <module>` and sanity-check each verdict against the code (a falsa must have a counterexample you understand; ensure checks aren't vacuous).
4. Write only checks/<module>.py and checks/results/<module>.tsv (output of the run, stdout redirected). Don't edit kit/ or other files.
5. Final reply to orchestrator: ONE line: counts true/false, and any helper gap. No claim details (they are in the tsv).
