# Backup e git: o que dá para desfazer se o agente fizer besteira

A ideia de "está tudo no git, se der ruim eu reverto" é boa, mas ela cobre
menos do que parece. Este guia mostra o que o git protege, o que não protege,
e como fazer backup das configurações dos agentes sem vazar segredos.

## O que o git do projeto protege

| Situação | Dá para desfazer pelo git? |
|---|---|
| Agente editou/apagou arquivos **já commitados** | ✅ `git restore`, `git checkout`, `git revert` |
| Agente fez commits ruins | ✅ `git reset` / `git revert` (o reflog guarda tudo por ~90 dias) |
| Mudanças que **ainda não foram commitadas** | ❌ Perdidas se o agente sobrescrever. Por isso: commit frequente |
| Arquivos ignorados ou fora do git: `.env`, banco SQLite local, `uploads/`, dados | ❌ O git nunca viu |
| O agente apagou ou reescreveu o próprio `.git` (`rm -rf .git`, `push --force`, `filter-branch`) | ❌ Localmente, não. Só uma cópia **remota** salva |

Conclusões práticas:

1. **Commit pequeno e frequente.** Peça ao agente para commitar a cada mudança
   lógica, sem perguntar (veja o [`AGENTS.md`](../../AGENTS.md) deste repo
   como exemplo). Cada commit vira um ponto de restauração.
2. **O backup de verdade é o remoto.** Faça `git push` (do host: as chaves SSH
   não estão no container) com frequência. Um repositório privado no GitHub/GitLab
   ou um bare repo em outro disco: `git clone --bare . /mnt/backup/projeto.git`.
3. **Dados fora do git precisam de outro backup.** Se o projeto tem um banco
   local ou arquivos importantes ignorados, copie-os para fora (ou use
   Déjà Dup, Borg, restic, rsync para outro disco).
4. O Claude Code tem **checkpoints** (`/rewind`, ou `Esc` duas vezes) que
   desfazem as edições que *ele* fez com as ferramentas de edição. Não cobrem
   o que ele fez via comandos de terminal (`rm`, `mv`, scripts).

> **E o Timeshift?** Ele é para o *sistema* (recuperar um Linux quebrado por
> atualização), não para os seus projetos. Na configuração padrão a sua home
> fica de fora, e é bom que fique: ver o
> [aprendizado do disco cheio](../aprendizados/2026-10-disco-cheio-timeshift-docker.md).

## Configurações dos agentes: `.claude`, `.gemini`, `.codex`

Essas pastas ficam **só na sua máquina**. O `dev-docker` monta as pastas
reais do host, então perder o disco (ou apagar a pasta) perde:

- suas instruções pessoais (`~/.claude/CLAUDE.md`), rules, skills, agentes, comandos;
- `settings.json` (permissões, hooks, modelo);
- a memória automática de cada projeto.

Também moram ali coisas que **não podem** ir para um git, nem privado:

- credenciais (`~/.claude/.credentials.json`, `~/.codex/auth.json`,
  `~/.gemini/oauth_creds.json`);
- transcrições completas das conversas (`~/.claude/projects/*/*.jsonl`,
  `~/.codex/sessions/`): **tudo** que passou pela conversa fica nelas,
  inclusive um `.env` que o agente leu ou um token que você colou.

### Receita: git dentro da própria pasta, ignorando tudo por padrão

Crie o repositório **dentro** de `~/.claude` com um `.gitignore` que ignora
tudo e libera só o que você escolher (lista branca). Funciona igual no host e
no container, porque a pasta é a mesma.

> Por que não um repositório separado com links simbólicos para dentro de
> `~/.claude`? Dentro do container, o link aponta para um caminho do host que
> não está montado, e o arquivo some.

No host:

```bash
cd ~/.claude
git init
nano .gitignore
```

```gitignore
# Tudo ignorado por padrão; libera só o que é configuração sua.
*
!.gitignore
!CLAUDE.md
!settings.json
!keybindings.json
!rules/
!rules/**
!skills/
!skills/**
!agents/
!agents/**
!commands/
!commands/**
!output-styles/
!output-styles/**
# Memória automática de cada projeto (sem as transcrições)
!projects/
!projects/*/
!projects/*/memory/
!projects/*/memory/**
```

Confira **antes** do primeiro commit:

```bash
git add -A && git status --short       # só o que você liberou deve aparecer
git grep -nIiE 'token|secret|api[_-]?key|password|sk-' --cached   # nada sensível?
git commit -m "backup inicial"
```

Essa lista foi testada: credenciais, transcrições (`*.jsonl`), `history.jsonl`,
`file-history/` e `plugins/` ficam de fora.

O mesmo vale para as outras pastas, liberando só:

| Pasta | Liberar | Nunca liberar |
|---|---|---|
| `~/.gemini` | `settings.json`, `GEMINI.md`, `commands/` | `oauth_creds.json`, `google_accounts.json`, `tmp/`, histórico |
| `~/.codex` | `config.toml`, `AGENTS.md`, `prompts/` | `auth.json`, `sessions/`, `history.jsonl`, `log/` |

Os nomes de arquivos de credencial mudam entre versões. Rode `ls -la` na
pasta e na dúvida, não libere.

Depois, crie um repositório **privado** e faça `git push` do host. Automatize
com um `cron` ou `systemd timer` se quiser (`git add -A && git commit -m auto && git push`).

### Tokens e chaves em git privado: o risco

"Privado" não quer dizer "secreto":

- Se a sua conta do GitHub for invadida, o invasor lê tudo.
- Um repositório pode virar público por engano, ser forkado, ou ser lido por
  um app/integração com acesso ao repo (CI, bots, ferramentas de IA).
- O git guarda o histórico **para sempre**. Apagar o arquivo depois não
  resolve: precisa reescrever o histórico **e** trocar a credencial.

Regra: **credencial não vai pro git.** Para os agentes isso nem faz falta:
basta fazer login de novo (`/login` no Claude, `codex login`), coisa de um
minuto. Se você precisa guardar uma chave de API, use um gerenciador de
senhas (Bitwarden, KeePassXC) ou criptografe antes (`age`, `sops`, `git-crypt`).

### `settings.json` também pode ter segredo

O bloco `env` do `settings.json` às vezes recebe uma chave de API ou o token
de um servidor MCP. Por isso o `git grep` acima. Prefira variáveis de
ambiente do shell ou um arquivo fora do repositório para esses valores.
