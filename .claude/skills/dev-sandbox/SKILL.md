---
name: dev-sandbox
description: Working map of the dev-sandbox repo (Docker sandbox for AI coding agents) - how dev-docker, the Dockerfile and the mounts fit, the non-obvious decisions behind them, and where each topic lives. Use before answering how dev-sandbox works, judging a change to it, or answering Claude Code questions in this repo.
---

# dev-sandbox: working map

Facts that cost reading time to rebuild. Details live in the files linked; read
them before quoting specifics. Current version and test status: top section of
`CHANGELOG.md`.

## Purpose
Run Claude Code, Codex and agy (Antigravity CLI) in Docker, isolated from the
host, with project files owned by the host user. Audience: Brazilian devs,
including beginners. The image is complete on purpose (6-8 GB): a missing tool
costs more (silent workarounds, tokens, errors) than disk
(`docs/guias/filosofia-da-imagem.md`).

## How it works
- `dev-docker` (bash, runs on the HOST, symlinked from `~/.local/bin`):
  1. Parses `--nome NOME`, `--atalho NOME [path]` (writes `~/.local/bin/dev-docker-NOME`), `--atalhos`.
  2. Mount path = host path. `/workspace` for system dirs and for `/` or `$HOME` (asks `sim` first). `/NOME` with `--nome`.
  3. Unless `DEV_GIT_RW=1`: `.git/hooks` and `.git/config` bind-mounted read-only for repos up to 2 levels below the mount, plus their submodules (`.git/modules/*`).
  4. `DEV_PORTS="5173 8090:8080"` → `-p 127.0.0.1:host:container`. None by default.
  5. `sudo docker run -it --rm --cap-drop ALL --security-opt no-new-privileges --user UID:GID`.
  6. On exit: lists host-run files changed during the session (ctime vs a marker), keeps the container's exit code.
- Mounts, outer before inner (order matters): project → `~/.cache/dev-sandbox/home` as `$HOME=/tmp/dev-home` → real host `~/.gemini`, `~/.claude`, `~/.codex` over it → `~/.cache/dev-sandbox/cargo` as `/usr/local/cargo/registry`.
- Env set by the script: `HOME`, `DEV_SANDBOX=1`, `DEV_SANDBOX_NAME`, `DEV_SANDBOX_PORTS`, `CLAUDE_CODE_TMPDIR=/tmp/dev-home/.cache/claude-tmp`.
- `Dockerfile`: debian bookworm-slim; apt tools; uv; Node 22 + pnpm/yarn/typescript/tsx; Rust stable (`/usr/local/cargo` world-writable); Chromium + Tauri v2 libs; optional `WITH_GO`/`WITH_JAVA`; agents in the last layer (`AGENTS_REFRESH` rebuilds only it); `DISABLE_AUTOUPDATER=1`; `chmod 755 /root` + `a+rX /root/.local` (agents installed as root, run as the host UID); `HOME=/tmp/dev-home` (1777).
- Agent instructions: `sandbox/AGENTS.md` → `/etc/claude-code/CLAUDE.md` (Claude loads it by itself, proven) and `/etc/dev-sandbox/AGENTS.md` (Codex/agy need one conditional line in their host global file, see README). `sandbox/AGENTS-completo.md` is a reference copy, not in the image. `sandbox/managed-settings.json` → `/etc/claude-code/` (deny Read/Edit on agent credentials).

## Decisions that look wrong but are not
| Decision | Reason | Where |
|---|---|---|
| `--user UID:GID` | Core fix: bind mounts keep UIDs, root-owned files break host tools | `DOCUMENTACAO.md#o-problema-de-fundo-bind-mount-e-uid` |
| No `docker` group, `sudo` every time | The group is passwordless root | `DOCUMENTACAO.md#por-que-nao-usar-o-grupo-docker` |
| Project at its host path | Claude keys memory/`--resume` by path; v0.1 `/workspace` mixed all projects | `docs/aprendizados/2026-10-memoria-misturada-entre-projetos.md` |
| Whole `$HOME` persisted | New tools persist without listing them; cost: poisoned cache survives | `DOCUMENTACAO.md#por-que-a-home-inteira-e-montada` |
| `~/.claude.json` not shared with host | Single-file bind mounts break on atomic rewrite | `docs/claude-code/sessoes-e-persistencia.md` |
| Auto-update off | Updates went to `$HOME` and were never used | `docs/aprendizados/2026-10-claude-autoupdate-orfao.md` |
| No ports by default, `127.0.0.1` only | Conflicts (Syncthing) and one container at a time | `docs/aprendizados/2026-10-portas-fixas.md` |
| Separate cargo registry; `cargo install` binaries are lost | Toolchain mismatch with host cache; only `registry` is mounted | `DOCUMENTACAO.md#por-que-o-cache-do-cargo-fica-separado` |
| Playwright needs `executablePath` | It reads no env var for the browser | `docs/aprendizados/2026-10-playwright-ignora-chromium-da-imagem.md` |
| Security by mechanism, not prose | Instructions are not locks; mounts, deny rules and the exit report are | `docs/guias/seguranca.md`, `docs/claude-code/instrucao-ou-mecanismo.md` |
| Container-only facts (e.g. host path translation) go in `sandbox/AGENTS.md`, not `~/.claude/rules` | Host `~/.claude` is mounted in, so its rules also load in host sessions, where they are wrong | `docs/claude-code/instrucao-ou-mecanismo.md` |
| Scratchpad not mounted at its host path | Only fixes displayed temp paths; plans live in `~/.claude/plans`, so the path line is still needed | this table |

## Known open gaps
Credentials readable by a script that opens files itself (deny covers `cat`/`head`/`sed`, not `python`); outbound internet; repos deeper than 2
levels or created in-session get only the exit warning; nested sandboxes
(`/sandbox`, agy nsjail) untested inside Docker. Full list: `docs/guias/seguranca.md`.

## Where each topic lives
| Topic | File |
|---|---|
| Install, daily use, quick table | `README.md` |
| Why each script/Dockerfile line exists, troubleshooting | `DOCUMENTACAO.md` |
| Bridges still open, host-run files | `docs/guias/seguranca.md` |
| Ports, Tauri, parallel sessions, worktrees | `docs/guias/portas-e-sessoes-paralelas.md` |
| Updating agents, image, host | `docs/guias/atualizacao.md` |
| Branch workflow (`claude` by default, when to split) | `docs/guias/branches.md` |
| Image size, disk, Timeshift | `docs/guias/filosofia-da-imagem.md` |
| Backup of `~/.claude` without leaking secrets | `docs/guias/backup-e-git.md` |
| Claude Code behavior (memory, sessions, context, cache, subagents, model) | `docs/claude-code/README.md` (index) |
| Real problems and their causes | `docs/aprendizados/README.md` (index) |
| Personal skill that sets up this repo's `.claude/` pattern in other projects | `extras/skills/montar-consultor/` (its `example` links to `.claude/`) |
| Missing tools reported by agents | host `~/.cache/dev-sandbox/home/.dev-sandbox/feedback.md` |

## Claude Code questions
1. Find the guide in `docs/claude-code/README.md` and read it. Those guides were verified against the official docs (stamp at the bottom of each).
2. Not covered, or possibly outdated: delegate to the `claude-code-pesquisador` agent instead of fetching docs here (official pages exceed 100k characters).
3. Sandbox-specific: the built-in Explore and Plan agents get no CLAUDE.md, so they don't know the container rules; `/etc/claude-code/CLAUDE.md` can't be excluded per project; instruction edits apply only to the next session (and to the image only after a rebuild).
