# Check-writing card
- One script per claim: `checks/<module>/check_<ID>.py`. Write only in your module's folder.
- Start with: `import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); from harness import rng, verdict, search`
  then import from `calc.<module>`.
- Fixed-value claims: compute the actual value and call `verdict(id, actual == expected, counterexample="got <actual>", method=...)`.
- "For every ..." claims: use `search(id, cases, prop, method)` with cases = hand-picked edge cases FIRST, then exhaustive ranges or `rng()`-generated inputs (default seed in harness.SEED; if you use another seed, state it in `method`). Exceptions count as violations.
- Counterexample: the smallest/clearest concrete input plus actual vs expected output.
- Must be deterministic: run each script twice, outputs must be identical. Run as `python3 checks/<module>/check_<ID>.py` from the workspace root.
- Do not edit calc/, harness.py or other folders. If the harness lacks something, say so in your reply instead of working around it.
- Reply ONLY with one line per claim: `ID | true/false | counterexample or - | command`. No other text.
