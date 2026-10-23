# dev-sandbox — instructions for agents working on this repo

Docker environment for running AI coding agents isolated from the host.
Audience: Brazilian developers, including beginners ("vibe coders").

## Language
- Docs for humans (`README.md`, `DOCUMENTACAO.md`, `docs/`): Brazilian Portuguese, plain and direct.
- Instructions for AI (`AGENTS.md`, `sandbox/AGENTS.md`, rules): English, short.

## Sources of truth
- `Dockerfile` and `dev-docker` are the real configuration. Docs link to them and quote short excerpts; never paste whole copies that will drift.
- `sandbox/AGENTS.md` is baked into the image and loaded by agents in every project: keep it short, every line costs context in all sessions.

## Workflow
- Never commit on `main`; work on a branch.
- Commit after each logical change, without asking first, so the maintainer or another agent can review, revert, or continue. Never push.
- You usually run *inside* the sandbox: you cannot run `docker` here. Validate scripts with `bash -n` and dry runs (fake `sudo`), and state clearly what still needs a real test on the host.

## Learnings
- Non-obvious discoveries (a bug, a trade-off, something that cost hours) go to `docs/aprendizados/` following its README.
- Missing tools reported by agents (`~/.dev-sandbox/feedback.md`) are triaged there before going into the `Dockerfile`.
