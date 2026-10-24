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

### O jeito básico

1. **Abra um terminal na pasta do projeto.** O jeito mais fácil: no
   gerenciador de arquivos, clique com o botão direito na pasta do projeto e
   escolha **"Abrir no terminal"** (o nome muda conforme o sistema: "Abrir em
   um terminal", "Open in Terminal"). Quem prefere o teclado: abra o terminal
   e digite `cd ~/Projetos/meu-site` (o `~` é a sua pasta pessoal,
   `/home/seu-usuario`).
2. Digite `dev-docker`. Ele abre o container com essa pasta dentro.
3. Dentro do container, digite `claude` (ou `codex`, `agy`).

O projeto aparece dentro do container no mesmo caminho que tem no seu
computador, e o Claude guarda memória e conversas separadas por projeto.

<a id="atalho"></a>
### O macete: um comando só seu para cada projeto

Para o projeto que você abre todo dia, dá para criar **uma vez** um comando
com o nome do projeto. Depois disso, basta abrir qualquer terminal
(`Ctrl+Alt+T`) e digitar esse comando: sem procurar a pasta, sem `cd`.

**Criando (uma vez por projeto):**

1. Abra o terminal **na pasta do projeto**, como no passo 1 acima.
2. Escolha um nome curto para o projeto (letras minúsculas, números e hífen;
   por exemplo `meu-site`) e digite:

   ```bash
   dev-docker --atalho meu-site
   ```

   Aqui `meu-site` é o nome que **você** escolhe. Sem mais nada depois do
   nome, ele usa a pasta onde o terminal está.
3. Ele mostra qual pasta vai guardar e pergunta. **Confira a pasta**, e só então
   digite `s`:

   ```text
   $ dev-docker --atalho meu-site
   O comando dev-docker-meu-site vai abrir sempre esta pasta:
       /home/ana/Projetos/meu-site
   Confirma? Digite 's' para criar: s
   Pronto. De qualquer terminal, em qualquer pasta, digite:  dev-docker-meu-site
   ```

**Usando (todos os dias):** abra qualquer terminal e digite

```bash
dev-docker-meu-site
```

Ele abre o container com o projeto, que lá dentro fica em `/meu-site`. Depois
é só `claude`, como sempre.

**Cuidados:**

- **A pasta certa é a raiz do projeto:** a que tem o `.git`, ou onde ficam o
  `README`, o `package.json`, o `Cargo.toml`. Não uma subpasta (`src`), nem a
  pasta de cima. Se a pasta não tem `.git`, ele avisa; a sua pasta pessoal
  inteira e a raiz do sistema ele recusa.
- **Errou a pasta?** Abra o terminal na pasta certa e rode o mesmo
  `dev-docker --atalho meu-site`: ele mostra para onde o atalho aponta hoje e
  troca depois que você confirmar.
- **Ver todos os seus atalhos:** `dev-docker --atalhos`. **Apagar um:**
  `rm ~/.local/bin/dev-docker-meu-site`.
- **Moveu ou renomeou a pasta do projeto** (ou a do dev-sandbox)? O atalho
  continua apontando para o lugar antigo: crie de novo.
- **Também dá para passar o caminho** em vez de abrir o terminal na pasta:
  `dev-docker --atalho meu-site ~/Projetos/meu-site`.
- **Memória do Claude:** com atalho, ela fica guardada pelo nome do projeto
  (`~/.claude/projects/-meu-site/`), e não pelo caminho. Se o projeto já tinha
  memória do jeito básico, ela fica na pasta antiga:
  [como migrar](docs/claude-code/migrar-memorias.md). Os prós e contras estão em
  [projeto com nome](DOCUMENTACAO.md#projeto-com-nome).

### Outras coisas do dia a dia

| Quero... | Como |
|---|---|
| Abrir o site no navegador do host | `DEV_PORTS="5173" dev-docker` e o servidor em `0.0.0.0` ([guia](docs/guias/portas-e-sessoes-paralelas.md)) |
| Outro terminal no mesmo container | `sudo docker exec -it <nome-mostrado-ao-iniciar> bash` |
| Dois agentes no mesmo projeto | `claude --worktree <nome>` ([guia](docs/guias/portas-e-sessoes-paralelas.md#dois-agentes-no-mesmo-projeto)) |
| Retomar a conversa depois do `exit` ou do limite de uso | Reabra o projeto do mesmo jeito (mesmo caminho ou mesmo nome) e `claude --continue` ([guia](docs/claude-code/sessoes-e-persistencia.md)) |
| Não perder uma conversa importante (o Claude apaga as antigas em 30 dias) | `/rename`, `/export` e anote o ID ([guia](docs/claude-code/preservar-conversas.md)) |
| Atualizar os agentes | `sudo docker build --build-arg AGENTS_REFRESH=$(date +%s) -t dev-sandbox .` |
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

## Documentação

- [`CHANGELOG.md`](CHANGELOG.md): o que mudou em cada versão e como atualizar.
- [`DOCUMENTACAO.md`](DOCUMENTACAO.md): o *porquê* de cada decisão do script e do `Dockerfile`.
- [`docs/`](docs/README.md): guias (segurança, backup, portas, imagem), Claude Code
  (projetos, memória, sessões, conversas, modelo e esforço) e
  [aprendizados](docs/aprendizados/README.md) da comunidade.
