---
name: mirrors
description: Keeps read-only local copies of outside git repositories (docs, reference code, example configs) in mirrors/ at the repo root, pinned to a commit or following a branch. Use when the user wants to mirror, update or check an outside repository, or when a task needs many files of an outside repository and reading them locally beats fetching pages.
argument-hint: "[add <name> <url> | check | pin <target>... [@version] | follow <target>... | remove <target>]"
allowed-tools: Bash(python3 *fetch_mirrors.py*)
---

# Mirrors

`python3 "${CLAUDE_SKILL_DIR}/fetch_mirrors.py"` does the work; run it from
anywhere inside the repository. It creates `mirrors/mirrors.json` and the two
`.gitignore` lines (`/mirrors/*`, `!/mirrors/mirrors.json`) when missing, also
before `git init` (then other `.gitignore` rules are not checked). The
manifest is versioned; the copies are not. Each copy has no `.git` (no hooks
can run from it), is read-only on disk, and records its commit in
`.mirror-commit`. Links pointing outside a copy are dropped.

| Task | Arguments |
|---|---|
| Fetch everything (fresh clone, or after a manifest change) | *(none)* |
| What is missing, stale or behind its branch; pinned copies past their release | `--check` |
| List mirrors | `--list` |
| Add, pinned to the newest commit of the default branch | `--add <name> <url> [--ref <branch or tag>] [--include <path> ...] [--license <SPDX> ...]` |
| Add, always taking the newest commit | the same plus `--follow` |
| Pin to the newest commit of its ref, a ref, or a commit | `--pin <target>... [<ref or 40-char commit>]` |
| Pin to the tag of a published version (`1.2.3` or `v1.2.3`) | `--pin <target>... @<version>` |
| Pin to the version in package.json on the default branch | `--pin <target>... @package` |
| Switch to following | `--follow <target>...` |
| Delete the copy and the entry | `--remove <target>` |

A target is a mirror name, or `<set>/<member>` for a set: a url with
`{member}` (one repository per package, e.g. `https://host/org/{member}`).
`--pin` or `--follow` on a member the set does not list yet adds it; on the
set name, they apply to all its members. With `--pin`, the last argument is
the ref when it is not a target. A version with no tag fails.

## Pinned or following
- **Pinned** (`commit` in the manifest): code or specs that documents cite. Commit the manifest together with the documents that cite the new version, so the project's commit fixes the sources it cites.
- **Following** (`"follow": true`): documentation you want current, such as a language's docs or a tool's own repo. Each plain run fetches the newest commit; nothing in the manifest changes.

## Rules
- Check the license of a new source before adding it and record it with `--license`. With no license file, say so to the user.
- `--include` keeps big repositories small (sparse checkout, plus the repository's `LICENSE*` files). For Rust workspaces with mixed licenses, add `"license_check": "cargo"` to the entry: the fetch refuses any included crate whose `Cargo.toml` license is not listed.
- Never edit files under `mirrors/`; they are read-only and replaced on the next fetch. To use a file, copy it out.
- Cite files as `mirrors/<name>/<path>` (or `mirrors/<set>/<member>/<path>`).
- After `--add`, `--pin`, `--follow` or `--remove`, tell the user to commit `mirrors/mirrors.json` (and `.gitignore` if it changed).
- Report the script's output in a few lines; don't paste fetched content.
