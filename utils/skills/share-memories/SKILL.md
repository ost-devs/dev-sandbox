---
name: share-memories
description: Shares Claude Code auto-memories between projects - all of them, a list, or a category such as dev - and keeps them in sync (one copy, linked into each project). Use when a hook reports a new memory in a project that belongs to a shared-memory group, when the user wants to share, unshare, move, group, review or check memories across projects, or to install it.
argument-hint: "[status | share <group> <memory>... | unshare <group>/<file>... | move <group> <group>/<file>... | group <name> | install]"
allowed-tools: Bash(python3 *share_memories.py*)
---

# Share memories

Memory creation is not yours to change here: write memories exactly as usual.
This skill only decides, afterwards, whether a memory also belongs to other
projects. `python3 "${CLAUDE_SKILL_DIR}/share_memories.py"` does the moving;
you do the judging.

How it works: a shared memory has one copy in `~/.claude/shared-memories/<group>/`.
Each member project's `memory/` has a relative symlink to it, and its `MEMORY.md`
lists it in a generated block (`share-memories:start` … `end`). Never edit that
block; edit the memory. Write and Edit refuse to write through the symlink and
name the target: write to the target, and the change reaches every project.
Hooks re-link and refresh the blocks; new projects of a group get the links at
their first session.

## Deciding about a new memory

A hook says "New memory `x.md`" when the project is in a group. Finish the
current step first, then read the memory and the groups (`status`) and pick one:

| The memory | Do |
|---|---|
| Needs this project to make sense: its files, paths, decisions, deadlines, people, versions | Nothing. It stays local. Say nothing |
| Holds as written for most projects of a group | `share <group> <path>`, then tell the user in one line, including how to undo |
| Has a general lesson inside project-specific wording | Propose a rewrite (below) |
| Is a short rule that must apply in every session of every project | Suggest moving it to `~/.claude/CLAUDE.md` instead: it loads whole, a memory only loads when recalled |

The bar: every shared memory adds an index line to every session of every
member, and a memory read in a project where it doesn't fit misleads. Share
when you would expect it to be used in most members, not merely to be true
there. `user` and `feedback` memories are usual candidates, `reference`
sometimes, `project` rarely. Pick the narrowest group that fits. When unsure,
keep it local: sharing later is one command, an unneeded line costs every day.

## Rewriting for the group (only with the user's permission)

1. Show the user the current text, the proposed one, and the group.
2. Keep what makes it actionable: the rule, the **Why**, the **How to apply**,
   and one concrete example even if it comes from this project. Remove only
   what is meaningless elsewhere (local paths, file names, ticket numbers).
3. If the general version loses something this project needs, split: share the
   general part and keep a short local memory with the specific remainder,
   linking `[[the-shared-name]]`. If nothing useful survives generalizing,
   keep it local.
4. Write the approved text to the memory file, then run `share`.

Without an answer, leave the memory local and unchanged.

## Showing memories to the user

Memories are written for the model. When you show one to the user (a rewrite,
a conflict, a review they asked for) and it is in another language than the
one they write in, show a faithful translation next to it, unless they said
they don't want one. The file keeps its language.

## Commands

| Task | Arguments |
|---|---|
| Groups, members, shared memories, pending fixes, hook check | `status` |
| Share (moves the files, links them in all members) | `share <group> <memory path>...` |
| Unshare: delete, or keep a plain copy in one project | `unshare <group>/<file>.md... [--keep <project folder>]` |
| Move to another group | `move <new group> <group>/<file>.md...` |
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
