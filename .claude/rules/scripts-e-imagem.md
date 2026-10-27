---
paths:
  - "dev-docker"
  - "Dockerfile"
  - "sandbox/**"
  - "extras/**"
---

# Changing the script, the image or the agent instructions

## Validate
- No `docker` here. Run `bash -n dev-docker`, then a dry run: a fake `sudo` script first in `PATH` that prints the `docker run` args and simulates the agent (touch files, exit with a code). Use a throwaway repo in the scratchpad, never this one.
- With `set -euo pipefail`, a failing pipeline inside `$(...)` exits the script: end it with `|| true` when failure is acceptable.
- Say what still needs a real test on the host.

## Propagate (one change, every place that describes it)
| Changed | Also update |
|---|---|
| Mount, env var, flag or protection in `dev-docker` | `DOCUMENTACAO.md` (its section, the security summary table, troubleshooting), `docs/guias/seguranca.md` if it opens or closes a bridge, `README.md` table if user-facing, `CHANGELOG.md` |
| Package, ENV or layer in `Dockerfile` | `README.md` image table, `sandbox/AGENTS*.md` if agents should act differently, `CHANGELOG.md` with the rebuild needed |
| `sandbox/AGENTS.md` | Same change in `sandbox/AGENTS-completo.md` when it applies; takes effect only after a rebuild |
| How the pieces fit, or a decision and its reason | `.claude/skills/dev-sandbox/SKILL.md` |
| Non-obvious discovery | `docs/aprendizados/` + its index |

## `sandbox/AGENTS.md` principles
Every line costs context in every session of every project. Keep a line only if
it changes what the agent does and the agent could not deduce it from the
environment. Mechanisms (mounts, `managed-settings.json`, the exit report)
beat prose for anything that must hold.

## Final message
`dev-docker`, `Dockerfile`, `extras/` hooks and `.github/` run on the host or in CI: list the ones you changed.
