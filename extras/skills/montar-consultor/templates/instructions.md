# Template: project instructions (`AGENTS.md` / `CLAUDE.md`)

Loads in full in every session, before anything else. Every line costs context
in every task, so it holds only what applies to every task.

## Which file
| Project has | Do |
|---|---|
| Nothing | Create `AGENTS.md` (read by Claude Code and other agents) |
| Only `AGENTS.md` | Edit it. Claude Code reads it natively when there is no `CLAUDE.md` |
| Only `CLAUDE.md` | Edit it; don't rename it without asking |
| Both | Claude Code reads only `CLAUDE.md`. Its first line must be `@AGENTS.md`; Claude-only notes go below it |

## Keep a line only if
- it applies to every task in the repo (else: a rule with `paths:`);
- it changes what the agent does (else: delete);
- the agent could not deduce it from a few reads of the repo (else: delete);
- it doesn't have to hold no matter what. What must always hold goes in a mechanism (settings `permissions`, a hook, CI), not prose.

Target under 200 lines (official guidance); most projects need 20 to 60.

## Skeleton

```markdown
# <project> - instructions for agents

<One sentence: what it is and who it is for.>

## Language
- <Language for code, commits, docs for humans, files for AI.>

## Sources of truth
- <The files that are the real configuration or spec. Docs point to them.>

## Workflow
- <Branch and commit rules. Validation every change needs, e.g. `npm test`.>
- <What cannot run in this environment and must be stated as untested.>

## Where to look
- How the project works and why: `/<project>` skill (`.claude/skills/<project>/`).
- <Docs index, if any.>
- Before ending a long session: `/consolidar`.
```

Drop any section that would be empty. Don't list the directory tree or the
stack: the agent sees both by itself.
