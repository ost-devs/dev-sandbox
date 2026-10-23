# dev-sandbox

Ambiente Docker para rodar agentes de IA de programação (Claude Code, Codex,
Antigravity CLI) **isolados do seu sistema**, com os arquivos do projeto
pertencendo ao seu usuário normal, não a `root`.

- O agente só enxerga o projeto aberto e as próprias configurações. Suas chaves
  SSH, navegador, documentos e outros projetos ficam fora do alcance.
- Arquivos criados dentro do container nascem com o seu dono no host:
  VS Code, Obsidian e git continuam funcionando normalmente.
- Login, configurações e memória dos agentes persistem entre sessões, nas
  mesmas pastas que uma instalação nativa usaria.

Isolamento não é invulnerabilidade: leia [o que o sandbox protege e o que
não protege](docs/guias/seguranca.md) antes de confiar nele para código de terceiros.

## O que vem na imagem

| Categoria | Inclui |
|---|---|
| Agentes | Claude Code, Codex CLI, Antigravity CLI (`agy`) |
| Linguagens | Python 3 + `uv`, Node.js 22 + pnpm/yarn/TypeScript, Rust + clippy/rustfmt, C/C++ (`gcc`, `clang`, `cmake`) |
| Opcionais no build | Go (`WITH_GO=1`), Java + Maven (`WITH_JAVA=1`) |
| Navegador e desktop | Chromium headless (Puppeteer/Playwright), bibliotecas do Tauri v2 |
| Utilitários | `git`, `rg`, `fd`, `jq`, `rsync`, `sqlite3`, `tmux`, `lsof`, `ip`, `dig`, `nc`... |

É uma imagem grande (6–8 GB) de propósito: [por quê](docs/guias/filosofia-da-imagem.md).

## Instalação

**1. Docker.** Se ainda não tem, ver [Instalar o Docker](DOCUMENTACAO.md#instalar-o-docker).
**Não** coloque seu usuário no grupo `docker` ([motivo](DOCUMENTACAO.md#por-que-nao-usar-o-grupo-docker)):
o custo é digitar a senha do `sudo` ao abrir uma sessão.

**2. Clone e construa a imagem:**

```bash
git clone https://github.com/ost-devs/dev-sandbox ~/dev-sandbox
cd ~/dev-sandbox
sudo docker build -t dev-sandbox .
```

**3. Instale o comando `dev-docker`** como um link para o script do repositório.
Assim, um `git pull` já atualiza o script:

```bash
mkdir -p ~/.local/bin
ln -sf ~/dev-sandbox/dev-docker ~/.local/bin/dev-docker
echo "$PATH" | grep -q "$HOME/.local/bin" && echo "ok" || echo 'falta: adicione export PATH="$HOME/.local/bin:$PATH" ao ~/.bashrc'
```

**4. Teste:**

```bash
mkdir -p ~/dev-sandbox-teste && cd ~/dev-sandbox-teste
dev-docker
touch teste.txt && exit
stat -c '%u:%g %n' teste.txt    # deve bater com: echo "$(id -u):$(id -g)"
```

## Uso

```bash
cd ~/Dev/meu-projeto
dev-docker                         # ou: dev-docker ~/Dev/meu-projeto
claude                             # (ou codex, agy) dentro do container
```

| Quero... | Como |
|---|---|
| Abrir o site no navegador do host | `DEV_PORTS="5173" dev-docker` e o servidor em `0.0.0.0` ([guia](docs/guias/portas-e-sessoes-paralelas.md)) |
| Outro terminal no mesmo container | `sudo docker exec -it <nome-mostrado-ao-iniciar> bash` |
| Dois agentes no mesmo projeto | `claude --worktree <nome>` ([guia](docs/guias/portas-e-sessoes-paralelas.md#dois-agentes-no-mesmo-projeto)) |
| Retomar a conversa depois do `exit` ou do limite de uso | `claude --continue` ([guia](docs/claude-code/sessoes-e-persistencia.md)) |
| Atualizar os agentes | `sudo docker build --build-arg AGENTS_REFRESH=$(date +%s) -t dev-sandbox .` |
| Pasta com vários repositórios cuja documentação usa `/workspace/...` | `DEV_MOUNT_AT=/workspace dev-docker` ([trade-off](DOCUMENTACAO.md#por-que-o-projeto-e-montado-no-mesmo-caminho-do-host)) |
| Mexer em `.git/config` de dentro (ex.: `git remote add`) | `DEV_GIT_RW=1 dev-docker` ([por que é bloqueado](docs/guias/seguranca.md#a-ponte-mais-perigosa-código-que-roda-fora-do-container)) |

`exit` destrói o container. O projeto, os logins e os caches continuam no host.
Faça `git push` pelo terminal do host: as chaves SSH não entram no container.

## Instruções do ambiente para os agentes

O arquivo [`sandbox/AGENTS.md`](sandbox/AGENTS.md) explica ao agente onde ele
está: o que persiste, que não há `sudo`, como lidar com portas e com
ferramentas que faltam. Ele vai para dentro da imagem.

- **Claude Code:** carrega sozinho (a imagem o instala em `/etc/claude-code/CLAUDE.md`).
- **Codex e agy:** acrescente uma linha ao arquivo global de instruções do
  agente no host (`~/.codex/AGENTS.md` e `~/.gemini/GEMINI.md`). Fora do
  container a condição é falsa e nada muda:

  ```markdown
  If the environment variable DEV_SANDBOX is 1, read /etc/dev-sandbox/AGENTS.md before starting any task.
  ```

## Vindo da v0.1?

1. `git pull` e reconstrua a imagem (`sudo docker build -t dev-sandbox .`).
2. Troque a cópia antiga do script pelo link:
   `mv ~/.local/bin/dev-docker ~/.local/bin/dev-docker.v01.bak` e o passo 3 da instalação.
   Se você tinha mudanças próprias (portas, mounts), veja `DEV_PORTS` acima antes de reaplicar.
3. O projeto agora aparece no container no mesmo caminho do host, e não em
   `/workspace`. Memórias antigas do Claude ficaram em `~/.claude/projects/-workspace/`:
   [como migrar](docs/claude-code/memoria-e-instrucoes.md#migrando-memórias-antigas-de--workspace).
4. Recupere o espaço do auto-update órfão do Claude:
   `rm -rf ~/.cache/dev-sandbox/home/.local/share/claude ~/.cache/dev-sandbox/home/.local/bin/claude`.

## Documentação

- [`DOCUMENTACAO.md`](DOCUMENTACAO.md): o *porquê* de cada decisão do script e do `Dockerfile`.
- [`docs/`](docs/README.md): guias (segurança, backup, portas, imagem), Claude Code
  (memória, sessões) e [aprendizados](docs/aprendizados/README.md) da comunidade.
