# Memória e instruções no Claude Code

O Claude Code começa cada sessão sem lembrar de nada. Duas coisas carregam
conhecimento de uma sessão para outra:

| | Instruções (`CLAUDE.md`, `AGENTS.md`, rules) | Memória automática (auto memory) |
|---|---|---|
| **Quem escreve** | Você (ou o Claude, quando você pede) | O próprio Claude, por conta própria |
| **O que contém** | Regras e convenções: "use pnpm", "commits em português" | Aprendizados: suas correções, preferências, contexto que não está no código |
| **Onde fica** | No repositório (vai pro git) ou em `~/.claude/` | `~/.claude/projects/<projeto>/memory/` — só na sua máquina |
| **Escopo** | Projeto, usuário ou máquina inteira | Um repositório (compartilhada entre os worktrees dele) |
| **Carregado** | Inteiro, em toda sessão | Só o índice `MEMORY.md` (primeiras 200 linhas ou 25 KB); o resto sob demanda |
| **Compartilhado com o time?** | Sim, se estiver commitado | Não. É pessoal e local |

Nenhum dos dois é uma *trava*: o Claude lê e tenta seguir, mas não há
garantia. Para algo que **precisa** acontecer sempre (bloquear um comando,
rodar o lint antes de commit), use um **hook** em `settings.json`
([instrução ou mecanismo?](./instrucao-ou-mecanismo.md)).

Fonte oficial: <https://code.claude.com/docs/en/memory>. O que está abaixo foi
conferido contra ela em outubro/2026 (Claude Code 2.1.30x).

---

## 1. Instruções: `CLAUDE.md`, `AGENTS.md` e rules

### Onde ficam e quem enxerga

| Arquivo | Para que serve | Vai pro git? |
|---|---|---|
| `/etc/claude-code/CLAUDE.md` | Instruções da **máquina** ("managed"). Não dá para desligar por projeto. [Prova de que carrega sozinho](../aprendizados/2026-10-etc-claude-md-carrega-sozinho.md) | — |
| `~/.claude/CLAUDE.md` | Suas preferências pessoais, em **todos** os projetos | Não (é da sua home) |
| `~/.claude/rules/*.md` | Regras pessoais por tema, em todos os projetos | Não |
| `./CLAUDE.md` ou `./.claude/CLAUDE.md` | Instruções do **projeto**, para o time | Sim |
| `./.claude/rules/*.md` | Regras do projeto por tema, opcionalmente só para certos arquivos | Sim |
| `./CLAUDE.local.md` | Suas notas pessoais neste projeto | Não (coloque no `.gitignore`) |
| `./AGENTS.md` | Padrão aberto, lido por Codex, Claude e outros | Sim |

Regras de carregamento que vale saber:

- Arquivos do diretório atual **e de todos os diretórios acima** carregam no
  início. Os de subpastas carregam quando o Claude mexe num arquivo daquela
  subpasta.
- Tudo é **somado**, nada sobrescreve. Se dois arquivos se contradizem, o
  Claude escolhe um, sem aviso. Evite conflitos.
- O Claude Code lê o `AGENTS.md` **só se não houver** `CLAUDE.md` (ou
  `CLAUDE.local.md`) no projeto. Para ter os dois, coloque `@AGENTS.md` na
  primeira linha do `CLAUDE.md`.
- `@caminho/arquivo.md` dentro de um CLAUDE.md importa outro arquivo (até 4
  níveis). Importar **não economiza contexto**: o arquivo importado carrega
  junto.
- Mantenha cada arquivo com menos de ~200 linhas. Quanto maior, menos ele é
  seguido.

### Rules: instruções que só aparecem quando importam

Um arquivo em `.claude/rules/` com `paths` no topo só entra no contexto
quando o Claude trabalha em arquivos que batem com o padrão:

```markdown
---
paths:
  - "src-tauri/**/*.rs"
---
Use `thiserror` para erros. Nunca `unwrap()` fora de testes.
```

Sem `paths`, a regra carrega sempre, como um pedaço do CLAUDE.md.

**Quando usar o quê:**
- Vale para o projeto inteiro e é curto → `CLAUDE.md` / `AGENTS.md`.
- Vale só para uma parte (o Rust, os testes, a pasta `docs/`) → rule com `paths`.
- É preferência sua, não do time → `~/.claude/CLAUDE.md` ou `CLAUDE.local.md`.
- Tem que acontecer sempre, sem exceção → hook.

---

## 2. Memória automática

### Como funciona

Durante a conversa, o Claude decide sozinho o que vale guardar: uma
correção sua ("não, aqui usamos pnpm"), uma preferência, uma decisão de
projeto, um link para algo fora do repositório. Ele **não** guarda o que dá
para descobrir lendo o código, nem o que o CLAUDE.md já diz.

Cada memória é um arquivo `.md` pequeno; o `MEMORY.md` é o índice, uma
linha por memória:

```text
~/.claude/projects/-home-voce-meu-projeto/memory/
├── MEMORY.md              # índice — carregado em toda sessão
├── feedback-testes.md     # uma memória
└── referencia-staging.md  # outra
```

Os tipos que o Claude usa: `user` (quem você é), `feedback` (como você quer
que ele trabalhe), `project` (decisões e prazos que não estão no código) e
`reference` (onde achar coisas fora do repo).

### É automático?

- **Gravar:** sim, por padrão. Quando aparece "Saved 1 memory" ou
  "Recalled 2 memories", é isso acontecendo. Você também pode pedir:
  *"lembre que os testes de API precisam do Redis rodando"*.
- **Carregar:** sim. O índice entra em toda sessão; cada arquivo é lido
  quando o assunto aparece.
- **Desligar:** `/memory` → alternar *auto memory* (salva
  `"autoMemoryEnabled": false` no seu `~/.claude/settings.json`). Só num
  projeto: o mesmo campo em `.claude/settings.json` do projeto. Por
  variável: `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.
- **Apagar:** é arquivo de texto. Edite ou apague à vontade, ou use `/memory`
  para abrir a pasta.
- **Limpeza automática:** a faxina do Claude Code apaga transcrições
  antigas (30 dias por padrão), mas **não** apaga as memórias.

### O nome da pasta do projeto

`<projeto>` é o caminho da raiz do repositório git com tudo que não é letra
ou número trocado por `-`:

```text
/home/voce/Dev/meu-projeto  →  ~/.claude/projects/-home-voce-Dev-meu-projeto/
```

Todos os worktrees e subpastas do mesmo repositório usam a mesma memória.

---

## 3. Memória dentro do dev-sandbox

O `dev-docker` monta o seu `~/.claude` real dentro do container. Então:

- A memória **sobrevive** ao `--rm`: ela fica no host, não no container.
- É a **mesma** memória de quando você usa o Claude fora do Docker, no mesmo
  projeto, porque o caminho é o mesmo (ver abaixo). Com `--nome`, não: o
  caminho de dentro passa a ser `/nome`.

### O problema que existia: tudo virava `-workspace`

Até a v0.1, todo repositório era montado em `/workspace`. Para o Claude
Code, *todos os seus projetos eram o mesmo projeto*:
`~/.claude/projects/-workspace/`. Isso misturava:

- a memória de projetos diferentes (uma preferência do projeto A aparecia no B);
- a lista do `/resume` (sessões de todos os projetos juntas);
- o histórico do `--continue` (continuava a última sessão de *qualquer* projeto).

Foi descoberto na prática: uma memória sobre o grupo `docker`, gravada numa
sessão de diagnóstico de disco, ficou na mesma pasta usada pelo próprio
repositório dev-sandbox.

**Correção (v0.2):** o `dev-docker` monta o repositório **no mesmo caminho
que ele tem no host** (`/home/voce/Dev/meu-projeto` dentro e fora). Cada
projeto ganha sua pasta. Exceções que continuam em `/workspace`: pastas de
sistema e montagens amplas (`/` ou a home inteira, que pedem confirmação).

Com `dev-docker --nome meu-projeto` o projeto aparece em `/meu-projeto`, e a
memória fica em `~/.claude/projects/-meu-projeto/`: um nome curto, que não
depende do caminho no computador e continua o mesmo em outro PC com o mesmo
backup do `~/.claude`. Em troca, deixa de ser a memória do Claude usado fora
do container ([comparação](../../DOCUMENTACAO.md#projeto-com-nome)).

> Alternativa que existe, mas não foi adotada: manter `/workspace` e definir
> `CLAUDE_CODE_PROJECT_DIR_NAME` por projeto (exige também
> `CLAUDE_CONFIG_DIR`). Montar no caminho real resolve mais coisa de uma vez:
> worktrees, caminhos em mensagens de erro e memória compartilhada com o uso nativo.

### Migrando memórias antigas de `-workspace`

Passo a passo completo, incluindo o que fazer com cada memória: [migrar memórias](./migrar-memorias.md).

No host, veja o que tem lá e mova cada memória para o projeto certo:

```bash
ls ~/.claude/projects/-workspace/memory/
# descubra o nome da pasta nova: o caminho do repo com / trocado por -
echo "$HOME/Dev/meu-projeto" | sed 's|[^A-Za-z0-9]|-|g'
mkdir -p ~/.claude/projects/-home-voce-Dev-meu-projeto/memory
mv ~/.claude/projects/-workspace/memory/alguma-memoria.md \
   ~/.claude/projects/-home-voce-Dev-meu-projeto/memory/
```

Depois, edite os dois `MEMORY.md` (tire a linha de um e coloque no outro).
Se a memória vale para **todos** os projetos, ela é na verdade uma
instrução pessoal: copie o conteúdo para `~/.claude/CLAUDE.md` e apague a
memória.

As sessões antigas (`*.jsonl`) também ficam em `-workspace` e somem do
`/resume` dos projetos novos. Não vale a pena migrar: a faxina automática
apaga essas transcrições em 30 dias, e se precisar de alguma antes disso, é
um arquivo de texto (JSON por linha) que dá para ler direto.

---

## 4. Possibilidades (e como usar bem)

- **Ensine uma vez.** Corrigiu o Claude ("não use `unwrap`", "rode os testes
  com `--release`")? Diga *"lembre disso"*. Na próxima sessão ele já sabe.
- **Promova o que ficou estável.** Memória é pessoal. Quando uma memória vira
  regra do projeto, mova para o `CLAUDE.md` ou para uma rule: aí ela vai
  pro git e vale para o time e para outros agentes.
- **Contexto que não está no código:** "o deploy é sexta", "a API de
  pagamentos é mock até março", "o cliente prefere telas simples".
- **Referências:** onde fica o board, o dashboard, a planilha.
- **Subagentes com memória própria:** um subagente pode ter a sua pasta de
  memória (campo `memory` na definição do agente), separada da conversa principal.
- **Revise de vez em quando.** Memória velha engana. O Claude marca a data
  (`modified`) em cada uma, mas quem sabe se ainda vale é você.
- **Backup:** memória é local e não vai pro git do projeto. Para não perder,
  ver [Backup e git](../guias/backup-e-git.md).

### O que **não** colocar na memória (nem no CLAUDE.md)

Senhas, tokens, chaves de API. Tudo isso fica em texto puro no disco e, se
você fizer backup em git, vai junto. Ver [Segurança](../guias/seguranca.md).

---

## Comandos úteis

| Comando | O que faz |
|---|---|
| `/memory` | Lista os arquivos de instrução e memória, liga/desliga a memória automática, abre a pasta |
| `/context` | Mostra quais CLAUDE.md e rules foram carregados nesta sessão |
| `/init` | Cria um CLAUDE.md inicial analisando o projeto |
| `claude purge <caminho> --dry-run` | Mostra o que seria apagado (transcrições **e memória**) de um projeto |
