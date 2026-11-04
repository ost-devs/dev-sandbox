# Estado do trabalho entre sessões: memória ou arquivo de progresso

Uma sessão nova não lê a conversa anterior. O que ela precisa saber para
continuar (onde você parou, o próximo passo, o que falta) tem que estar em
algum lugar que ela leia. Este guia escolhe esse lugar, para qualquer projeto.

Base oficial: as páginas de [memória](https://code.claude.com/docs/en/memory),
[janela de contexto](https://code.claude.com/docs/en/context-window) e
[hooks](https://code.claude.com/docs/en/hooks). Conferido em novembro/2026
(Claude Code 2.1.316).

## A resposta curta

| Situação | Onde fica o estado |
|---|---|
| Padrão, sem configurar nada | **Memória de projeto** (a memória automática do Claude Code) |
| Outra ferramenta ou pessoa precisa ler o estado, ou o progresso é o próprio conteúdo | **Arquivo no repositório**, declarado numa linha do `AGENTS.md` |
| Sempre | **Um lugar só** para cada estado. Se o projeto tem arquivo de progresso, as pendências não ficam também em memória |

Duas fontes para a mesma coisa acabam divergindo, e aí o agente não sabe em
qual acreditar.

## Por que a memória é o padrão

| | Memória de projeto | Arquivo de progresso no repositório |
|---|---|---|
| Carrega sozinho? | Sim: o índice `MEMORY.md` entra em toda sessão (as primeiras 200 linhas ou 25 KB) | Só se o `AGENTS.md` mandar ler ou um hook mostrar |
| Depois de uma compactação | Volta inteira, relida do disco | Um arquivo lido com mais de ~5.000 tokens volta só como caminho |
| Quem mantém | O Claude grava, atualiza e apaga o que terminou, sem você pedir | Precisa de uma instrução para cada sessão manter |
| Polui o repositório? | Não, fica em `~/.claude` | Sim: commits e diffs com anotações que não são o produto |
| Quem vê | Só o Claude Code, só nessa pasta de projeto | Qualquer agente, pessoa ou máquina com o repositório |
| Segue o branch? | Não (anote o branch na memória) | Sim |
| Backup | O seu, de `~/.claude` ([backup e git](../guias/backup-e-git.md)) | O git |

No dev-sandbox, o limite "só nessa pasta de projeto" não pesa. O `dev-docker`
monta o repositório sempre no mesmo caminho, então toda sessão do mesmo
projeto cai na mesma pasta de memória ([o nome da pasta do
projeto](./memoria-e-instrucoes.md#o-nome-da-pasta-do-projeto)). Abra sempre
com o mesmo comando, e com o mesmo `--nome` se você usa um.

## Quando usar um arquivo no repositório

Só quando a memória não alcança quem precisa do estado:

1. **Outra ferramenta ou pessoa lê o estado:** outro agente (Codex, Cursor),
   um colaborador, um CI.
2. **O progresso é o conteúdo:** uma trilha de estudos com o nível atual, o
   roteiro de um livro. Ali o arquivo faz parte do que você está construindo.
3. **Branches longos em paralelo, cada um com estado diferente.**

Nesses casos:

- Declare o arquivo numa linha do `AGENTS.md` (ou `CLAUDE.md`), em inglês:

  ```markdown
  - Progress: `journal/PROGRESS.md` (where we stopped, next step, pending). Read it at start; update it in the same turn the state changes.
  ```

- Se quiser garantir que ele seja lido, um hook `SessionStart` mostra o
  arquivo no início da sessão. O que um hook `SessionStart` imprime entra no
  contexto do Claude. Em `.claude/settings.json` do projeto (o comando roda
  onde o Claude roda, no container):

  ```json
  {
    "hooks": {
      "SessionStart": [
        { "hooks": [ { "type": "command", "command": "cat journal/PROGRESS.md 2>/dev/null; true" } ] }
      ]
    }
  }
  ```

- Não guarde as mesmas pendências também em memória.

## Cada tipo de estado num lugar

| O quê | Onde |
|---|---|
| Pendências, próximo passo, onde parou | Memória de projeto (ou o arquivo declarado no `AGENTS.md`) |
| Trabalho inacabado | Commit no branch e o estado no mesmo lugar acima, com o nome do branch |
| Decisão e o motivo dela, como o projeto funciona | O mapa do projeto ou os docs ([consultor do projeto](./consultor-do-projeto.md)) |
| O que já está no código ou no `git log` | Nada: a sessão nova descobre sozinha |

## No dia a dia

1. **O Claude grava** as pendências em memória quando elas surgem, e apaga
   as concluídas.
2. **Antes de `/clear` ou de parar uma sessão longa**, rode `/consolidar`. Ele
   confere o que ainda está só na conversa e manda cada item para o seu lugar.
   O `/clear` não apaga a conversa: abre uma nova, e a anterior continua no
   `/resume`. Só que a nova não lê a anterior, por isso o `/consolidar` vem antes.
   A skill `/montar-consultor` instala o `/consolidar` em qualquer projeto
   ([montar o consultor](./montar-consultor.md)).
3. **Você revisa** de vez em quando com `/memory`. Se usa a skill
   `/share-memories`, ela pode manter uma nota em português das memórias do
   projeto ([compartilhar memórias](./compartilhar-memorias.md)).

## Aplicar em qualquer projeto

- [ ] Nada a fazer para o padrão: a memória automática já vem ligada.
- [ ] `/consolidar` instalado (`/montar-consultor`).
- [ ] O projeto se encaixa num dos três casos acima? Só então: arquivo de
      progresso, linha no `AGENTS.md`, hook opcional.

## De onde vem cada afirmação

| Afirmação | Fonte |
|---|---|
| `MEMORY.md` carrega em toda sessão, primeiras 200 linhas ou 25 KB | Documentação oficial, [memory](https://code.claude.com/docs/en/memory) |
| A memória automática é relida do disco depois da compactação | Documentação oficial, [context window](https://code.claude.com/docs/en/context-window) ("what survives compaction") |
| Arquivo lido com mais de ~5.000 tokens volta só como caminho | [Trabalhar por projeto](./projetos.md) |
| O que um hook `SessionStart` imprime vira contexto | Documentação oficial, [hooks](https://code.claude.com/docs/en/hooks) |
| A memória é o melhor padrão; um lugar só por estado | Análise deste repositório (novembro/2026), não documentação |
