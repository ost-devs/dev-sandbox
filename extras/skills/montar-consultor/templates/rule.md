# Template: path-scoped rule (`.claude/rules/<part>.md`)

Costs nothing until Claude reads or edits a file matching `paths:` (Read,
Write, Edit, or a single-file Bash read such as `cat`). Then it loads and stays
for the session. A rule without `paths:` loads always: avoid that, use
`CLAUDE.md` instead.

## One rule per part
A part is a set of files that share checks: `src/api/**` + `openapi.yaml`;
`migrations/**` + `models/**`; `docs/**`. Name the file after the part.
Subfolders under `.claude/rules/` are allowed.

## `paths:` syntax
- YAML list of globs, relative to the folder that holds `.claude/`.
- `**` any depth; `{ts,tsx}` alternatives; a literal `[` needs `\[`.
- Check each glob matches real files: `git ls-files '<glob>' | head -3`.

## Content: only what someone touching these files needs

```markdown
---
paths:
  - "<glob>"
  - "<glob>"
---

# Changing <part>

## Validate
- <Exact command(s) to run after a change, e.g. `pnpm test api`.>
- <What can't be tested here and must be reported as untested.>

## Propagate (one change, every place that describes it)
| Changed | Also update |
|---|---|
| <file or kind of change> | <docs, client, changelog, the map skill...> |
| How the parts fit, or a decision and its reason | `.claude/skills/<project>/SKILL.md` |

## Conventions
- <Only non-obvious ones: naming, error handling, a trap that already bit someone.>
```

Drop empty sections. 10 to 40 lines is typical. If two rules repeat a line,
the line probably belongs in `CLAUDE.md`.
