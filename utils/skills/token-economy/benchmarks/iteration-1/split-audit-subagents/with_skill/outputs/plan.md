# Plano: conferir as 480 afirmações de `docs/paridade.md` contra `mirrors/`

Objetivo fixo: cada uma das 480 afirmações recebe um veredito apoiado em evidência no código (arquivo:linha). O plano economiza tokens sem cortar isso: nada de amostragem no lugar da conferência, nada de "parece certo" sem abrir o código.

## Resumo

| Etapa | Quem faz | O que volta para a conversa principal |
|---|---|---|
| 0. Preparar | script na conversa principal | contagem de afirmações por crate (uma tabela) |
| 1. Piloto | 1 subagente, 1 crate | custo medido + vereditos para eu conferir por amostra |
| 2. Rodada | 3 subagentes em paralelo, em ondas | uma linha por subagente |
| 3. Consolidar | script + conversa principal | só as afirmações que não foram confirmadas |

## Etapa 0 — preparar uma vez, compartilhar com todos

Feito antes de qualquer subagente, para nenhum deles redescobrir a mesma coisa.

1. **Extrair as afirmações para um arquivo estruturado.** Um script lê `docs/paridade.md` e gera `audit/claims.tsv` com `id | crate | função | afirmação | linha no paridade.md`. Se o formato do documento for irregular demais para script, um subagente faz essa extração e devolve só o caminho do arquivo e a contagem. A conversa principal não lê as 480 afirmações.
2. **Índice de símbolos por crate.** Um script com `grep -n` (`pub fn`, `fn`, `impl`, `trait`, `macro_rules!`) gera `audit/index/<crate>.tsv` com `símbolo | arquivo:linha`. Assim cada subagente vai direto à função citada em vez de varrer o crate.
3. **Briefing único em `audit/brief.md`** (curto, cerca de 30 linhas): o que é um veredito, o formato de saída, as regras de evidência, o que fazer quando a função não existe ou tem vários `impl`. O prompt de cada subagente aponta para esse arquivo e diz qual é a sua fatia; não repete as regras.
4. **Fatiar.** Saída: `audit/slices.tsv` (fatia → crate/módulo → ids). Regra inicial, que o piloto ajusta:
   - uma fatia = um crate (as afirmações sobre o crate Y só precisam do código do Y);
   - crate com muito mais afirmações ou linhas que a média (60 mil / 12 ≈ 5 mil linhas, 480 / 12 = 40 afirmações) é dividido por módulo;
   - crates pequenos (poucas afirmações) são juntados numa só fatia.

   Resultado esperado: algo entre 10 e 14 fatias.

A conversa principal vê apenas a tabela de contagem por fatia.

## O que cada subagente lê e escreve

- **Lê:** `audit/brief.md`, suas linhas de `audit/claims.tsv`, o índice do seu crate e, no código, só a função citada mais o que for preciso para decidir (funções chamadas, tipos, testes do crate que mostram o comportamento). Não lê o crate inteiro, não lê o `paridade.md` inteiro, não lê outros crates (a não ser que a afirmação dependa de uma reexportação; nesse caso segue a reexportação e anota).
- **Escreve, uma linha por afirmação, logo depois de decidir** (não no fim), em `audit/results/<fatia>.tsv`:
  `id | veredito | evidência (arquivo:linha) | nota de uma linha`
  Vereditos: `confirma`, `contradiz`, `parcial`, `não encontrado`.
  Se cair por limite de uso ou falha, perde só a afirmação em andamento; ao retomar, pula os ids já presentes no arquivo.
- **Devolve para a conversa principal uma linha só:** `fatia X: 41 conferidas — 33 confirma, 4 contradiz, 3 parcial, 1 não encontrado → audit/results/X.tsv`.
- Tipo de subagente: `general-purpose` (precisa ler o código a fundo e escrever arquivo). O `Explore` lê trechos para localizar código, não para auditar comportamento.

## Etapa 1 — piloto

Roda **uma** fatia de tamanho médio, sozinha, antes de lançar o resto. Mede:

- tokens e tempo da fatia;
- se o contexto do subagente ficou folgado ou apertado;
- qualidade: eu confiro à mão cerca de 5 vereditos (incluindo todos os `contradiz`) contra o código.

Com isso decido o tamanho das fatias: se o subagente terminou com muita folga, juntar fatias (menos custo fixo de briefing e índice); se apertou o contexto ou começou a errar, dividir. Se o briefing gerou vereditos mal formatados ou ambíguos, corrijo `brief.md` agora, uma vez, antes da rodada.

## Etapa 2 — rodada em ondas

- **3 subagentes em paralelo** por onda, não 12 de uma vez. Subagentes paralelos batem no limite de uso juntos; com 3, uma interrupção afeta pouca coisa e o que já foi escrito em `audit/results/` fica salvo. Se o piloto mostrar custo baixo por fatia, subo para 4.
- Entre ondas, a conversa principal só lê as linhas de retorno; não abre os arquivos de resultado.
- Fatia que falhar é relançada com a instrução de pular os ids já presentes.

## Etapa 3 — consolidar

1. Um script junta `audit/results/*.tsv` em `audit/relatorio.tsv` e confere: os 480 ids aparecem exatamente uma vez, toda linha tem evidência no formato `arquivo:linha`.
2. A conversa principal lê **só** as linhas que não são `confirma` (estimativa: algumas dezenas) e as confere ou agrupa por padrão.
3. Entrega: um resumo curto (contagens por veredito e por crate) mais a lista das afirmações a corrigir em `docs/paridade.md`, cada uma com a evidência.

## Checagem extra: decidir pelo rendimento

Uma segunda passada nos `confirma` (outro subagente reconfere uma amostra) custa caro. Proposta: fazer essa reconferência **só no piloto**, numa amostra de uns 10 `confirma`. Se não achar erro, não repito nas outras fatias e aviso você. Se achar, mantenho a amostra em todas as fatias.

## Decisões que são suas (trocam resultado por tokens)

| Escolha | Opção mais barata | O que ela abre mão |
|---|---|---|
| Modelo dos subagentes | Sonnet: custo bem menor por fatia | mais risco de veredito errado em comportamento sutil (genéricos, traits, macros). Sugestão: Sonnet no piloto e comparar com a minha conferência manual; se errar, Opus |
| Reconferir `confirma` | só no piloto (proposta acima) | um erro do tipo "confirmou o que não devia" fora do piloto pode passar |
| Paralelismo | 3 por onda | demora mais no relógio do que 6 ou 12, mas o limite de uso pega menos coisa no meio |

## Estimativa grosseira (o piloto substitui por números medidos)

- Por fatia: briefing + índice + leitura das funções citadas (algumas centenas a poucos milhares de linhas, não as ~5 mil do crate) + 40 linhas de saída.
- Conversa principal: ~1 tabela de contagem, ~12 linhas de retorno, as linhas não confirmadas. Nenhuma leitura de código ou das 480 afirmações.
