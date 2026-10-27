FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Filosofia: imagem "completa" de propósito (~6–8 GB). Para um ambiente de
# agentes de IA, faltar ferramenta custa mais (o agente improvisa em
# silêncio, gasta tokens, erra) do que alguns GB de disco. Ver
# docs/guias/filosofia-da-imagem.md antes de enxugar.

# ── Base do sistema + utilitários que agentes usam sem avisar ────
RUN apt-get update && apt-get install -y \
    curl wget git git-lfs ca-certificates gnupg openssh-client \
    build-essential pkg-config cmake clang \
    libssl-dev libsqlite3-dev libpq-dev zlib1g-dev \
    jq unzip zip xz-utils tree ripgrep fd-find rsync file less patch bc \
    procps lsof iproute2 dnsutils netcat-openbsd \
    sqlite3 tmux nano \
    python3 python3-pip python3-venv python-is-python3 \
    && ln -sf /usr/bin/fdfind /usr/local/bin/fd \
    && rm -rf /var/lib/apt/lists/*

# ── uv (Python moderno: venvs e pacotes em segundos) ─────────────
RUN curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=/usr/local/bin UV_NO_MODIFY_PATH=1 sh

# ── Node.js 22 LTS + TypeScript ──────────────────────────────────
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g pnpm yarn typescript tsx \
    && rm -rf /var/lib/apt/lists/*

# ── Rust stable ───────────────────────────────────────────────────
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal \
    && rustup component add clippy rustfmt \
    && chmod -R a+w /usr/local/cargo /usr/local/rustup

# ── Navegador headless (Chromium) + bibliotecas do Tauri v2 ──────
RUN apt-get update && apt-get install -y \
    chromium fonts-liberation libnss3 libatk-bridge2.0-0 libdrm2 \
    libxkbcommon0 libgbm1 libasound2 \
    libwebkit2gtk-4.1-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev patchelf \
    && rm -rf /var/lib/apt/lists/*

# O Playwright não lê variável de ambiente para o navegador: cada projeto
# passa executablePath (ver docs/aprendizados/2026-10-playwright-ignora-chromium-da-imagem.md).
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# ── Linguagens extras (desligadas por padrão) ────────────────────
# Ligue no build: sudo docker build --build-arg WITH_GO=1 --build-arg WITH_JAVA=1 -t dev-sandbox .
ARG WITH_GO=0
ARG WITH_JAVA=0
RUN if [ "$WITH_GO" = "1" ]; then \
      GO_VERSION="$(curl -fsSL 'https://go.dev/VERSION?m=text' | head -1)" \
      && curl -fsSL "https://go.dev/dl/${GO_VERSION}.linux-$(dpkg --print-architecture).tar.gz" | tar -C /usr/local -xz; \
    fi \
    && if [ "$WITH_JAVA" = "1" ]; then \
      apt-get update && apt-get install -y default-jdk-headless maven && rm -rf /var/lib/apt/lists/*; \
    fi
ENV PATH="${PATH}:/usr/local/go/bin"

# ── Agentes de IA ────────────────────────────────────────────────
# Ficam por último: são o que mais muda. Para atualizar só eles, sem
# refazer o resto: sudo docker build --build-arg AGENTS_REFRESH=$(date +%s) -t dev-sandbox .
ARG AGENTS_REFRESH=0
RUN echo "agents refresh: $AGENTS_REFRESH" \
    && curl -fsSL https://antigravity.google/cli/install.sh | bash \
    && curl -fsSL https://claude.ai/install.sh | bash \
    && npm install -g @openai/codex

# O auto-update do Claude Code baixa versões novas em $HOME (persistente),
# mas o PATH usa a da imagem: baixava e nunca usava. A imagem é a fonte da
# verdade; atualize com AGENTS_REFRESH acima.
ENV DISABLE_AUTOUPDATER=1

# Instruções do ambiente para os agentes. /etc/claude-code/CLAUDE.md é o
# local "managed" do Claude Code no Linux: carrega sozinho, só no container.
COPY sandbox/AGENTS.md /etc/dev-sandbox/AGENTS.md
COPY sandbox/AGENTS.md /etc/claude-code/CLAUDE.md
# Bloqueia as ferramentas de leitura/edição do Claude nas credenciais dos
# agentes, inclusive via `cat`/`head`/`sed`. Não custa tokens; não cobre um
# script (Python, Node) que abra o arquivo sozinho.
COPY sandbox/managed-settings.json /etc/claude-code/managed-settings.json

# ── Permissões para rodar como usuário não-root ──────────────────
# Necessário mesmo que você só use um agente — ver DOCUMENTACAO.md.
RUN chmod 755 /root \
    && chmod -R a+rX /root/.local

ENV PATH="/root/.local/bin:${PATH}"

RUN mkdir -p /tmp/dev-home && chmod 1777 /tmp/dev-home
ENV HOME=/tmp/dev-home

WORKDIR /workspace
