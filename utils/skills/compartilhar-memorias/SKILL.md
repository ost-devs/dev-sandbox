---
name: compartilhar-memorias
description: Shares Claude Code auto-memories between projects - all of them, a list, or a category such as dev - and keeps them in sync (one copy, linked into each project). Use when a hook reports a new memory in a project that belongs to a shared-memory group, when the user wants to share, unshare, group or check memories across projects, or when it reports a sharing conflict.
argument-hint: "[status | compartilhar <memória> <grupo> | descompartilhar <grupo>/<arquivo> | grupos]"
allowed-tools: Bash(python3 *compartilhar.py*)
---

# Shared memories

Memory creation is not yours to change here: write memories exactly as usual.
This skill only decides, afterwards, whether a memory also belongs to other
projects. `python3 "${CLAUDE_SKILL_DIR}/compartilhar.py"` does the moving; you
do the judging.

How it works: a shared memory has one copy in
`~/.claude/memorias-compartilhadas/<group>/`. Each member project's `memory/`
has a relative symlink to it, and its `MEMORY.md` lists it in a generated block
(`compartilhar-memorias:inicio` … `fim`). Never edit that block; edit the
memory. Write and Edit refuse to write through the symlink and name the target:
write to the target, and the change reaches every project. Hooks re-link and
refresh the blocks; new projects of a group get the links at their first session.

## Deciding about a new memory

A hook says "New memory `x.md`" when the project is in a group. Finish the
current step first, then read the memory and the groups (`status`) and pick one:

| The memory | Do |
|---|---|
| Needs this project to make sense: its files, paths, decisions, deadlines, people, versions | Nothing. It stays local. Say nothing |
| Holds as written for most projects of a group | `compartilhar <path> <group>`, then tell the user in one line, including how to undo |
| Has a general lesson inside project-specific wording | Propose a rewrite (below) |
| Is a short rule that must apply in every session of every project | Suggest moving it to `~/.claude/CLAUDE.md` instead: it loads whole, a memory only loads when recalled |

The bar: every shared memory adds an index line to every session of every
member, and a memory read in a project where it doesn't fit misleads. Share
when you would expect it to be used in most members, not merely to be true
there. `user` and `feedback` memories are usual candidates, `reference`
sometimes, `project` rarely. Pick the narrowest group that fits. When unsure,
keep it local: sharing later is one command, an unneeded line costs every day.

## Rewriting for the group (only with the user's permission)

1. Show the user the current text and the proposed one, and the group.
2. Keep what makes it actionable: the rule, the **Why**, the **How to apply**,
   and one concrete example even if it comes from this project. Remove only
   what is meaningless elsewhere (local paths, file names, ticket numbers).
3. If the general version loses something this project needs, split: share the
   general part and keep a short local memory with the specific remainder,
   linking `[[the-shared-name]]`. If nothing useful survives generalizing,
   keep it local.
4. Write the approved text to the memory file, then run `compartilhar`.

Without an answer, leave the memory local and unchanged.

## Commands

| Task | Arguments |
|---|---|
| Groups, members, shared memories, pending fixes, hook check | `status` |
| Share (moves the file, links it in all members) | `compartilhar <absolute path of the memory> <group>` |
| Unshare: delete, or keep a plain copy in one project | `descompartilhar <group>/<file>.md [--manter <project folder>]` |
| Repair links and blocks (after a manual change in `grupos.json` or files) | `sincronizar [--projeto <project folder>]` |

A project folder is the name under `~/.claude/projects/` (the memory path shows it).

## Groups

`~/.claude/memorias-compartilhadas/grupos.json`, edited with the user:

```json
{"grupos": {"todos": ["*"], "dev": ["-dev-sandbox", "-ferrum", "/home/me/Dev/*"]}}
```

An entry is a project folder name or a project path; `*` matches anything, so
`["*"]` is every project. Membership is by folder, so a project opened at
another path (`dev-docker --nome`, a moved repo) is another member. After
editing the file, run `sincronizar`. To move a memory between groups:
`descompartilhar g/x.md --manter <one member>`, then `compartilhar` it again.

## Conflicts

`status` and the hooks report a member that has a plain file with the same name
as a shared memory but different content. Show the user both, merge into the
shared copy (or rename the local one), delete the local file, run `sincronizar`.

## Setup (once)

Copy this folder to `~/.claude/skills/`, create `grupos.json`, and add to
`~/.claude/settings.json` (merge with existing `hooks`):

```json
"hooks": {
  "PostToolUse": [{"matcher": "Write|Edit", "hooks": [{"type": "command",
    "command": "python3 \"$HOME/.claude/skills/compartilhar-memorias/compartilhar.py\" hook"}]}],
  "SessionStart": [{"hooks": [{"type": "command",
    "command": "python3 \"$HOME/.claude/skills/compartilhar-memorias/compartilhar.py\" hook"}]}]
}
```

Without the hooks nothing syncs on its own; `status` warns about it.
