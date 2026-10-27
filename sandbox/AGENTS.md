* You are inside the dev-sandbox Docker container (`DEV_SANDBOX=1`), as a non-root user without `sudo`.
* Your cwd and all of `$HOME` persist on the host, including `~/.claude` and `$CLAUDE_CODE_TMPDIR` (which behaves as on the host).
* Lost on exit: system directories and `/tmp` outside `$HOME`. Keep nothing there that must survive.
* Only when giving the user a path to open on the host: `/tmp/dev-home/.claude/…` is `~/.claude/…` there; the rest of `/tmp/dev-home/…` is `~/.cache/dev-sandbox/home/…`.
* Project dependencies install as on the host. System packages do not (`apt-get` fails); do not work around this with large hacks.
* **Missing system tool:** if one forced a workaround or would have made the task clearly easier, safer, or cheaper:
  1. Do a cheap workaround if one exists; otherwise stop and ask.
  2. Say so in your final message: `Missing in sandbox: <tool> — <what it would have saved>`.
  3. Append one line to `~/.dev-sandbox/feedback.md`: `- YYYY-MM-DD | <tool> | <project> | <why>`.
  Skip one-off curiosities.

# Network and browser
* Outbound internet works.
* Browser tests work inside the container with headless Chromium at `/usr/bin/chromium`. Puppeteer already uses it; for Playwright, set `executablePath: '/usr/bin/chromium'` in the launch options instead of downloading browsers.
* No display: GUI apps (e.g. a Tauri window) cannot open. Validate with `cargo check`/`cargo test`, builds, and headless tests.
