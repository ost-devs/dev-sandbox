# Trigger test 1 (2026-10-29)

Skill installed for real (symlink `.claude/skills/token-economy` -> `utils/skills/token-economy`), Claude Code 2.1.310, `claude-opus-5-5`, cwd `/dev-sandbox`, skill at commit 185795c.

- `seq-1.json`: queries 0,1,4,7,13 once, `--max-turns 8`.
- `seq-2.json`: the other 15 twice, `--max-turns 2` (the trigger shows in the first actions).
- Command: `python3 trigger_seq.py ../../evals/trigger-eval.json <indices> out.json`.

skill-creator's `run_eval` (a fake command in `.claude/commands`) gave 0/60 here, even for clear cases: the model doesn't call that command in this CLI version. Don't use it or `run_loop` for this skill.

Result: no false trigger in 19 runs of the 10 negatives (two went to `claude-api`, as they should). Positives triggered in 9 of 16 runs: 0,1,4,7 (1/1), 6 (2/2), 3,8,9 (1/2), 2,5 (0/2). The misses started by exploring with Bash; with `--max-turns 2`, a later trigger isn't seen.
