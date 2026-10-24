# Migrar memórias e conversas do Claude entre pastas de projeto

O Claude Code guarda memória e conversas numa pasta com o nome do **caminho
onde você abriu o `claude`** (a raiz do repositório git, se houver):

```text
caminho do projeto           →  pasta no ~/.claude/projects/
/workspace                   →  -workspace
/home/voce/Dev/meu-projeto   →  -home-voce-Dev-meu-projeto
/meu-projeto  (--nome)       →  -meu-projeto
```

Mudou o caminho, mudou a pasta. Nada é apagado: a pasta antiga continua lá,
só não é mais lida. Isso acontece ao sair da v0.1 (tudo era `/workspace`), ao
trocar o caminho do host por `--nome`, ou ao mover/renomear o projeto.

Os comandos abaixo rodam **no host**, com o Claude fechado.

## 1. Ver o que existe

```bash
ls ~/.claude/projects/
ls ~/.claude/projects/-workspace/memory/      # memórias (arquivos .md + o índice MEMORY.md)
ls ~/.claude/projects/-workspace/*.jsonl      # conversas (uma por sessão)
```

Para saber o nome da pasta nova de um caminho: troque tudo que não é letra
ou número por `-`.

```bash
echo "/meu-projeto" | sed 's|[^A-Za-z0-9]|-|g'
```

## 2. Decidir o destino de cada memória

Abra cada arquivo da pasta `memory/` e pergunte: vale para **um** projeto ou
para **todos**?

| Vale para | Destino |
|---|---|
| Um projeto ("os testes de API precisam do Redis") | a pasta `memory/` do projeto novo |
| Todos os projetos ("uso `sudo docker`", "commite sem perguntar") | o seu `~/.claude/CLAUDE.md` (instrução pessoal, carregada em todo projeto), e apague a memória |
| Uma regra que o time ou outros agentes também devem seguir | o `CLAUDE.md`/`AGENTS.md` do repositório (vai para o git) |

Memória é um rascunho pessoal e local; quando ela vira regra, o lugar dela é
um arquivo de instruções ([diferença](./memoria-e-instrucoes.md)).

## 3. Mover

```bash
ANTIGA=~/.claude/projects/-workspace
NOVA=~/.claude/projects/-meu-projeto
mkdir -p "$NOVA/memory"
mv "$ANTIGA/memory/uma-memoria.md" "$NOVA/memory/"
```

Depois edite os dois `MEMORY.md`: tire a linha da memória movida do antigo e
coloque no novo. É só uma lista de links, uma linha por memória.

## 4. E as conversas antigas?

- **Voltar a uma conversa antiga:** `claude --resume <id-da-sessão>` funciona
  **de qualquer pasta**; o Claude procura o ID em todos os projetos da
  máquina. O ID é o nome do arquivo `.jsonl`. No seletor (`claude --resume`
  sem argumento), `Ctrl+A` mostra as conversas de todos os projetos.
- **Levar uma conversa para o projeto novo:** retome-a e use `/cd <caminho>`
  dentro dela; a documentação diz que isso a move para a pasta do novo
  diretório.
- **Não deixe a faxina levar as importantes:** as transcrições somem em 30
  dias (`cleanupPeriodDays`). Como guardar: [preservar conversas](./preservar-conversas.md).

## 5. Conferir

Abra o `claude` no caminho novo e rode `/memory`: a pasta mostrada deve ser a
nova, e as memórias movidas devem aparecer. Quando tudo estiver certo, apague a
pasta antiga (ou mantenha até a faxina das conversas).

---

## Caso real: saída da v0.1 com memórias misturadas em `-workspace`

Numa instalação v0.1, `~/.claude/projects/-workspace/memory/` tinha quatro
memórias de sessões diferentes (diagnóstico de disco, dev-sandbox, um projeto
Rust). As quatro eram preferências pessoais, então o destino certo de todas
era o `~/.claude/CLAUDE.md`, por exemplo:

```markdown
# Personal preferences
- My host user is not in the docker group on purpose: use `sudo docker`; never suggest adding me to it.
- Security advice states what remains exposed, not only what is protected.
- After editing repository files, commit on a working branch without asking; never on main, never push unless asked.
- In learning logs, tag each entry's basis: evidence (where), official docs (URL, date) or analysis (what would confirm it).
```

E as quatro memórias foram apagadas da pasta antiga. As conversas ficaram em
`-workspace` até a faxina; para reabrir uma delas, o comando da seção 4.
