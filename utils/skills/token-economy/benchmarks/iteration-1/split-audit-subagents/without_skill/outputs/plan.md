# Plano: conferir `docs/paridade.md` contra os crates em `mirrors/`

**Objetivo:** dar um veredito para cada uma das 480 afirmações ("a função X do crate Y se comporta como Z"), com evidência no código (arquivo:linha). A conversa principal não deve ler nem o código nem o documento inteiro: ela só coordena e junta os resultados.

**Números de partida:** 480 afirmações, 12 crates, ~60 mil linhas no total (em média ~40 afirmações e ~5 mil linhas por crate).

---

## Passo 0: preparar o terreno (conversa principal, sem subagente)

Isso é mecânico e barato. Faço com script, não lendo o documento no contexto.

1. **Numerar as afirmações.** Um script dá um ID estável para cada uma (`P001`…`P480`) e grava `audit/claims.tsv` com as colunas `id | crate | função | afirmação | linha em paridade.md`. Se o crate não estiver explícito numa linha, ela vai para `audit/sem-crate.tsv`, para eu triar à mão.
2. **Contar por crate.** `cut -f2 audit/claims.tsv | sort | uniq -c` mostra quantas afirmações cada crate tem.
3. **Medir cada crate.** `wc -l` em `mirrors/<crate>/src` dá o tamanho de cada um.
4. **Separar um arquivo por lote:** `audit/lotes/<lote>.tsv`, só com as afirmações daquele lote.

Para a conversa principal só voltam as duas tabelas pequenas (contagem e tamanho). Com elas eu fecho a divisão do passo 1.

## Passo 1: como dividir

**Regra:** cada lote é um crate. O subagente lê o código de um crate só e confere tudo o que o documento afirma sobre ele. Assim ninguém lê o mesmo código duas vezes, e quem confere conhece o contexto do crate inteiro (traits, macros, reexports).

Ajustes conforme os números do passo 0:

| Situação | O que fazer |
|---|---|
| Crate normal (até ~8 mil linhas e ~60 afirmações) | 1 lote |
| Crate grande (mais de ~8 mil linhas **ou** mais de ~60 afirmações) | Dividir por módulo (`src/foo/`, `src/bar/`), agrupando as afirmações pelo módulo da função |
| Crates pequenos (menos de ~1.500 linhas e menos de ~15 afirmações) | Juntar 2 ou 3 num lote só |
| Afirmação que envolve dois crates (ex.: "Y reexporta X de W") | Fica no lote do crate citado como Y, e o subagente pode abrir só o trecho necessário do outro |

Estimativa: **12 a 15 lotes**.

## Passo 2: quantos em paralelo

- **4 em paralelo** por rodada, cerca de 3 a 4 rodadas.
- Por que não 12 de uma vez: se as instruções tiverem um defeito (formato de saída errado, critério de veredito confuso), eu descubro na primeira rodada e corrijo antes de gastar tudo. Também fica mais fácil acompanhar.
- **Rodada piloto:** a primeira tem só 2 lotes pequenos. Confiro a saída e ajusto as instruções. Depois sigo com 4 por rodada.
- Esforço `lower` nos subagentes de conferência: a tarefa é bem delimitada e o próprio formato permite verificar o resultado.

## Passo 3: o que cada subagente recebe e lê

**Prompt (igual para todos, mudando só o lote):**

- O pedido do usuário, palavra por palavra.
- O caminho do seu lote: `audit/lotes/<lote>.tsv`.
- A pasta do código: `mirrors/<crate>/` (e quais módulos, se o lote for parcial).
- Os critérios de veredito (abaixo) e o formato de saída.
- Limites: só ler, nunca alterar `mirrors/` nem `docs/`. Não abrir outros crates, a não ser o trecho necessário numa afirmação entre crates.

**O que ele lê:**

1. O arquivo do lote (não o `paridade.md` inteiro).
2. Para cada função: localizar com `grep` (`fn nome`, `impl ... for`, `pub use`, macros) e ler a definição e o que ela chama diretamente. Ler o crate inteiro só se for pequeno.
3. Testes e doc-comments da função, quando existirem: muitas vezes mostram o comportamento esperado melhor que o corpo.

**Vereditos possíveis:**

| Veredito | Quando |
|---|---|
| `confirma` | O código faz o que a afirmação diz |
| `diverge` | O código faz outra coisa (dizer o quê) |
| `parcial` | Vale em parte (ex.: só com uma feature ligada, só em um caso) |
| `nao-encontrado` | A função não existe nesse crate/versão |
| `indeterminado` | Depende de algo que não dá para ver estaticamente (outro crate, runtime, `cfg`) |

## Passo 4: o que volta para a conversa principal

**No arquivo** `audit/resultados/<lote>.tsv` (detalhe completo, uma linha por afirmação):
`id | veredito | arquivo:linha | trecho curto (até 3 linhas) | explicação em uma frase`

**Na resposta do subagente** (o que entra no meu contexto), só isto:
- Contagem por veredito: `confirma 31, diverge 4, parcial 2, nao-encontrado 1, indeterminado 1`.
- A lista dos IDs que **não** são `confirma`, cada um com uma frase.
- Qualquer problema com as instruções (afirmação ambígua, crate com versão diferente da esperada).

Assim, 480 afirmações viram umas 12 respostas curtas no contexto principal. O detalhe fica em disco para quem quiser conferir.

## Passo 5: juntar e conferir

1. **Juntar por script:** concatenar `audit/resultados/*.tsv` em `audit/resultado.tsv` e conferir que os 480 IDs aparecem, cada um uma vez. Os que faltarem voltam para um lote de repescagem.
2. **Segunda opinião só nos casos difíceis:** os `diverge`, `parcial` e `indeterminado` (espero algo como 10 a 20% do total) vão para uma segunda rodada, agrupados por crate, com esforço `higher`. O subagente recebe a afirmação, o veredito anterior e a evidência, e confirma ou corrige. Os `confirma` não são refeitos, mas eu sorteio ~5% deles e confiro à mão para medir se o primeiro passo está confiável.
3. **Relatório final:** `audit/relatorio.md` com o resumo por crate (tabela) e a lista de divergências, cada uma com a linha do `paridade.md` e a evidência no código. Não edito o `paridade.md`: corrigir o documento é uma decisão do usuário, e fica como proposta.

## Resumo

| Item | Valor |
|---|---|
| Lotes | 12 a 15 (um por crate, ajustado pelo tamanho) |
| Paralelos | 2 no piloto, depois 4 por rodada |
| Cada subagente lê | o arquivo do seu lote + o código de um crate, guiado por grep |
| Volta para a conversa | contagem por veredito + lista curta das não confirmadas |
| Fica em disco | uma linha por afirmação, com arquivo:linha e trecho |
| Segunda rodada | só as não confirmadas, com esforço maior |
| Conferência final | script de cobertura dos 480 IDs + amostra de 5% dos `confirma` |
