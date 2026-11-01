# Card for module auditors
Repo root = cwd. Read claims.md rows for YOUR module only, and kit/<module>.py. Write ONLY checks/<module>.py.
Use `from _lib import *` after `sys.path.insert(0, dirname(__file__))` (see _lib.py; seed/generators are there, do not write your own RNG).
One function per claim, name it as dict key = claim id (e.g. 'T01'), decorated @exact (fixed inputs, return True or (False, detail)) or @prop (def f(r): draw inputs from r; return None if holds else a string with repr of the inputs). End file with `run({...})`.
Read each claim LITERALLY, including its quantifier ("any string", "every n>=0") and domain; a claim that holds only on a subset of its stated domain is falsa. For 'for any' claims use @prop with generators covering the stated domain (reuse ALPHABET/rand_*; extend domain-specific generators in your own file if needed, always from r). Property false => counterexample is the concrete failing inputs and actual output; shrink by hand if easy, else keep as found. Don't weaken a claim to make it pass; don't strengthen it to make it fail.
An @exact claim that is true needs actual call result compared; for exceptions the runner records falsa.
Run `python3 checks/<module>.py` twice and confirm identical output. Finish by replying with ONE line: module, count true/false. Do not paste output; results live in the script. Don't read other modules' files. If _lib lacks something, say so in the reply rather than editing it.
Reproduce command: `python3 checks/<module>.py <ID>` (one claim) or without args (all).
