* You are inside the dev-sandbox Docker container (`DEV_SANDBOX=1`), as a non-root user without `sudo`.
* `$CLAUDE_CODE_TMPDIR` behaves as on the host.
* Your cwd, `~/.claude` and all `$HOME` persists on the host.
* Lost on exit: system directories and `/tmp` outside `$HOME`. Keep nothing there that must survive.
* `apt-get` fails. Do not work around this with large hacks.
* **Missing system tool:** if one forced a workaround or would have made the task clearly easier, safer, or cheaper:
  1. Do a cheap workaround if one exists; otherwise stop and ask.
  2. Say so in your final message: `Missing in sandbox: <tool> — <what it would have saved>`.
  3. Append one line to `~/.dev-sandbox/feedback.md`: `- YYYY-MM-DD | <tool> | <project> | <why>`.
  Skip one-off curiosities.
* Project dependencies: as on the host.

# Network and ports
* Outbound internet works.
* Browser tests work inside the container: headless Chromium is at `/usr/bin/chromium`, and Puppeteer and Playwright already point to it.
* No display: GUI apps (e.g. a Tauri window) cannot open. Validate with `cargo check`/`cargo test`, builds, and headless tests.
* Only when the user needs to open something in **their** browser: published ports are in `$DEV_SANDBOX_PORTS`, as `5173` or `host:container`. Bind to `0.0.0.0` (e.g. `vite --host`) on the container port and give the user the host port. If empty, no port is published: the user must restart with `DEV_PORTS="<port>" dev-docker`.

# Git
- `.git/hooks` and `.git/config` are **read-only** on purpose (they run on the host). Commits work; local `git config`, `git remote add` and `push -u` do not. If needed, ask the user to do it on the host or restart with `DEV_GIT_RW=1`.
- Missing identity: `git config --global`, never in the repo.
- No SSH keys: the user pushes from the host. Don't ask for keys or tokens.

# Security boundaries
- Never read, print, copy, or modify agent credentials (`~/.claude/.credentials.json`, `~/.codex/auth.json`, tokens under `~/.gemini`).
- These files **run on the host**, outside the isolation, with the user's privileges: `.vscode/` (tasks, settings), `.envrc`, `.git/hooks` and `.git/config` (read-only protection misses submodules and repos created during the session), hook folders (`.husky/`, `.lefthook*`), `Makefile`, `package.json` scripts, `build.rs`, Tauri config. When you create or change any of them, list them explicitly in your final message so the user can review before running anything on the host.
