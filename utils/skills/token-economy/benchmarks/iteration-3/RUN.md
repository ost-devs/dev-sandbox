# Iteration 3 (2026-10-29): executed runs on Sonnet, with a decision rule fixed before the batch

- Skill version: `skill-snapshot/SKILL.md` (commit 119df14).
- Model: `claude-sonnet-5-5` for every run (orchestrator and subagents that inherit it), Claude Code 2.1.310.
- Isolation: `--setting-sources project,local`. Skills in `~/.claude/skills` are not loaded (checked: the without_skill list has no `token-economy`, mirrors or share-memories); `with_skill` has the skill at `.claude/skills/token-economy/` in its copy. Each run has its own fresh copy of the case `files/`.
- Runner: `../harness/batch.py` → `run_case.py` (run) + `grade_*.py` (programmatic grading, each grader tested with one must-pass and one must-fail input) → `compare.py` (statistics).
- Usage: read from the session transcripts (main + subagents), checked equal to `modelUsage` of `claude -p`. `units = input + 1.25·cache_write + 0.1·cache_read + 5·output` (the API price ratios), so units are proportional to cost on one model.

## Cases

| Case | What it is | Why it is here |
|---|---|---|
| `audit-claims-interrupted` | 152 claims about 8 modules, checks must re-run; subagents one per module | large enough for per-agent fixed cost; also run with a simulated usage limit |
| `verify-claims-subagents` | 24 claims, 4 modules (iteration 2 case) | cheap, same task shape |
| `parser-diff` | old vs new CSV line parser, ~200 generated inputs, reproducible | cheap, a different task (differential testing) |
| `triage-issues` | 80 issues: type + duplicates | cheap, many similar items, one small input |

Simulated usage limit (`audit-claims-interrupted`, interrupted runs): a watcher kills the whole run (orchestrator and subagents together) once usage passes `L` units, then the session is resumed with `claude -p --resume <id> "A sessão parou no meio porque bati no limite de uso. Continua de onde parou e termina a tarefa."`. `L` = half the mean units of the full runs of both configurations, set after the full runs and before the interrupted ones.

## Decision rule (written before the batch)

Per case, cost metric = units per run. `ratio = mean(with_skill) / mean(without_skill)`, 95% bootstrap interval (10 000 resamples, seed 1), exact permutation p-value.

- Interval contains 1: **páreo** if the interval is inside [0.9, 1.1], otherwise **inconclusivo**.
- Interval excludes 1, by how far the ratio is from 1 (ratio, or 1/ratio when the skill costs more): < 0.5 **abismo**; 0.5–0.75 **grande diferença**; 0.75–0.9 **diferença pequena**; 0.9–1 **quase páreo**.
- Quality is reported next to cost (pass rate and the raw grade). A cost gain with lower quality is reported as such, never as a win.
- Interrupted runs: compare total units (both phases) the same way, and the resume overhead: interrupted total minus the mean of full runs of the same configuration.
- The verdict is what the data says, including "no difference" or "the skill costs more".

## Pilot

See `pilot/`. Its runs are not part of the batch.
