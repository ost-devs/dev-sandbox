# Verified Claude Code facts

- Skill listing truncates `description` + `when_to_use` at 1,536 characters; body loads only when invoked; supporting files load on demand (keep SKILL.md under 500 lines). skills page, 2026-10-27, 2.1.310.
- Skill frontmatter: `disable-model-invocation: true` = only the user invokes it (and it can't be preloaded by agents); `user-invocable: false` = only Claude; `paths` limits auto-loading; `context: fork` + `agent` runs it as a subagent. skills page, 2026-10-27, 2.1.310.
- Subagent `memory`: `user` → `~/.claude/agent-memory/<agent>/`, `project` → `.claude/agent-memory/<agent>/` (meant for git), `local` → `.claude/agent-memory-local/<agent>/`. First 200 lines or 25 KB of its MEMORY.md go into the agent's system prompt; Read/Write/Edit auto-enabled; no effect if auto memory is off. sub-agents page, 2026-10-27, 2.1.310.
- Subagent `skills` preloads full skill text (up to 32), controls preloading not access. Combined custom-agent descriptions over 15,000 tokens trigger a startup warning. sub-agents page, 2026-10-27, 2.1.310.
- Playwright 1.64.1 reads no env var for the browser path (`PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH` is not in playwright-core); use `executablePath`. Source grep + test in container, 2026-10-26.
