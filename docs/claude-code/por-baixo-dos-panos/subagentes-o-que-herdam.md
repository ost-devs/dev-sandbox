# Subagentes: o que recebem da sessão principal

Um **subagente** é um segundo Claude, chamado pelo principal para fazer um
trabalho separado (pesquisar, rodar testes, revisar). Ele tem a **própria
janela de contexto**, e só o resultado final volta para a conversa principal.

Dúvida comum: "o subagente recebe o `CLAUDE.md` do projeto ou o que a sessão
principal determinou?". A resposta é: **o `CLAUDE.md`, sim; o que foi dito na
conversa, não.** Os detalhes:

## O que o subagente recebe

> "Each subagent starts with a fresh, isolated context window. It doesn't see
> your conversation history, the skills you've already invoked, or the files
> Claude has already read. Claude composes a delegation message that summarizes
> the task, and the subagent works from there."

| Recebe | Detalhe |
|---|---|
| Prompt de sistema **próprio** | O texto do arquivo do agente (`.claude/agents/*.md`) mais dados do ambiente, como a pasta de trabalho. **Não** o prompt de sistema do Claude Code |
| **Mensagem de tarefa** | O texto que o Claude principal escreve ao delegar. É a única ponte entre as conversas |
| **`CLAUDE.md`** | Todos os níveis da hierarquia que a conversa principal carrega: `~/.claude/CLAUDE.md`, do projeto, `CLAUDE.local.md`, rules, arquivos *managed* e `AGENTS.md` quando usados como instruções |
| Instantâneo do git | Branch, status e commits recentes |
| Skills listadas no campo `skills` do agente | Texto completo, só se listadas |

## O que não recebe

- o histórico da conversa e o que o principal já leu;
- instruções que você deu **só falando** na conversa;
- a memória automática da sessão principal (o subagente pode ter a sua, pelo campo `memory`);
- o estilo de saída (*output style*);
- as skills já usadas.

## Exceções

| Caso | Diferença |
|---|---|
| Agentes embutidos **Explore** e **Plan** | **Não** recebem `CLAUDE.md` nem instantâneo do git |
| Agente com `omitClaudeMd` | Recebe só os arquivos *managed*, ou nenhum |
| **Fork** | Herda a conversa inteira, o prompt de sistema e as ferramentas do principal |

## O risco de conflito, na prática

O que você teme existe, em parte. O subagente trabalha com:
(1) o `CLAUDE.md` do disco e (2) a mensagem de tarefa que o principal escreveu.
Se você combinou uma regra **só na conversa**, o subagente não a conhece, a
menos que o principal a repita na mensagem de tarefa.

E a documentação alerta: se duas instruções se contradizem, o Claude "may pick
one arbitrarily". Para evitar divergência:

1. regra que vale para todos: no `CLAUDE.md` (ou rule) do projeto;
2. regra de um agente específico: no arquivo do agente;
3. regra desta tarefa: na mensagem de tarefa (peça ao principal, ou escreva
   "ao delegar, inclua X na tarefa").

## No dev-sandbox

O `/etc/claude-code/CLAUDE.md` é um arquivo *managed* e faz parte da
hierarquia, então chega aos subagentes comuns, e até aos que usam
`omitClaudeMd`. **Mas não chega a Explore e Plan**, que ignoram `CLAUDE.md`.
Esses dois não saberiam, por exemplo, que o container não tem `sudo`.

## Mais detalhes

- **Contexto próprio:** o trabalho pesado fica fora da sua conversa; só volta o resumo.
- **Modelo:** vem do parâmetro da chamada, depois do campo `model` do agente, depois de `CLAUDE_CODE_SUBAGENT_MODEL`, e por fim o modelo da conversa principal. A janela de contexto do subagente é a do modelo dele.
- **Permissões:** se o agente não define, herda o modo de permissão da conversa principal.
- **Aninhamento:** por padrão, um subagente pode chamar outros, até 3 camadas abaixo da principal (`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`).
- **Custo:** cada subagente faz os próprios pedidos à API, somados ao uso da conversa principal. Ele não reaproveita o cache da principal (o prefixo é diferente), exceto o fork.

## Fontes

Conferido em outubro/2026 (Claude Code 2.1.310):
[subagentes](https://code.claude.com/docs/en/sub-agents) (seção *What loads at startup*),
[subagentes no SDK](https://code.claude.com/docs/en/agent-sdk/subagents),
[prompt caching](https://code.claude.com/docs/en/prompt-caching),
[memória](https://code.claude.com/docs/en/memory).
