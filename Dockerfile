FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# ── Base do sistema + Python + Utilitários para Agentes ──────────
RUN apt-get update && apt-get install -y \
    curl wget git ca-certificates build-essential pkg-config \
    libssl-dev libsqlite3-dev zlib1g-dev cmake \
    jq unzip zip tree ripgrep fd-find \
    python3 python3-pip python3-venv python-is-python3 \
    && rm -rf /var/lib/apt/lists/*

# ── Node.js 22 LTS + TypeScript ──────────────────────────────────
# Remova este bloco inteiro se não for usar Node/TS.
RUN curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g pnpm yarn typescript tsx \
    && rm -rf /var/lib/apt/lists/*

# ── Rust stable ───────────────────────────────────────────────────
# Remova este bloco (e CARGO_CACHE_PATH no script) se não for usar Rust.
ENV RUSTUP_HOME=/usr/local/rustup \
    CARGO_HOME=/usr/local/cargo \
    PATH=/usr/local/cargo/bin:$PATH
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y --default-toolchain stable --profile minimal \
    && chmod -R a+w /usr/local/cargo /usr/local/rustup

# ── Antigravity CLI (agy, da Google) ─────────────────────────────
# Remova este bloco (e o mount de .gemini no script) se não usar o agy.
RUN curl -fsSL https://antigravity.google/cli/install.sh | bash

# ── Claude Code (Anthropic) — opcional, comentado por padrão ────
# Instalador nativo: não depende do bloco Node.js acima. Para ativar:
# descomente a linha abaixo, reconstrua a imagem (Parte 1), e descomente
# as linhas de CLAUDE_PATH no script.
RUN curl -fsSL https://claude.ai/install.sh | bash

# ── Codex CLI (OpenAI) — opcional, comentado por padrão ──────────
# Exige o bloco Node.js acima. Para ativar: descomente a linha abaixo,
# reconstrua a imagem, e descomente as linhas de CODEX_PATH no script.
RUN npm install -g @openai/codex

# ── Parte 2: Navegador Invisível (Chromium) + Atalho fd + Suporte a Tauri v2 ─
RUN apt-get update && apt-get install -y \
    chromium fonts-liberation libnss3 libatk-bridge2.0-0 libdrm2 \
    libxkbcommon0 libgbm1 libasound2 \
    libwebkit2gtk-4.1-dev libgtk-3-dev libayatana-appindicator3-dev librsvg2-dev patchelf \
    && ln -sf /usr/bin/fdfind /usr/local/bin/fd \
    && rm -rf /var/lib/apt/lists/*

ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium \
    PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=/usr/bin/chromium

# ── Permissões para rodar como usuário não-root ──────────────────
# Necessário mesmo que você só use um agente — ver DOCUMENTACAO.md.
RUN chmod 755 /root \
    && chmod -R a+rX /root/.local

ENV PATH="/root/.local/bin:${PATH}"

RUN mkdir -p /tmp/dev-home && chmod 1777 /tmp/dev-home
ENV HOME=/tmp/dev-home

WORKDIR /workspace
