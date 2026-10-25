# Tarefa grande: dentro da conversa ou em partes independentes?

Exemplo clássico: traduzir um arquivo longo. Fazer isso **dentro da conversa**
costuma gastar muito mais do que parece. Este texto explica por quê, e qual
alternativa existe.

## O que acontece dentro da conversa

1. O Claude lê o arquivo. O conteúdo inteiro **entra no contexto** e fica lá
   até o fim da sessão.
2. Ele escreve a tradução em vários comandos (um trecho por vez).
3. **Cada comando é mais um pedido**, e cada pedido leva o contexto inteiro:
   o arquivo original, as traduções já escritas, tudo.

Isso não é invenção nem exagero. É o comportamento descrito na documentação:

> "Claude Code sends your full conversation with every request, and each time
> Claude uses tools it sends another request carrying that batch of tool results."

Com o cache de prompt, a releitura custa menos que o preço normal
([cache](./cache-de-prompt.md)), mas **continua crescendo** junto com o
contexto. Num exemplo ilustrativo de 10 trechos, o 10º pedido carrega o arquivo
original mais as 9 traduções anteriores.

> **Sobre números:** a documentação descreve o mecanismo, não dá uma conta
> pronta para este caso. O custo exato de uma tarefa específica só se sabe
> medindo (`/usage` mostra os tokens da sessão).

## A alternativa: partes independentes

Em vez de uma conversa que acumula, rode **várias chamadas curtas e
independentes**, cada uma com um pedaço do arquivo:

- O modo não interativo `claude -p` responde e encerra, sem abrir conversa.
- Combinado com `--no-session-persistence` (não salva a sessão) e
  `--tools ""` (sem ferramentas), cada chamada começa do zero e só recebe o
  trecho e as regras.
- Em princípio nada acumula: o contexto de cada chamada é só o trecho e as
  regras, então o 10º trecho tende a custar o mesmo que o 1º.

| | Dentro da conversa | Chamadas independentes (`claude -p`) |
|---|---|---|
| Contexto | Cresce a cada passo | Sempre pequeno |
| Pedidos | Vários, cada um com tudo | Um por trecho, só com o trecho |
| Controle de qualidade | Você olha o resultado final | Dá para checar cada trecho por script (por exemplo, contar linhas) |
| Bom para | Trabalho que precisa de ida e volta | Tarefas repetitivas, em lote, com formato fixo |
| Risco | Custo e lentidão crescentes | O trecho não conhece os vizinhos (um termo pode sair diferente em dois trechos) |

## Regra de bolso

- Precisa **conversar, decidir, explorar**? Fique na conversa.
- É a **mesma operação repetida** sobre pedaços independentes (traduzir,
  resumir, classificar, extrair)? Faça em partes independentes.
- Terminou uma tarefa e vai começar outra? `/clear`.

## Fontes

Conferido em outubro/2026 (Claude Code 2.1.310):
[custos](https://code.claude.com/docs/en/costs),
[prompt caching](https://code.claude.com/docs/en/prompt-caching),
[modo não interativo](https://code.claude.com/docs/en/headless).
