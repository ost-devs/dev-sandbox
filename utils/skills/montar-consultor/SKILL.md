---
name: montar-consultor
description: Sets up or audits a project's "consultant" - the files that let a fresh Claude Code session know the project without an old conversation (CLAUDE.md/AGENTS.md, path-scoped rules, a project-map skill, /consolidar, an optional researcher agent). Run it in the project root.
disable-model-invocation: true
argument-hint: "[auditar]"
---

# Set up the project consultant

Goal: any fresh session in this project answers as precisely as a long session
that already knows it, at the lowest fixed context cost. Knowledge leaves the
conversation and goes to files Claude Code loads at the right moment.

Sources (read only when a step needs them):
- `${CLAUDE_SKILL_DIR}/templates/` - one template per piece, with the rules for writing it. Enough on its own.
- Worked example (optional): the `.claude/` of dev-sandbox, the repo where this was built. With the `mirrors` skill available and the user's OK, keep it current with the `mirrors` skill: `--add dev-sandbox https://github.com/ost-devs/dev-sandbox --include .claude --follow` (or a plain run if `mirrors/mirrors.json` already lists it), then read `mirrors/dev-sandbox/.claude/`. It shows the result, never content to copy: it describes another project. Without the `mirrors` skill, skip it.

`$ARGUMENTS` = `auditar`, or the project already has a map skill or `/consolidar`: skip to **Audit**.

## 1. Survey (read, write nothing)

Collect facts, citing the file each came from:

1. Existing instructions: `CLAUDE.md`, `.claude/CLAUDE.md`, `CLAUDE.local.md`, `AGENTS.md` (root and subdirs), `.claude/` (rules, skills, agents, settings), `.cursor/rules`, `.github/copilot-instructions.md`. Note size (`wc -l -c`).
2. What the project is: `README*`, manifests (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Dockerfile`, compose, CI under `.github/workflows`), top two levels of the tree (`git ls-files | cut -d/ -f1-2 | sort -u | head -100`).
3. How to validate a change: test, lint, build, typecheck commands; what cannot run here.
4. Parts with their own rules: dirs whose changes need different checks or force updates elsewhere (API + client, schema + migrations, script + its docs).
5. Non-obvious decisions: `git log --oneline -200` (look for fix, revert, "because"), comments with `NOTE|HACK|WHY|porque|because`, ADRs, "why" sections in docs.
6. Docs: where they live, their language, whether there is an index.
7. Fast-changing external dependency with big docs (a framework, an API, Claude Code itself, a regulation) that people ask about often: candidate for a researcher agent. Note whether its docs can be mirrored: a git repository (often a `docs/` folder), or a site whose `llms.txt` links `.md` pages (`curl -s <site>/llms.txt | grep -c '\.md)'`).
8. Workflow: branch and commit conventions, from instructions and `git log`.

Big repo (over ~300 tracked files): delegate the sweep to an Explore agent and ask for the list above as the answer. Explore does not load CLAUDE.md, so put any rule it needs in the prompt.

**This session already worked on the project?** That knowledge is the most valuable input and the reason this skill exists: add the decisions, corrections and discoveries from this conversation to the facts, marked "from this session".

## 2. Ask only what the files cannot answer

One `AskUserQuestion` call, at most 4 questions. Typical:
- What would a new developer (or a fresh Claude) most likely get wrong here?
- Which pieces to create (pre-check the ones the survey justifies; table in step 3).
- Researcher agent: which external source, if the survey found a candidate.
- Language of AI-facing files: English (fewer tokens, the default) or the team's language.

Skip a question when the survey already answered it.

## 3. Plan and confirm

Decide each piece with this table:

| Piece | File | Create when | Template |
|---|---|---|---|
| Project instructions | `AGENTS.md` and/or `CLAUDE.md` | Always (edit, don't replace, if it exists) | `templates/instructions.md` |
| Path-scoped rule | `.claude/rules/<part>.md` with `paths:` | A part has its own validation or a "changed X, also update Y" list | `templates/rule.md` |
| Project map skill | `.claude/skills/<project>/SKILL.md` | Understanding the project takes reading several files | `templates/map-skill.md` |
| Session closer | `.claude/skills/consolidar/SKILL.md` | Always | `templates/consolidar.md` |
| Docs mirror | `mirrors/<name>/` through the `mirrors` skill (only `mirrors/mirrors.json` goes to git) | There is a researcher and its source can be mirrored (step 1.7), and the `mirrors` skill is installed. A local grep quotes exactly; web fetching truncates long pages and may summarize instead of quoting | `mirrors` skill: `--add <name> <git url or site/llms.txt> [--include <path>]` |
| Researcher agent | `.claude/agents/<domain>-pesquisador.md` + `.claude/agent-memory/<name>/MEMORY.md` | A fast-changing external source with big docs (step 1.7) | `templates/researcher-agent.md` |

Small project (a few files, one stack): instructions + `/consolidar` may be enough. Say so instead of creating empty pieces.

Show the user one table: file, create/edit, what goes in it (one line), approximate size. If the project has instructions already, list what moves where (e.g. "file-specific checklist → rule"). Wait for approval before writing.

## 4. Write

Read the template for each piece, then write it from the survey facts. For every piece:
- **Point, don't copy.** Link to the file that holds a fact; quote at most a line. Copies drift.
- **One fact, one place.** If it fits a rule, it leaves `CLAUDE.md`.
- **Only what changes behavior and can't be deduced** from the repo in a few reads.
- **Nothing invented.** A fact without a source from step 1 or the user stays out, or goes in marked as a question for the user.
- Existing content: move it, don't duplicate it; never drop a user's line without listing it in the report.

Order: rules, map skill, docs mirror, researcher, `/consolidar` (its routing table names the pieces that now exist), instructions last (they may point to the others).

Claude Code protects `.claude/`: each write there asks the user, and non-interactive runs refuse it. If a write is refused, stop and report; never write instructions that point to files that don't exist, and never write through Bash to get around it.

## 5. Verify

1. Frontmatter parses: `---` first line, `name`/`description` present, `paths` globs match real files (`git ls-files '<glob>' | head -3` for each).
2. Sizes: `wc -l -c` on each file. Limits: `CLAUDE.md`/`AGENTS.md` under 200 lines (official target), map `SKILL.md` under ~15,000 characters (re-attach after compaction keeps 5,000 tokens per skill), `/consolidar` under 60 lines.
3. Every path cited in the new files exists (`ls` them).
4. Propose a fresh-session test: three real questions whose answers are in the map, not in `CLAUDE.md`. Command, run from the project root:
   `claude -p --no-session-persistence "<question>. At the end, list the skills and files you read."`
   Run it only if the user agrees (it costs a session). Without a run, give the command in the report.

## 6. Report and commit

- Table: file → created/edited → what it holds → size.
- What you left out and why, and questions the user must answer to complete the map.
- How to use it: new conversation per topic; `/<project>` if an answer looks generic; `/consolidar` before `/clear`; `/context` shows what loaded.
- Commit following the project's own rules (branch, message language). No rules: ask before committing. Never push.

## Audit

For a project that already has the consultant. Read every piece and check:

| Check | Fix |
|---|---|
| Fact repeated in two pieces | Keep it in the most specific one |
| Path cited that no longer exists, or map out of date with `git log` since the map's last commit (`git log --oneline $(git log -1 --format=%h -- .claude/skills) ..`) | Update or delete the line |
| `CLAUDE.md` line that applies only to some files | Move to a rule |
| Content copied from a doc | Replace with a pointer |
| Map over the size limit | Cut what the linked docs already say |
| Researcher memory facts older than 60 days or a previous major.minor | Mark for re-check |
| Docs citing official pages that changed since the doc's last commit (docs mirror of a site or of web articles) | List them with the `mirrors` skill: `--stale <mirror> <docs folder>`; recheck each with the researcher |

Report findings as a table (problem → file:line → proposed fix) and apply only after the user agrees.
