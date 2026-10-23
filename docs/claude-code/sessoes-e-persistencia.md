# Sessões, arquivos temporários e persistência do Claude Code no container

O container do dev-sandbox morre a cada `exit` (`--rm`). Este guia responde:
**o que do Claude Code sobrevive, o que se perde, e como retomar trabalho**
sem deixar o terminal aberto por horas.

## O que fica onde

| O quê | Onde fica no container | Sobrevive ao `exit`? |
|---|---|---|
| Login (`.credentials.json`), `settings.json`, `CLAUDE.md` pessoal, skills, agentes | `~/.claude/` → seu `~/.claude` real do host | ✅ Sim, e é o mesmo do uso nativo |
| Transcrições das conversas (`/resume`, `--continue`) | `~/.claude/projects/<projeto>/*.jsonl` | ✅ Sim |
| Memória automática | `~/.claude/projects/<projeto>/memory/` | ✅ Sim |
| Checkpoints (desfazer edições, `/rewind`) | `~/.claude/file-history/` | ✅ Sim |
| `~/.claude.json` (estado do app: confiança em pastas, MCP pessoais, onboarding) | `/tmp/dev-home/.claude.json` → `~/.cache/dev-sandbox/home/` | ✅ Sim, mas **separado** do `~/.claude.json` nativo |
| Scratchpad e temporários do Claude | `$CLAUDE_CODE_TMPDIR` = `~/.cache/claude-tmp` (v0.2) | ✅ Sim (antes: ❌ ficavam no `/tmp` do container) |
| Processos rodando: servidor `npm run dev`, tarefas em background, `claude --bg` | Memória do container | ❌ Não. Morrem com o container |

### Por que o `~/.claude.json` fica separado

Ele fica **fora** da pasta `~/.claude`, direto na home. Dentro do container a
home é `/tmp/dev-home`, então ele cai no cache genérico. Na prática: a
primeira vez que você abre um projeto no container, o Claude pergunta de
novo se confia na pasta, e servidores MCP adicionados com `claude mcp add`
(escopo de usuário) num lado não aparecem no outro. O login é
compartilhado, porque esse fica em `~/.claude/.credentials.json`.

Montar o arquivo do host por cima não é uma boa ideia: o Claude regrava o
arquivo trocando-o por um novo, e um bind mount de arquivo único quebra com isso.

## A pasta `/tmp/claude-<uid>` (scratchpad)

É onde o Claude guarda arquivos de trabalho da sessão: scripts auxiliares,
saídas longas, imagens coladas. Ele gerencia sozinho: cria por sessão e a
faxina apaga junto com a transcrição (30 dias por padrão, `cleanupPeriodDays`).

- **`/exit` no Claude:** não apaga nada. A pasta continua lá.
- **`exit` do container (v0.1):** perdia tudo, porque `/tmp` era do container.
  Uma sessão retomada com `--continue` citava arquivos que não existiam mais.
- **v0.2:** o `dev-docker` define `CLAUDE_CODE_TMPDIR=/tmp/dev-home/.cache/claude-tmp`.
  A árvore do Claude vai para a home persistente e só ela. Nada além do
  Claude passa a persistir por causa disso: o resto do `/tmp` continua efêmero.

Se o Claude criou algo que você quer guardar, peça para ele mover para o projeto.

## Retomar trabalho em vez de esperar com o terminal aberto

A conversa fica salva no disco a cada mensagem. Bateu o limite de uso? Pode sair:

```bash
exit            # sai do Claude e do container
# ... horas depois ...
dev-docker      # no mesmo repositório
claude --continue          # retoma a última conversa deste projeto
claude --resume            # ou escolhe da lista
```

Isso só funciona direito **por projeto** a partir da v0.2. Antes, com tudo em
`/workspace`, o `--continue` pegava a última sessão de *qualquer* projeto
(ver [memória](./memoria-e-instrucoes.md#o-problema-que-existia-tudo-virava--workspace)).

O que **não** volta: processos que estavam rodando (um build longo, um servidor,
uma tarefa em background). Retome pedindo ao Claude para rodar de novo.

### Para tarefas longas de verdade

| Opção | Precisa do seu PC ligado? | Observação |
|---|---|---|
| Sair e `claude --continue` depois | Só quando voltar | O mais simples. Resolve o caso "esperar o limite voltar" |
| `tmux` dentro do container | Sim, e o container aberto | Sobrevive a fechar a *janela* do terminal, não ao `exit` do container. `tmux` já vem na imagem |
| `claude --remote-control` | Sim, e o container aberto | Acompanhar e responder pelo celular/navegador |
| Claude Code na web (claude.ai/code) ou GitHub Actions | Não | Roda na nuvem da Anthropic sobre o repositório no GitHub. Fora do dev-sandbox: outro ambiente, outras regras |

## Atualizações do Claude Code

Antes da v0.2, o auto-update baixava versões novas para
`~/.cache/dev-sandbox/home/.local/share/claude/` (persistente), mas o `PATH`
continuava apontando para a versão gravada na imagem. Resultado: **baixava,
ocupava espaço (836 MB num caso real) e nunca usava**.

Na v0.2 o auto-update está desligado na imagem (`DISABLE_AUTOUPDATER=1`) e a
atualização é por rebuild, só da camada dos agentes:

```bash
sudo docker build --build-arg AGENTS_REFRESH=$(date +%s) -t dev-sandbox .
```

Para recuperar o espaço das versões órfãs (no host):

```bash
du -sh ~/.cache/dev-sandbox/home/.local/share/claude
rm -rf ~/.cache/dev-sandbox/home/.local/share/claude ~/.cache/dev-sandbox/home/.local/bin/claude
```
