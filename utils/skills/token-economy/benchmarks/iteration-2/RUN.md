# Iteration 2 (2026-10-29): executed run

- Skill version: commit e5037a2 (shared environment and helpers, evidence with seeds).
- Case: `evals/verify-claims-subagents` (24 claims about `files/calc/`, 11 false; answers in `truth.json`).
- Runner: Claude Code 2.1.310, `claude -p` with the default model (claude-opus-5-5), 2 runs per configuration, all four in parallel. Each run had its own copy of `files/`; `with_skill` also had the skill at `.claude/skills/token-economy/SKILL.md` (removed from this copy), `without_skill` had none.

```sh
cd <fresh copy of files/> && claude -p "$(sed -n '/^---$/,/^---$/!p' prompt.md | sed '/^Input files/d;/^$/d')" \
  --output-format json --permission-mode acceptEdits --allowedTools "Bash Read Write Edit Glob Grep Agent Skill" > result.json
```

- Per run: `result.json` (cost and tokens per model, including subagents), `outputs/` (report and checks), `auto_grade.json` (verdicts vs `truth.json`, every reproduce command run twice), `grading.json`.
- The checks inside `outputs/checks/` use recorded seeds: `python3 checks/...` from `outputs/` gives the same output again. The model runs themselves are not seeded.
- `review.html`: the skill-creator viewer, opens offline.
