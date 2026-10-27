# Montar o consultor em qualquer projeto

Este guia mostra **como** montar o consultor do projeto em qualquer
repositório, passo a passo. O **porquê** de cada peça está na
[introdução](./consultor-do-projeto.md).

Quem faz o trabalho é a skill `/montar-consultor`, que vem no dev-sandbox
([`utils/skills/montar-consultor/`](../../utils/skills/montar-consultor/SKILL.md)).
Ela lê o projeto, pergunta o que não dá para descobrir sozinha, mostra um
plano e só escreve depois que você aprova.

## O que você terá no fim

| Arquivo no seu projeto | Para que serve | Sempre? |
|---|---|---|
| `AGENTS.md` ou `CLAUDE.md` | Regras que valem em toda tarefa | Sim |
| `.claude/rules/<parte>.md` | Checklist de quem mexe numa parte (ex.: "mudou a API? atualize o cliente") | Se o projeto tiver partes com regras próprias |
| `.claude/skills/<projeto>/SKILL.md` | O mapa: como funciona, decisões que parecem erradas, onde está cada assunto | Se entender o projeto exige ler vários arquivos |
| `.claude/skills/consolidar/SKILL.md` | O `/consolidar`, que guarda o que uma conversa aprendeu | Sim |
| `.claude/agents/<assunto>-pesquisador.md` | Um agente que pesquisa documentação externa e anota o que confirmou | Só se o projeto depende de algo que muda rápido (um framework, uma API) |

Projeto pequeno pode ficar só com as instruções e o `/consolidar`. A skill
avisa quando for o caso, em vez de criar peças vazias.

## 1. Instalar a skill (uma vez só)

A skill fica na sua pasta pessoal do Claude, então serve para todos os seus
projetos. Rode **no host**, trocando `~/dev-sandbox` pelo lugar onde você
clonou o dev-sandbox:

```bash
mkdir -p ~/.claude/skills
cp -r ~/dev-sandbox/utils/skills/montar-consultor ~/dev-sandbox/utils/skills/mirrors ~/.claude/skills/
```

A skill [`mirrors`](./mirrors.md) é opcional, mas
recomendada: com ela, o `/montar-consultor` baixa o `.claude/` do dev-sandbox
para `mirrors/dev-sandbox/` no seu projeto e o usa como exemplo pronto (sempre
na versão mais nova do GitHub). Ele pergunta antes. Sem ela, os modelos
bastam.

Para atualizar depois de um `git pull` no dev-sandbox, rode no host:

```bash
rm -rf ~/.claude/skills/montar-consultor ~/.claude/skills/mirrors
cp -r ~/dev-sandbox/utils/skills/montar-consultor ~/dev-sandbox/utils/skills/mirrors ~/.claude/skills/
```

Conferir: abra uma sessão nova do Claude em qualquer projeto e digite
`/montar`. A skill deve aparecer na lista.

## 2. Escolher o momento

| Situação | O que fazer |
|---|---|
| Você tem uma conversa longa que "conhece" o projeto | **Melhor momento.** Rode `/montar-consultor` nela: a skill aproveita o que a conversa descobriu, que não está em arquivo nenhum |
| Projeto novo ou sem conversa longa | Abra uma sessão nova na raiz do projeto e rode `/montar-consultor`. Ela monta pelo que lê nos arquivos e no `git log` |
| O projeto já tem o consultor | `/montar-consultor auditar`: procura repetição, caminhos que não existem mais e mapa desatualizado |

Rode sempre **na raiz do projeto** (onde fica a pasta `.git`), numa branch de
trabalho, nunca direto na `main`.

## 3. Rodar

```text
/montar-consultor
```

| Etapa | O Claude faz | Você faz |
|---|---|---|
| 1. Levantamento | Lê README, instruções que já existem, arquivos de configuração (`package.json`, `pyproject.toml`...), comandos de teste e o `git log` atrás de decisões. Não escreve nada | Espera |
| 2. Perguntas | Até 4 perguntas, só o que os arquivos não respondem | Responde. A mais importante: **"o que alguém novo erraria aqui?"**. A resposta vira a tabela de decisões do mapa |
| 3. Plano | Mostra uma tabela: arquivo, criar ou editar, o que vai dentro, tamanho | Confere e aprova, ou pede mudanças |
| 4. Escrita | Escreve cada peça a partir de um modelo | Aprova cada arquivo em `.claude/`: o Claude Code protege essa pasta e sempre pergunta |
| 5. Verificação | Confere o formato dos arquivos, os tamanhos, se cada caminho citado existe e se os `paths:` das rules acham arquivos | Espera |
| 6. Relatório | Mostra o que criou, o que deixou de fora e o que ainda falta você responder. Propõe três perguntas de teste | Revisa (abaixo) e decide sobre o commit |

Se o projeto já tem `CLAUDE.md` ou `AGENTS.md`, a skill **edita**, não
substitui. O que só vale para uma parte do projeto sai de lá e vai para uma
rule. Tudo que for movido aparece no relatório.

## 4. Revisar o resultado

A skill não inventa fatos, mas pode errar a importância deles. Leia com
calma, principalmente o mapa:

| Arquivo | Pergunte-se |
|---|---|
| `AGENTS.md` / `CLAUDE.md` | Cada linha vale para **toda** tarefa? Se não, devia estar numa rule |
| Rules | O comando de validação está certo? A tabela "mudou X, atualize Y" está completa? |
| Mapa (`.claude/skills/<projeto>/`) | As decisões têm o motivo certo? Falta alguma armadilha que você conhece? |
| Pesquisador | A fonte oficial é a certa? |

Para ver as mudanças antes do commit, no terminal do projeto:

```bash
git status
git diff
```

## 5. Testar com uma sessão nova

A prova de que funciona é uma conversa que **não viu** a montagem. Rode no
terminal do projeto (host ou container), uma pergunta real por vez:

```bash
claude -p --no-session-persistence "Por que o projeto faz X desse jeito? No fim, diga quais skills e arquivos você leu."
```

Escolha perguntas cuja resposta está no mapa, não no `CLAUDE.md`. Se a
resposta vier genérica ou a skill do projeto não aparecer na lista do fim,
a `description` do mapa precisa citar melhor os assuntos. Peça ao Claude
para ajustá-la.

O `--no-session-persistence` faz a sessão de teste não ficar no histórico.

Para ver o custo fixo, abra uma sessão nova e digite `/context`: as
instruções e rules aparecem em *Memory files*; o mapa, em *Skills* (só a
descrição, até ser usado).

## 6. No dia a dia

| Quando | Faça |
|---|---|
| Cada assunto novo | Abra uma conversa nova. Se a resposta parecer genérica, digite `/<projeto>` para carregar o mapa |
| Antes de encerrar uma conversa longa | `/consolidar`. Ele mostra o que guardou e onde |
| Depois do `/consolidar` | `/clear` sem medo |
| Mudou algo grande no projeto | Atualize o mapa no mesmo commit (a rule de cada parte lembra disso) |
| De tempos em tempos | `/montar-consultor auditar` |

## Montar à mão, sem a skill

Dá para fazer tudo sem a skill. Os modelos estão em
[`utils/skills/montar-consultor/templates/`](../../utils/skills/montar-consultor/templates/),
cada um com as regras de escrita e um esqueleto (em inglês, porque são
arquivos para a IA). Siga esta ordem:

| Ordem | Peça | Modelo |
|---|---|---|
| 1 | Rules das partes | [`rule.md`](../../utils/skills/montar-consultor/templates/rule.md) |
| 2 | Mapa do projeto | [`map-skill.md`](../../utils/skills/montar-consultor/templates/map-skill.md) |
| 3 | Pesquisador (opcional) | [`researcher-agent.md`](../../utils/skills/montar-consultor/templates/researcher-agent.md) |
| 4 | `/consolidar` | [`consolidar.md`](../../utils/skills/montar-consultor/templates/consolidar.md) |
| 5 | Instruções do projeto | [`instructions.md`](../../utils/skills/montar-consultor/templates/instructions.md) |

As instruções vêm por último porque apontam para as outras peças. O exemplo
pronto é o [`.claude/`](../../.claude/) deste repositório.

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| `/montar-consultor` não aparece | Skill não instalada em `~/.claude/skills/`, ou sessão aberta antes da instalação | Confira com `ls ~/.claude/skills/montar-consultor/SKILL.md` e abra uma sessão nova |
| Aparece uma pasta `mirrors/` no projeto | Você aceitou baixar o exemplo do dev-sandbox | É só leitura e fica fora do git (só o `mirrors/mirrors.json` vai). Para tirar: `/mirrors remove dev-sandbox` |
| O Claude ignora o `AGENTS.md` | O projeto também tem `CLAUDE.md`, e aí o Claude Code lê só ele | Ponha `@AGENTS.md` na primeira linha do `CLAUDE.md` |
| A rule não aparece no `/context` | Rules com `paths:` só carregam quando o Claude lê ou edita um arquivo que combina | Normal. Peça para ele abrir um arquivo da parte e confira de novo |
| O mapa não carrega sozinho | A `description` não cita o assunto da pergunta | Chame `/<projeto>` e melhore a `description` |
| Só o `AGENTS.md` foi criado e a skill parou | A escrita em `.claude/` foi recusada. Isso acontece sempre com `claude -p`, mesmo com `--permission-mode acceptEdits` e regra `Edit(.claude/**)` (testado na 2.1.310) | Rode a skill numa sessão interativa e aprove cada arquivo |
| O pesquisador não guarda nada | Memória automática desligada (`memory` depende dela) | Ligue em `/memory` |

## Base

Fatos do Claude Code conferidos nas páginas oficiais de
[skills](https://code.claude.com/docs/en/skills),
[memória](https://code.claude.com/docs/en/memory) e
[subagentes](https://code.claude.com/docs/en/sub-agents):

- skill pessoal em `~/.claude/skills/<nome>/` vale em todos os projetos e
  tem prioridade sobre uma do projeto com o mesmo nome;
- `${CLAUDE_SKILL_DIR}` aponta para a pasta da skill, e é assim que ela acha
  os modelos;
- depois de uma compactação, a skill usada volta com até 5.000 tokens
  (25.000 somando todas): por isso o limite de tamanho do mapa;
- `CLAUDE.md` deve ficar abaixo de 200 linhas;
- rule com `paths:` carrega quando o Claude lê ou edita um arquivo que
  combina; sem `paths:`, carrega sempre;
- o `AGENTS.md` é lido só quando não há `CLAUDE.md`;
- `memory: project` grava em `.claude/agent-memory/<agente>/`.

Dedução (não está na documentação): o limite de ~15.000 caracteres do mapa
é uma estimativa de 5.000 tokens para texto em inglês.

Conferido em outubro/2026 (Claude Code 2.1.310).
