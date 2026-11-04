---
name: share-memories
description: Shares Claude Code auto-memories between projects - all of them, a list, or a category such as dev - and keeps them in sync (one copy, linked into each project). Use when a hook reports a new memory in a project that belongs to a shared-memory group, when the user wants to share, unshare, move, group, review or check memories across projects (including the review notes nota.md beside groups.json), or to install it.
argument-hint: "[status | share <group> <memory>... | unshare <group>/<file>... | move <group> <group>/<file>... | line <group>/<file> | group <name> | install]"
allowed-tools: Bash(python3 *share_memories.py*)
---

# Share memories

Memory creation is not yours to change here: write memories exactly as usual.
This skill only proposes, afterwards, that a memory also belongs to other
projects, and the user decides. `python3 "${CLAUDE_SKILL_DIR}/share_memories.py"` does the moving.

How it works: a shared memory has one copy in `~/.claude/shared-memories/<group>/`.
Each member project's `memory/` has a relative symlink to it, and its `MEMORY.md`
lists it in a generated block (`share-memories:start` … `end`). The line is the
one Claude wrote for it (title and summary, kept in `groups.json` at share time),
tagged `_(shared, group <g>)_`: the block's comments are stripped when MEMORY.md
loads, so the tag is how you know an edit reaches other projects. Never edit that
block; edit the memory, or its line with `line`. Write and Edit refuse to write through the symlink and
name the target: write to the target, and the change reaches every project.
Hooks re-link and refresh the blocks; new projects of a group get the links at
their first session.

## Deciding about a new memory

Where a memory belongs is the user's call: their criteria are personal, and a
question in the middle of a task gets a tired "yes". So you never share on your
own and never ask mid-task. You propose, in writing, for a batch review.

A hook says "New memory `x.md`" when the project is in a group. Finish the
current step first, then read the memory and the groups (`status`) and pick one:

| The memory | Do |
|---|---|
| Needs this project to make sense: its files, paths, decisions, deadlines, people, versions | Nothing. It stays local. Say nothing |
| Would serve most projects of a group, as written or rewritten | Add it as a candidate to `nota.md` (below), then one line at the end of your reply: "candidata em nota.md", in the user's language. No question |
| Is a short rule that must apply in every session of every project | Same, and say in the candidate that it may belong in `~/.claude/CLAUDE.md` (loads whole; a memory only loads when recalled) |

The bar for proposing: every shared memory adds an index line to every session
of every member, and a memory read in a project where it doesn't fit misleads.
Propose when you would expect it to be used in most members, not merely to be
true there. A preference the user stated while working on one project (how much
freedom to take, how to explain) is about that project unless they said
otherwise. `user` and `feedback` memories are usual candidates, `reference`
sometimes, `project` rarely. Suggest the narrowest group that fits. When
unsure, don't propose.

Run `share`, `move`, `unshare` or `line` only when the user asks, usually while
going through `nota.md`. After a rewrite they approved: write the text to the
memory file and its usual MEMORY.md line, then `share` (it keeps that line). If
the general version loses something this project needs, split: share the
general part and keep a short local memory with the rest, linking
`[[the-shared-name]]`.

## Review notes

The user reviews memories in their own language in notes beside `groups.json`
(`~/.claude/shared-memories/`), which `status` and the hooks check:

- `nota.md`: one `#` section per group, one `##` entry per shared memory, then
  `# Candidatas` with the proposals.
- `nota-<project folder without the leading dash>.md` (`nota-ferrum.md`): the
  project's local memories. It exists only for projects the user asked to
  review; create one when they ask.

Each entry is a `##` heading ending in the file in backticks, which is how the
script matches it: `` `<group>/<file>.md` `` for shared, `` `<project folder>/<file>.md` ``
for a candidate, `` `<file>.md` `` in a project note. Under it: where it came
from (project and date), a faithful translation of the whole memory (the file
keeps its language), and your opinion in one or two lines (keep, move, delete,
and why). A candidate also names the suggested group, and the rewritten text
with its translation if you propose one.

When a hook says a note must be added to or updated, do it in the same turn.
When the user decides on an entry, apply it and update the note. When `status`
lists notes out of date, fix them.

## Showing memories to the user

Memories are written for the model. When you show one to the user (a rewrite,
a conflict, a review they asked for) and it is in another language than the
one they write in, show a faithful translation next to it, unless they said
they don't want one. The file keeps its language.

## Commands

| Task | Arguments |
|---|---|
| Groups, members, shared memories, pending fixes, review notes out of date, hook check | `status` |
| Share (moves the files, links them in all members) | `share <group> <memory path>...` |
| Unshare: delete, or keep a plain copy in one project | `unshare <group>/<file>.md... [--keep <project folder>]` |
| Move to another group | `move <new group> <group>/<file>.md...` |
| Show or change a shared memory's MEMORY.md line | `line <group>/<file>.md [--title <text>] [--summary <text>]` |
| Show a group; create it or change its members | `group <name> [--add <entry>...] [--remove <entry>...]` |
| Delete an empty group | `group <name> --delete` |
| Repair links and blocks (after a manual change) | `sync [--project <project folder>]` |
| Add the hooks to `~/.claude/settings.json` (backup kept) and create `groups.json` | `install [--dry-run]` |

A memory path is absolute, in `~/.claude/projects/<project folder>/memory/`.
An entry is a project folder name (`-dev-sandbox`) or a project path
(`/home/me/Dev/*`); `*` matches anything, so `*` alone is every project.
Membership is by folder: a project opened at another path (a moved repo, a
container with another mount) is another member. Group changes re-link
everything at once.

## Conflicts

`status` and the hooks report a member that has a plain file with the same name
as a shared memory but different content. Show the user both, merge into the
shared copy (or rename the local one), delete the local file, run `sync`.

## Setup

When the user asks to install: confirm the skill sits in `~/.claude/skills/`,
run `install --dry-run`, show what will be added, then `install`. Then help
them create the first group with `group`. The hooks apply to sessions started
afterwards.
