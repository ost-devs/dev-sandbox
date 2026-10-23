# dev-sandbox

Ambiente de desenvolvimento containerizado (Docker) com Node.js, Rust e um ou
mais agentes de codificação por IA (Antigravity CLI, Claude Code, Codex),
isolado do sistema operacional real, com arquivos criados dentro do
container pertencendo ao seu usuário normal — não a `root`.

Para o *porquê* de cada decisão abaixo, ver [`DOCUMENTACAO.md`](./DOCUMENTACAO.md).

## Por que isso existe

- Um agente de IA executa comandos e edita arquivos de forma autônoma. Se for
  manipulado por conteúdo malicioso (prompt injection num README de um
  repositório de terceiros, por exemplo), ele só tem acesso ao que estiver
  explicitamente disponível dentro do container — não ao resto do seu
  sistema.
- Arquivos criados dentro do container nascem com o dono certo no seu PC real
  (não `root`), então programas como Obsidian, VS Code e Git continuam
  funcionando normalmente sobre os mesmos arquivos.
- Configuração e autenticação de cada agente persistem entre sessões, usando
  as MESMAS pastas que uma instalação nativa (fora do Docker) usaria.

## Pré-requisitos

- Docker instalado (`docker --version` funciona). Se não tiver, ver
  [`DOCUMENTACAO.md`](./DOCUMENTACAO.md#instalar-o-docker).

## Componentes desta configuração

| Componente | Ativo por padrão? | Bloco no `Dockerfile` | Mount extra no script |
|---|---|---|---|
| Node.js 22 + TypeScript | ✅ | `Node.js` | — |
| Rust stable | ✅ | `Rust` | `CARGO_CACHE_PATH` |
| Antigravity CLI (`agy`) | ✅ | `Antigravity CLI` | overlay de `.gemini` |
| Claude Code | comentado | `Claude Code` | overlay de `.claude` |
| Codex CLI | comentado | `Codex CLI` | overlay de `.codex` |

**Para remover um componente ativo:** apague o bloco correspondente no
`Dockerfile` E a linha de `--mount`/variável associada no script (se
houver). As duas partes — senão o script tenta montar uma pasta para uma
ferramenta que não existe mais na imagem (inofensivo, mas desnecessário).

**Para ativar Claude Code ou Codex:** descomente o bloco correspondente no
`Dockerfile`, descomente as linhas associadas no script, reconstrua a
imagem (Parte 1).

---

## Parte 1 — Criar a imagem

```bash
mkdir -p ~/dev-sandbox && cd ~/dev-sandbox
nano Dockerfile
```

Conteúdo do `Dockerfile`:

```dockerfile
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# ── Base do sistema (obrigatório) ────────────────────────────────
RUN apt-get update && apt-get install -y \
    curl git ca-certificates build-essential pkg-config libssl-dev jq unzip \
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
# RUN curl -fsSL https://claude.ai/install.sh | bash

# ── Codex CLI (OpenAI) — opcional, comentado por padrão ──────────
# Exige o bloco Node.js acima. Para ativar: descomente a linha abaixo,
# reconstrua a imagem, e descomente as linhas de CODEX_PATH no script.
# RUN npm install -g @openai/codex

# ── Permissões para rodar como usuário não-root ──────────────────
# Necessário mesmo que você só use um agente — ver DOCUMENTACAO.md.
RUN chmod 755 /root \
    && chmod -R a+rX /root/.local

ENV PATH="/root/.local/bin:${PATH}"

RUN mkdir -p /tmp/dev-home && chmod 1777 /tmp/dev-home
ENV HOME=/tmp/dev-home

WORKDIR /workspace
```

Salvar: `Ctrl+O`, `Enter`, `Ctrl+X`.

Construir a imagem:

```bash
sudo docker build -t dev-sandbox .
```

Reconstrua com o mesmo comando sempre que editar o `Dockerfile` — ativar ou
remover um componente, ou atualizar a versão de alguma ferramenta.

## Parte 2 — Não coloque seu usuário no grupo `docker`

```bash
# NÃO rode isto:
# sudo usermod -aG docker $USER
```

Motivo detalhado em [`DOCUMENTACAO.md`](./DOCUMENTACAO.md#por-que-nao-usar-o-grupo-docker).
Na prática, o custo é digitar a  senha do `sudo` ao iniciar a sessão
(`dev-docker`). O agente não precisa de comandos `docker` para trabalhar; se
ele (ou uma dependência maliciosa) tentar acessar o daemon do Docker para
escapar do container, a falta de sudo bloqueia a ação.

## Parte 3 — Script de atalho

```bash
mkdir -p ~/.local/bin
nano ~/.local/bin/dev-docker
```

Conteúdo:

```bash
#!/bin/bash
set -e

REPO_PATH="$(realpath "${1:-.}")"
HOST_UID="$(id -u)"
HOST_GID="$(id -g)"

# Pasta genérica: qualquer coisa que uma ferramenta gravar em $HOME dentro
# do container, sem overlay específico abaixo, persiste aqui automaticamente.
DEV_HOME_PATH="$HOME/.cache/dev-sandbox/home"

# Credenciais/config REAIS do seu usuário — as mesmas pastas que uma
# instalação nativa (fora do Docker) de cada agente já usa.
GEMINI_PATH="$HOME/.gemini"            # agy
# CLAUDE_PATH="$HOME/.claude"          # Claude Code — descomente se ativou
# CODEX_PATH="$HOME/.codex"            # Codex CLI — descomente se ativou

# Cache de pacotes cargo — separado por design (ver DOCUMENTACAO.md).
CARGO_CACHE_PATH="$HOME/.cache/dev-sandbox/cargo"

mkdir -p "$DEV_HOME_PATH" "$GEMINI_PATH" "$CARGO_CACHE_PATH"
# mkdir -p "$CLAUDE_PATH"    # descomente se ativou Claude Code
# mkdir -p "$CODEX_PATH"     # descomente se ativou Codex

sudo docker run -it --rm \
  --user "$HOST_UID:$HOST_GID" \
  --env "HOME=/tmp/dev-home" \
  --mount "type=bind,src=$REPO_PATH,dst=/workspace" \
  --mount "type=bind,src=$DEV_HOME_PATH,dst=/tmp/dev-home" \
  --mount "type=bind,src=$GEMINI_PATH,dst=/tmp/dev-home/.gemini" \
  --mount "type=bind,src=$CARGO_CACHE_PATH,dst=/usr/local/cargo/registry" \
  --workdir /workspace \
  dev-sandbox:latest
  # Se ativou Claude Code, adicione esta linha ABAIXO da do GEMINI:
  # --mount "type=bind,src=$CLAUDE_PATH,dst=/tmp/dev-home/.claude" \
  # Se ativou Codex, adicione esta linha ABAIXO da do GEMINI:
  # --mount "type=bind,src=$CODEX_PATH,dst=/tmp/dev-home/.codex" \
```

> **⚠️ Ordem importa:** o mount de `$DEV_HOME_PATH` (a pasta inteira)
> precisa vir ANTES dos mounts específicos (`.gemini`, `.claude`, `.codex`)
> na lista de flags — são overlays sobre a pasta genérica, não o
> contrário. Detalhes em
> [`DOCUMENTACAO.md`](./DOCUMENTACAO.md#por-que-a-ordem-dos-mounts-importa).

Tornar executável e garantir que seja encontrado:

```bash
chmod +x ~/.local/bin/dev-docker
echo "$PATH" | grep -q "$HOME/.local/bin" && echo "ok, já está" || echo "falta adicionar"
```

Se faltar (descubra seu shell com `echo "$SHELL"`):

```bash
# bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
# zsh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

## Parte 4 — Uso do dia a dia

```bash
cd /caminho/do/repositorio
dev-docker
```

Ou, de qualquer lugar: `dev-docker ~/caminho/do/repo`.

Dentro do container: `agy`, `node`, `npm`, `cargo`, `rustc` — e `claude` ou
`codex`, se você ativou algum deles — já disponíveis. `exit` destrói o
container (`--rm`); o repositório e as pastas de cache/credenciais no host
continuam intactos.

## Parte 5 — Corrigir arquivos antigos (se você já rodou isso como root antes)

```bash
cd ~/meu-projeto-afetado
sudo chown -R "$(id -u):$(id -g)" .
```

> **⚠️ Cuidado:** rode isso **só** dentro do repositório afetado. Nunca em
> `/` nem numa pasta ampla que contenha dados do sistema.

## Parte 6 — Teste rápido

```bash
mkdir -p ~/dev-sandbox-test && cd ~/dev-sandbox-test
dev-docker
```

Dentro do container, crie um arquivo de teste (`touch teste.txt`) e saia
(`exit`). No host:

```bash
stat -c '%u:%g %n' ~/dev-sandbox-test/teste.txt
```

Compare com `id -u` e `id -g` — os números devem bater.

---

Explicação completa de cada decisão, arquivos de instrução por agente
(`GEMINI.md`/`CLAUDE.md`/`AGENTS.md`), tabela de segurança, troubleshooting
e testes avançados: [`DOCUMENTACAO.md`](./DOCUMENTACAO.md).
