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

## Results (2026-11-01)

Batch finished; `compare.json`, `summary.txt`. Cost about US$ 18 (US$ 14.53 reported + killed phases, which report nothing + US$ 0.88 in four runs lost to a real usage limit, in `*.failed-*`, redone after the reset, not used). Isolation checked in every run: `skill_listing` present in all with_skill transcripts, absent in all without_skill.

| Group | n | Units ratio (95% CI), p | USD ratio (95% CI) | Quality | Verdict by the rule |
|---|---|---|---|---|---|
| audit, full | 4+4 | 0.871 (0.826-0.914), p=0.029 | 0.846 (0.794-0.895) | 152/152 in all | diferença pequena a favor da skill |
| audit, interrupted | 4+4 | 0.817 (0.687-0.969), p=0.114 | not available | 152/152 in all | diferença pequena a favor da skill (weak: p and interval disagree) |
| verify-claims | 6+6 | 1.081 (0.925-1.316), p=0.738 | 0.879 (0.703-1.008) | 24/24 in all | inconclusivo |

Reading:
- p=0.029 is the smallest possible with 4+4; a bootstrap on n=4 is optimistic.
- Resume overhead: +78k units (+20.7%) with the skill, +125k (+28.7%) without. The gap is inside the noise (sd about 70-76k, n=4 per group); the skill is not shown to reduce resume loss.
- The gain is mostly fewer output tokens in the audit (25-30k vs 32-42k, full runs).
- Seconds are not reported as a result: runs shared a parallel pool and the means hinge on outliers (240 s, 254 s).
- Deviation from the rule: units assume one model. verify-claims with_skill run-5 sent subagents to Haiku: 295k units but US$ 0.165, the cheapest run. This is why units and USD disagree in that case; without it, the units ratio is 0.97. USD added to `compare.py` after seeing this, so USD is a post hoc reading, not the pre-registered one. The cause of the Haiku choice was not examined.
- The pilot's 0.72 (n=1) overestimated the gain.
- Interruption: `L` = 203 138 units; kills landed at 203-245k because the watcher polls every 2 s.
- Grader limit: it re-runs commands and checks verdicts, not the depth of a check. Reports sampled by hand: `with_skill/interrupted-2`, `without_skill/interrupted-1`.
- `parser-diff` and `triage-issues` were not run in the batch; this iteration says nothing about tasks where the skill does not trigger.
