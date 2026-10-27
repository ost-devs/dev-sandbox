# Template: project map skill (`.claude/skills/<project>/SKILL.md`)

The knowledge that takes hours to rebuild: how the parts fit, decisions that
look wrong but have a reason, where each topic is written. Only its
`description` costs context at startup; the body loads when Claude judges the
topic relevant or the user types `/<project>`.

## Rules
- **A map, not a manual.** Each line points to the file with the details. Quote at most a line.
- **Under ~15,000 characters.** After compaction, an invoked skill comes back with its first 5,000 tokens only. Put what matters most first.
- **Facts with sources.** Every decision cites where its reason is written (doc, commit, issue). No source: ask the user or leave it out.
- **No `disable-model-invocation`.** Claude must be able to load it alone.
- **Not a copy of `CLAUDE.md`, the README or the rules.** Point to them.

## `description` (the trigger)
Claude decides from this text alone whether to load the map. Name the project,
say what it is in a few words, list what the map covers, and say when to use
it. Pattern:

> Working map of <project> (<what it is>) - how <main parts> fit, the non-obvious decisions behind them, and where each topic lives. Use before answering how <project> works, judging a change to it, or <domain questions>.

Keep it under ~400 characters (the listing truncates at 1,536, shared with `when_to_use`).

## Skeleton

```markdown
---
name: <project>
description: <see above>
---

# <project>: working map

Facts that cost reading time to rebuild. Details live in the files linked;
read them before quoting specifics. <Where the current version/status is.>

## Purpose
<2-4 lines: what it does, for whom, the main constraint that shapes it.>

## How it works
<The flow a change goes through, or the parts and how they talk. Numbered
steps or short bullets, each with the file that implements it.>

## Decisions that look wrong but are not
| Decision | Reason | Where |
|---|---|---|
| <what a newcomer would "fix"> | <why it is like that> | <doc, commit, issue> |

## Known open gaps
<Limitations people already know about, so the agent doesn't "discover" them again.>

## Where each topic lives
| Topic | File |
|---|---|
| <install / run> | <README.md> |
| <architecture, why> | <docs/...> |

## <Domain> questions
<Only if there is a researcher agent: 1. read <docs index>; 2. not covered or
possibly stale: delegate to `<name>` instead of fetching docs here.>
```

The "Decisions" table is the most valuable section: it holds what neither the
code nor the docs make obvious. Fill it from `git log`, code comments, and the
user's answer to "what would a newcomer get wrong?".
