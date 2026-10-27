# Branches com agentes: uma branch `claude` no dia a dia

No dia a dia, o agente trabalha numa branch só, chamada `claude`. Você revisa o
que ele fez e junta na `main` quando quiser. Uma branch nova só aparece quando
o trabalho precisa ficar **separado** do resto: um experimento que pode ir para
o lixo, dois agentes ao mesmo tempo, algo que não pode entrar na `main` ainda.

## Por que não uma branch por tarefa

**Quem desfaz é o commit, não a branch.** Se o agente faz um commit por mudança
lógica, `git revert <commit>` desfaz uma coisa só, sem mexer no resto. Você não
precisa de uma branch por tarefa para conseguir voltar atrás.

Uma branch por tarefa pequena custa caro no cotidiano: são muitos nomes, muitos
merges e muitas branches esquecidas. Neste repositório, em três dias de
trabalho (outubro/2026), juntaram-se sete branches locais além da `main`. Três
já tinham entrado na `main` e nunca foram apagadas, e duas ficaram paradas sem
merge.

**Por que não commitar direto na `main`, então?** Porque a `main` é o que você
**revisou**, e a `claude` é o que o agente fez e você ainda não olhou. A
fronteira entre as duas é a sua revisão. Ela também protege o `git push`: só a
`main` vai para o GitHub.

## O ciclo do dia a dia

| Passo | Quem | Comando |
|---|---|---|
| 1. Começar na `claude` (ela é criada a partir da `main` se não existir) | Agente | `git switch claude` ou `git switch -c claude main` |
| 2. Se a `main` andou (você commitou pelo host), trazer para a `claude` | Agente | `git merge main` |
| 3. Trabalhar, um commit por mudança | Agente | — |
| 4. Ver o que ainda não foi revisado | Você | `git log --oneline main..claude` e `git diff main..claude` |
| 5. Desfazer um commit de que não gostou | Você ou agente | `git revert <commit>` (na `claude`) |
| 6. Juntar na `main` | Você | `git switch main && git merge --ff-only claude && git switch claude` |
| 7. Publicar | Você, **no host** | `git push` (na `main`) |

Os passos 1 a 6 funcionam dentro do container. O passo 7, não: as chaves SSH
não entram no container ([por quê](./seguranca.md)).

Se o `merge --ff-only` recusar, é porque a `main` tem commits que a `claude` não
tem. Rode `git merge main` na `claude` (passo 2) e tente de novo.

A `claude` **não vai para o GitHub**. Como o `.git/config` é somente leitura
dentro do container, um `git push -u` daqui falharia de qualquer forma.

## Quando abrir outra branch

A pergunta que decide: **"vou querer jogar isto fora inteiro, ou segurar isto
enquanto o resto segue para a `main`?"** Se a resposta for sim, use uma branch
própria. Se for não, use a `claude`.

| Situação | Por que separar | Nome sugerido |
|---|---|---|
| Experimento que pode ir para o lixo (refatoração arriscada, testar uma ideia) | Apagar a branch é mais limpo que reverter dez commits | `exp/<assunto>` |
| Dois agentes ao mesmo tempo no mesmo projeto | Na mesma pasta e na mesma branch, um atropela o outro | Use worktree: `claude --worktree <nome>` cria a branch ([guia](./portas-e-sessoes-paralelas.md#dois-agentes-no-mesmo-projeto)) |
| Trabalho longo (dias) que não pode travar o resto | As correções pequenas continuam indo para a `main`, e o trabalho longo entra quando terminar | `feat/<assunto>` |
| Precisa de um teste que o agente não consegue fazer antes de entrar | Ex.: mudança no `dev-docker` que só se testa com Docker de verdade no host | `feat/<assunto>` |
| Variante que nunca vai para a `main` | Ex.: a branch `pessoal` deste repositório, com a sua imagem | Nome próprio |
| Contribuição para o projeto de outra pessoa (PR) | O PR precisa conter só aquela mudança | `fix/<assunto>`, `docs/<assunto>` |

Na dúvida, o agente pergunta antes de criar.

### Quando a outra branch termina

1. Junte na `main` (você revisa, como no passo 6).
2. Traga para a `claude`: `git switch claude && git merge main`.
3. Apague a branch (próxima seção).

Se descobrir no meio do caminho que um trabalho na `claude` deveria ter sido
separado, crie a branch a partir dela (`git switch -c feat/<assunto>`) e
desfaça esses commits na `claude` com `git revert`.

## Remover uma branch

Uma branch é só um ponteiro para um commit: apagar não libera espaço nem
apaga commits que já estão na `main`. O motivo para apagar é **clareza**:
quando `git branch` mostra só o que está vivo, você sabe o que falta revisar.

### Quando vale apagar

| Situação | Apagar? |
|---|---|
| Já entrou na `main` | Sim. Não há nada nela que a `main` não tenha |
| Experimento abandonado | Sim, depois de conferir que não há nada a salvar (abaixo) |
| A `claude` depois de um merge | **Não.** Ela continua sendo a branch do dia a dia |
| Variante permanente (`pessoal`) ou trabalho longo em andamento | Não |
| Tem um PR aberto no GitHub | Não, até o PR ser aceito ou fechado |

### Do jeito certo

1. **Veja o que já entrou e o que não entrou** (funciona no container):

   ```bash
   git branch --merged main      # pode apagar com -d
   git branch --no-merged main   # tem commits que a main não tem
   ```

2. **Branch que já entrou:** apague com `-d`, que recusa se houver algo fora
   da `main`:

   ```bash
   git branch -d <nome>
   ```

3. **Branch que não entrou** (experimento abandonado): olhe o que vai embora
   e, só então, force com `-D`:

   ```bash
   git log --oneline main..<nome>   # os commits que você vai descartar
   git branch -D <nome>
   ```

   O git mostra o commit em que ela estava: `Deleted branch exp/x (was a1b2c3d)`.
   Anote esse código. Para desfazer: `git branch exp/x a1b2c3d`.

4. **Se ela também estiver no GitHub**, apague lá pelo terminal do **host**
   (o container não tem as chaves):

   ```bash
   git push origin --delete <nome>
   git fetch --prune   # limpa as referências a branches que sumiram do GitHub
   ```

**O `-d` recusou, mas o PR foi aceito no GitHub?** Isso acontece quando o
GitHub junta os commits num só ("squash"): o conteúdo está na `main`, mas os
commits originais não. Confira se juntar a branch traria algo novo e, se não
trouxer, use `-D` (precisa de git 2.38 ou mais novo; o da imagem é 2.39):

```bash
[ "$(git merge-tree --write-tree main <nome>)" = "$(git rev-parse 'main^{tree}')" ] \
  && echo "nada a perder: pode usar -D" || echo "tem conteúdo fora da main"
```

Não use `git diff main...<nome>` para isso: depois de um squash ele continua
mostrando as mudanças, mesmo que elas já estejam na `main` (testado).

**Apaguei sem anotar o código.** O `git reflog` lista por onde o `HEAD` passou
e costuma achar o último commit da branch. Isso tem prazo: commits que nenhuma
branch alcança somem na limpeza automática do git, depois de cerca de 30 dias
(padrão do git, configurável). Não conte com isso para guardar trabalho.

## Para levar ao seu projeto

Cole no `CLAUDE.md` ou no `AGENTS.md` do projeto (em inglês, porque é para a IA):

```markdown
- Commit on branch `claude` (create it from `main` if missing; `git merge main` first if `main` moved). Never commit on `main`, never push.
- Use a separate branch only for throwaway experiments, parallel sessions (`claude --worktree`), long work that must not block `claude`, or work that needs a test you can't run. Ask if unsure.
```

Neste repositório, a regra está no [`AGENTS.md`](../../AGENTS.md).
