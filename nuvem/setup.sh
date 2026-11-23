#!/bin/bash
# dev-sandbox na nuvem do Claude Code (claude.ai/code): setup script do ambiente.
# Como usar: docs/guias/nuvem.md
#
# Roda como root antes da sessão abrir; o resultado fica no cache do ambiente
# (~7 dias). Precisa sair com 0 e em menos de ~5 min, por isso cada passo
# termina em "|| true". Aqui leva cerca de 1 minuto.
#
# Instala só o que o Dockerfile tem e a imagem da nuvem não (conferido em
# 11/2026). Já vêm na imagem: Python + uv, Node 22 + pnpm/yarn, Rust +
# clippy/rustfmt, Go, Java, GCC/Clang/cmake, Docker, PostgreSQL, Redis, git,
# gh, jq, rg, tmux, Playwright e Chrome (/usr/bin/google-chrome).

export DEBIAN_FRONTEND=noninteractive
exec > >(tee -a /var/log/dev-sandbox-nuvem.log) 2>&1
echo "== dev-sandbox nuvem: $(date -u +%FT%TZ) =="

# ── Pacotes do Dockerfile que faltam na imagem da nuvem ─────────
apt-get update -qq || true
apt-get install -y -qq --no-install-recommends \
  openssh-client libpq-dev tree fd-find rsync iproute2 dnsutils sqlite3 \
  libwebkit2gtk-4.1-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev patchelf \
  || echo "AVISO: parte dos pacotes apt falhou"
[ -e /usr/local/bin/fd ] || ln -s /usr/bin/fdfind /usr/local/bin/fd || true

# ── TypeScript e tsx globais (a imagem só traz o ts-node) ───────
npm install -g --silent typescript tsx || echo "AVISO: typescript/tsx falhou"

# ── /usr/bin/chromium: o mesmo caminho da imagem Docker ─────────
# Aponta para o google-chrome da nuvem, um script que acrescenta
# --no-sandbox quando roda como root. Um link direto para o binário do
# Chrome faz o Puppeteer falhar como root. Não baixe navegadores aqui:
# o Playwright da imagem já tem o dele.
if [ -x /usr/bin/google-chrome ]; then ln -sf /usr/bin/google-chrome /usr/bin/chromium || true; fi

# ── Instruções do ambiente para o Claude ────────────────────────
# Fazem o papel do /etc/claude-code/CLAUDE.md da imagem Docker: valem em
# toda sessão deste ambiente, em qualquer repositório.
mkdir -p /root/.claude
cat > /root/.claude/CLAUDE.md <<'EOF'
# Environment: Claude Code cloud VM (dev-sandbox setup)

* You are in an Anthropic-hosted cloud VM (Ubuntu 24.04) as root, with the repository freshly cloned. Nothing outside the repository survives the session: deliver work as commits pushed to the session's branch.
* `apt-get` works, but what you install mid-session is lost when the session ends.
* **Missing system tool:** if one forced a workaround or would have made the task clearly easier, safer, or cheaper:
  1. Install it for this session if that is quick; otherwise do a cheap workaround, or stop and ask.
  2. Say so in your final message: `Missing in sandbox: <tool> — <what it would have saved>`, so the user can add it to the environment's setup script.
  Skip one-off curiosities.

# Network, browser, services
* Outbound access is limited to the environment's allowlist. If the proxy blocks a host, do not route around it; name the host in your final message.
* Headless Chrome is preinstalled and Playwright and Puppeteer use it with no options. Only if a project pins its own Playwright version: set `executablePath: '/usr/bin/chromium'` instead of running `playwright install`.
* No display: GUI apps (e.g. a Tauri window) cannot open. Validate with builds, `cargo check`/`cargo test`, and headless tests.
* Docker, PostgreSQL and Redis are installed but stopped: `service docker start`, `service postgresql start`, `service redis-server start`.
EOF

echo "== dev-sandbox nuvem: fim =="
exit 0
