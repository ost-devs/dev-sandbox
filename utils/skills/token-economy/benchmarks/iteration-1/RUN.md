# Iteration 1 (2026-10-29)

- Skill version: commit c440e06 (`SKILL.md` before the shared-harness and seed points).
- Cases: `evals/split-audit-subagents`, `evals/insurance-request`, `evals/cut-quality-request` (planning only: each run writes `plan.md`, executes nothing).
- Runner: Claude Code 2.1.310, model claude-opus-5-5, one `general-purpose` subagent per case and configuration, 1 run each. `with_skill` read `SKILL.md` first; `without_skill` had no skill.
- Grading: by the orchestrating session against each case's `graders/` (`grading.json`, with evidence).
- `review.html`: the skill-creator viewer (outputs + benchmark), opens offline.
- Model runs are not seeded: re-running gives similar, not identical, plans. Compare pass rates and tokens, not wording.
