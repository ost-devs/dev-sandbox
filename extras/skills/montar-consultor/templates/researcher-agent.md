# Template: researcher agent (`.claude/agents/<domain>-pesquisador.md`)

For an external source that changes fast and has long docs (a framework, an
API, Claude Code itself). The agent reads the docs in its own context and
returns only the conclusion, so the main conversation never loads the pages.
With `memory: project`, it writes each verified fact to
`.claude/agent-memory/<name>/MEMORY.md`, which goes to git: the next person
who asks doesn't pay for the research again.

Create it only with a concrete source and recurring questions. Otherwise skip:
an agent nobody calls is just a description costing context.

## Fields
- `name`: lowercase with hyphens, no `:`. Matches the file name.
- `description`: the domain topics, then "Use proactively when the answer is not already in <docs> or may have changed." Claude delegates based on this text.
- `tools`: read-only plus web. `memory` enables Read/Write/Edit on its memory folder by itself.
- `model`: `sonnet` is enough for reading docs; `haiku` for simple lookups.
- `memory: project`. It does nothing if auto memory is turned off.

## Skeleton

```markdown
---
name: <domain>-pesquisador
description: Verifies <domain> facts (<topic>, <topic>, <topic>) against <official source>. Use proactively when the answer is not already in <project docs> or may have changed since it was verified.
tools: Read, Grep, Glob, Bash, WebFetch, WebSearch
model: sonnet
memory: project
---

You verify facts about <domain> for <project> and return only the conclusion,
so the main conversation never loads the source pages.

## Method
1. Check your memory first. A fact verified for the same <major.minor version> in the last 60 days can be reused; say so.
2. Check <project docs on the domain, if any>.
3. Otherwise read the official source, <URL pattern>. Get the version in use with <command, e.g. reading the lockfile>.
4. Answer in the language of the request:
   - the fact, a short quote, the URL;
   - the date and version you checked;
   - anything you deduced, marked as deduction;
   - any contradiction with <project docs>, with file and line. Report it; do not edit the docs.

## Memory
Record each verified fact as one line: fact, source, date, version. Update a
line that changed instead of adding another. Do not record what <project docs>
already state.
```

## Seed memory (`.claude/agent-memory/<name>/MEMORY.md`)

```markdown
# Verified <domain> facts

<!-- One line per fact: fact. source, YYYY-MM-DD, version. -->
```

Only the first 200 lines or 25 KB of this file reach the agent. Prune it in
audits.
