---
name: mirrors
description: Keeps read-only local copies of outside sources in mirrors/ at the repo root - git repositories (pinned or following a branch), documentation sites with llms.txt, and web articles captured as markdown with the articles they link to. Use when the user wants to mirror, capture, update or check an outside source, or when a task needs many files or pages of one and reading them locally beats fetching pages.
argument-hint: "[add <name> <url> [--web] | check | pin <target>... [@version] | follow <target>... | links <name> | remove <target>]"
allowed-tools: Bash(python3 *fetch_mirrors.py*)
---

# Mirrors

Run `python3 "${CLAUDE_SKILL_DIR}/fetch_mirrors.py" [args]` from anywhere inside the repository. The manifest `mirrors/mirrors.json` is versioned; the copies in `mirrors/<name>/` are gitignored, have no `.git`, are read-only and record their commit in `.mirror-commit`. The script creates the manifest and the `.gitignore` lines when missing.

```
(no args)                                        fetch everything
--check [target...]                              missing, stale, behind its branch, pinned before its release
--list
--add <name> <url> [--ref R] [--include PATH...] [--license SPDX...] [--follow]
--add <name> <site>/llms.txt [--include en]      docs site as pages, always current
--add <name> <url> --web [--depth N] [--max-pages N]   web articles as markdown (snapshot)
--pin <target>... [ref | commit | @version | @package]
--follow <target>...
--remove <target>
--links <name>                                   links in captured articles not captured yet
--refresh [target...]                            fetch web articles again; pages now
--max-age H [target...]                          skip pages checked less than H hours ago
--stale <name> [folder]                          files citing pages changed since their last commit
```

A target is a mirror name, or `<set>/<member>` when the url has `{member}` (one repository per package). `--pin` or `--follow` on a member not listed yet adds it; on the set name, they apply to all members. With `--pin`, the last argument is the ref when it is not a target; a version with no tag fails.

## Choosing
- Pinned for code or specs that documents cite; following for docs you want current.
- Prefer a site's git repository over its pages; `--add` prints a hint when the pages link to GitHub. For lookups, fetch pages with `--max-age 24`.
- Web articles need Defuddle; the script prints the install command. Start with depth 0, show the user `--links <name>` and let them pick, or use `--depth 1` with a small `--max-pages`: sites cross-link a lot.
- Check the license before adding and record it with `--license`; with no license file, tell the user.
- `--include` keeps big repositories small (sparse checkout, plus `LICENSE*`). For Rust workspaces with mixed licenses, `"license_check": "cargo"` in the entry refuses included crates whose license is not listed.

## After
- After `--add`, `--pin`, `--follow` or `--remove`, tell the user to commit `mirrors/mirrors.json` (and `.gitignore` if it changed); a new pin goes in the same commit as the documents that cite it.
- Report the script's output in a few lines; don't paste fetched content.
