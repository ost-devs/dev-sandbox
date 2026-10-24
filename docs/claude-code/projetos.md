# Trabalhar com o Claude Code por projeto

Como o Claude Code entende "um projeto", o que fica guardado por projeto e o
que é global, como organizar projetos com vários repositórios, e como manter
memória e instruções úteis ao longo de semanas. Base: a documentação oficial
([memória](https://code.claude.com/docs/en/memory),
[contexto](https://code.claude.com/docs/en/context-window),
[boas práticas](https://code.claude.com/docs/en/best-practices),
[uso em paralelo](https://code.claude.com/docs/en/agent-view)), lida em
outubro/2026.

## 1. O que é "um projeto" para o Claude Code

É o **caminho onde você abre o `claude`**. Se esse caminho está dentro de um
repositório git, vale a raiz do repositório. Tudo que é "do projeto" sai daí:

| Por projeto (pasta em `~/.claude/projects/<caminho>/`) | Global (vale em todo projeto) |
|---|---|
| Memória automática (`memory/`) | `~/.claude/CLAUDE.md` e `~/.claude/rules/`: suas preferências |
| Conversas: o que `--continue` e `--resume` encontram | Login, `~/.claude/settings.json` |
| | Skills e agentes em `~/.claude/skills/`, `~/.claude/agents/` |

E, dentro do repositório (vai para o git): `CLAUDE.md` ou `AGENTS.md`,
`.claude/rules/`, `.claude/settings.json`, `.claude/skills/`, `.claude/agents/`.

Consequência prática: **abra o projeto sempre pelo mesmo caminho**. Abrir uma
vez pela raiz e outra por uma pasta acima cria duas memórias e duas listas de
conversas.

## 2. Abrir projetos no dev-sandbox

| Jeito | Caminho dentro | Memória em | Bom para |
|---|---|---|---|
| `cd ~/Dev/app && dev-docker` | o mesmo do host | `-home-voce-Dev-app` | usar o Claude dentro e fora do container com a mesma memória |
| `dev-docker --nome app ~/Dev/app` | `/app` | `-app` | caminho curto e memória que não depende do computador |
| `dev-docker --atalho app` uma vez, num terminal aberto na pasta do projeto; depois `dev-docker-app` de qualquer terminal ([passo a passo](../../README.md#atalho)) | `/app` | `-app` | projetos que você abre todo dia |

Os prós e contras completos estão na [DOCUMENTACAO](../../DOCUMENTACAO.md#projeto-com-nome).
Trocou de jeito? A memória fica na pasta antiga: [migrar](./migrar-memorias.md).

## 3. Um projeto que consulta outros repositórios

Caso comum: você trabalha num repositório e quer que a IA consulte outros
(a biblioteca que você está portando, um projeto de referência). Clonar tudo
lado a lado numa pasta e abrir a pasta inteira funciona, mas cria três
problemas: as referências nos documentos dependem do layout da sua máquina,
as versões consultadas não ficam registradas, e o `.git` de cada clone vira
mais uma [porta de entrada](../guias/seguranca.md).

O que funciona melhor, testado num projeto real:

1. Uma pasta `mirrors/` **dentro** do repositório, no `.gitignore`.
2. Um manifesto versionado (por exemplo `mirrors.json`) com, para cada fonte:
   URL, commit exato e licença.
3. Um script que baixa cada fonte no commit fixado, **sem** `.git`.
4. Documentos e instruções citam tudo a partir da raiz do repositório:
   `mirrors/biblioteca/src/arquivo.ts:120`.

Ganhos: o agente abre o caminho como está escrito; outra máquina ou outra
pessoa reconstrói tudo com um comando; trocar de versão é um diff no
manifesto; e a busca do Claude (que usa o `rg`) **ignora** `mirrors/` quando
procura a partir da raiz, sem misturar o código consultado com o seu. Para
buscar lá dentro, o caminho é dado explicitamente.

## 4. Onde colocar cada instrução

| Coloque em | Quando | Por quê |
|---|---|---|
| `~/.claude/CLAUDE.md` | preferência sua para todos os projetos | carrega em toda sessão, de todo projeto |
| `CLAUDE.md` ou `AGENTS.md` do repositório | regra que vale em toda tarefa do projeto | carrega em toda sessão e volta depois de cada compactação; **mantenha abaixo de ~200 linhas**, porque ocupa contexto em toda mensagem e, longo demais, é menos seguido |
| `.claude/rules/x.md` com `paths:` | regra de uma parte do código (só o Rust, só os testes) | carrega só quando o Claude mexe nesses arquivos |
| Um documento comum (`docs/...`) citado nas instruções | procedimento longo de uma fase ou tarefa | lido quando preciso, sem limite de tamanho. Cuidado: depois de uma compactação, um arquivo lido com mais de ~5.000 tokens volta **só como caminho**; deixe escrito num arquivo de progresso o que reler |
| Skill (`.claude/skills/<nome>/SKILL.md`) | um fluxo que você dispara (`/nome`) | o corpo só carrega quando usado |
| Hook (`.claude/settings.json`) | algo que **tem** de acontecer sempre | é executado pelo Claude Code, não depende do modelo obedecer |

Duas regras que evitam metade dos problemas:

- **Cada regra num lugar só.** Se dois arquivos dizem coisas diferentes, o
  Claude pode seguir qualquer um. Repetir "para reforçar" gera essa divergência
  com o tempo.
- **`CLAUDE.md` e `AGENTS.md` juntos:** o Claude só lê o `AGENTS.md` se não
  houver `CLAUDE.md`. Para usar os dois, o `CLAUDE.md` contém só a linha
  `@AGENTS.md`.

## 5. O ciclo da memória

1. **O Claude grava** sozinho correções e preferências ("Saved 1 memory").
   Você também pode pedir: *"lembre que..."*.
2. **Você revisa** de vez em quando: `/memory` abre a pasta. Memória velha
   engana; apague o que não vale mais.
3. **Você promove** o que ficou estável: vale para todos os projetos → seu
   `~/.claude/CLAUDE.md`; vale para o projeto e para quem mais trabalha nele →
   `CLAUDE.md`/`AGENTS.md` do repositório.
4. **Você faz backup**: memória é local ([backup e git](../guias/backup-e-git.md)).

O índice `MEMORY.md` carrega em toda sessão (as primeiras 200 linhas). Cada
memória detalhada só é lida quando o assunto aparece.

## 6. Sessões longas e limites de uso

- **Nomeie** a sessão (`/rename auditoria-view`) e volte a ela com
  `claude --resume`. `claude --continue` retoma a última do projeto.
- **`/clear` entre tarefas sem relação.** Contexto velho atrapalha e gasta
  tokens em toda mensagem.
- **Estado em arquivos, não na conversa.** Peça ao agente para manter um
  arquivo de progresso (feito, falta, próximo passo) e commitar antes de
  parar. Qualquer sessão nova continua dali.
- **Limite de uso no meio de uma tarefa longa:** o Claude continua sozinho
  quando o limite volta, **mas só numa sessão interativa que continua
  aberta**. Sessões em background (`claude --bg`) e `claude -p` não esperam.
  Para não ficar com o terminal aberto, rode tudo dentro de um `tmux` **no
  host** (lá fora, não dentro do container):

  ```bash
  tmux new -s meu-projeto          # no host
  dev-docker-meu-projeto           # dentro do tmux
  claude                           # dentro do container
  # Ctrl+b e depois d: sai do tmux, tudo continua rodando
  tmux attach -t meu-projeto       # volta depois
  ```

  O `tmux` dentro do container também existe na imagem, mas o que acontece com
  o container quando você fecha o terminal que rodou o `dev-docker` não foi
  testado; com o `tmux` no host essa dúvida não existe (instale com
  `sudo apt install tmux`). Com a máquina dormindo mais de ~30 minutos, o
  Claude pede um Enter antes de continuar. Detalhes:
  [sessões e persistência](./sessoes-e-persistencia.md).
- **Trabalho em paralelo no mesmo projeto:** `claude --worktree <nome>` (cada
  agente no seu checkout), ou outro container
  ([guia](../guias/portas-e-sessoes-paralelas.md)).

## 7. Checklist de um projeto bem configurado

- [ ] Abro sempre pelo mesmo caminho (ou pelo atalho `dev-docker-<nome>`).
- [ ] `CLAUDE.md`/`AGENTS.md` curto, com o que vale em toda tarefa e links para o resto.
- [ ] Nenhuma regra repetida em dois arquivos.
- [ ] Repositórios consultados em `mirrors/`, com versão fixada.
- [ ] O agente mantém um arquivo de progresso e commita antes de parar.
- [ ] Reviso `/memory` de tempos em tempos e promovo o que ficou estável.
- [ ] `~/.claude` tem backup.
