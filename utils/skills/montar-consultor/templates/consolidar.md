# Template: session closer (`.claude/skills/consolidar/SKILL.md`)

The habit that keeps the consultant alive: before `/clear` or ending a long
session, the user types `/consolidar` and what the session learned moves to
the files. `disable-model-invocation: true` keeps it out of the context until
then.

Copy the block below. Edit only the routing table: one row per piece that
exists in this project (drop rows for pieces you didn't create, rename paths).

```markdown
---
name: consolidar
description: Before /clear or ending a long session, moves what this session learned into the place a new session will read, so nothing depends on this conversation.
disable-model-invocation: true
---

# Consolidate this session

Goal: a fresh session must be as precise as this one without reading it.

1. List what this session established that a fresh session would not know: decisions and their reasons, discoveries, user corrections and preferences, state of unfinished work.
2. Drop every item a fresh session can deduce from the repo, `git log` or the environment.
3. Route each remaining item to exactly one place. Update or delete stale entries there before adding new ones.

| Item | Place |
|---|---|
| User preference or correction about how to work | Auto memory (personal, not in git) |
| Rule for every task in this repo | `<AGENTS.md or CLAUDE.md>` (keep it short) |
| Rule for some files only | `.claude/rules/*.md` with `paths:` |
| How <project> works, a decision and its reason, where a topic lives | `.claude/skills/<project>/SKILL.md`, if it isn't already in a doc it can point to |
| Non-obvious discovery others could hit | `<docs folder for learnings, or the map's Decisions table>` |
| Verified <domain> fact | Memory of `<researcher agent>` |
| Unfinished work | Commit it on its branch and keep one project memory: branch, next step, date. Delete it when done |

4. Show the user a table: item → where it went. Ask before committing if the user has not authorized commits.
5. Tell the user it is safe to `/clear`.
```
