# Plano: revisar docs/claude-code/ contra a documentação oficial

## Objetivo (o que não muda)

Cada afirmação das 38 páginas de `docs/claude-code/` conferida contra a cópia oficial em `mirrors/claude-code-docs`, com evidência: para cada afirmação, a página oficial e o trecho que a confirma ou contradiz. O resultado final é uma lista de divergências (errado, desatualizado, sem fonte) com a correção sugerida, por página.

## Antes de começar: duas partes do pedido que eu proponho mudar

Você pediu duas coisas "por garantia". Fiz a conta e as duas custam muito sem melhorar o resultado. A decisão é sua; abaixo, o que cada caminho custa e o que deixa de dar.

### 1. "Cada subagente lê a documentação oficial inteira"

- A cópia oficial tem uns 10 MB (~120 páginas), cerca de 2,5 milhões de tokens. **Não cabe no contexto de um subagente**: ele não consegue ler tudo de verdade, só começar, encher o contexto e perder o começo. Na prática isso deixa a verificação *pior*, não mais segura.
- Custo, se coubesse: 38 páginas × 3 rodadas × ~2,5 M tokens ≈ 285 milhões de tokens.
- **Proposta:** montar uma vez um índice da documentação oficial (página → assuntos, títulos, configurações, flags que ela cobre) e salvar em arquivo. Cada subagente recebe a página nossa + a lista das páginas oficiais relevantes e lê essas páginas **inteiras** (não trechos). Se uma afirmação não tiver página oficial no índice, o subagente busca no mirror (grep) antes de marcar "sem fonte".
- O que se perde: nada do que a verificação precisa. O risco é o índice apontar a página errada; o grep de reserva cobre isso.

### 2. "Rodar cada verificação 3 vezes com subagentes diferentes"

- Triplica o custo inteiro. Vale se as três rodadas discordarem com frequência; se concordarem quase sempre, a segunda e a terceira não acham nada.
- **Proposta:** medir antes de decidir (passo 2 abaixo). Rodo as 3 verificações independentes em um piloto de 3 páginas e comparo:
  - Se as rodadas concordam (mesmas divergências encontradas), passo para **1 rodada por página + segunda verificação só nas afirmações marcadas como incertas ou divergentes**. Toda divergência que vira correção é conferida duas vezes; o que foi confirmado com trecho citado não precisa.
  - Se discordam bastante, mantenho as 3 rodadas, como você pediu.
- Eu te mostro o resultado do piloto e o custo medido antes de escolher. Não corto nada sem você saber.

## Passos

1. **Índice da documentação oficial (uma vez só).** Um subagente lê o mirror por partes e escreve `review/index.md`: para cada página oficial, caminho, título e assuntos cobertos. Também listo as 38 páginas nossas com as páginas oficiais relevantes para cada uma (`review/mapa.md`). Todos os subagentes depois reusam esses arquivos, em vez de cada um redescobrir onde está cada coisa.

2. **Piloto (3 páginas, 3 rodadas independentes).** Escolho 3 páginas de tamanhos diferentes (uma curta, uma média, uma longa). Cada rodada escreve `review/piloto/<pagina>-rodada<N>.md` no formato abaixo. Meço: tokens por página, quanto as rodadas concordam, quantos erros reais a 2ª e a 3ª rodada acharam que a 1ª não achou. **Paro e te mostro** os números e a proposta de como seguir.

3. **Rodada principal.** Com o formato e o tamanho definidos pelo piloto:
   - Agrupo as páginas por assunto (páginas que usam as mesmas páginas oficiais vão juntas, para não ler a mesma página oficial várias vezes). Tamanho do grupo definido pelo custo medido no piloto.
   - Cada subagente recebe: instruções curtas (um arquivo compartilhado `review/instrucoes.md`, escrito uma vez), as páginas do grupo, a lista de páginas oficiais a ler.
   - Cada subagente escreve o resultado de **cada página assim que termina** em `review/resultados/<pagina>.md`. Se bater limite de uso ou travar, perde só a página em andamento; retomo pelas que faltam.
   - Poucos subagentes em paralelo de cada vez (ex.: 3 ou 4), porque em paralelo eles batem no limite de uso juntos.

4. **Segunda verificação (conforme decidido no passo 2).** Outro subagente, sem ver a resposta do primeiro, confere as afirmações marcadas como divergentes ou incertas. Se os dois discordarem, eu mesmo leio o trecho oficial e decido.

5. **Consolidação.** Junto tudo em `review/relatorio.md`: por página, as divergências com trecho oficial, caminho no mirror e correção sugerida. Na conversa, só o resumo (quantas páginas, quantas divergências, as mais graves). Não edito `docs/claude-code/` sem você aprovar as correções.

## Formato do resultado por página

```
## <página>
| Afirmação (linha) | Status | Página oficial | Trecho oficial | Correção sugerida |
```

Status: `confirmado`, `divergente`, `desatualizado`, `sem fonte`, `incerto`.

## Custo estimado

| Caminho | Ordem de grandeza |
|---|---|
| Como pedido (3 rodadas, docs inteira por agente) | ~285 M tokens, e não funciona (não cabe no contexto) |
| 3 rodadas, só páginas oficiais relevantes | ~3× o caminho abaixo |
| 1 rodada + 2ª verificação nas divergências/incertezas | o menor; número real sai do piloto |

## O que preciso de você

1. Ok para trocar "ler a documentação inteira" por índice + páginas relevantes lidas inteiras?
2. Ok para decidir o número de rodadas depois do piloto, com os números na mão?
