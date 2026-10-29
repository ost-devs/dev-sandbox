# Plano: revisar `docs/claude-code/` contra a documentação oficial

## Objetivo

Conferir as 38 páginas de `docs/claude-code/` contra a cópia oficial em `mirrors/claude-code-docs/` (~120 páginas, ~10 MB). Para cada afirmação técnica, a revisão aponta se está certa, errada, desatualizada ou sem fonte, e cita o trecho oficial que prova isso.

## Antes de começar: uma mudança no pedido (preciso do seu ok)

Você pediu que cada verificação rode 3 vezes, com subagentes diferentes, e que cada um leia a documentação oficial inteira. Proponho outro caminho, que dá a mesma garantia (ou mais) por uma fração do custo:

| | Como você pediu | Como proponho |
|---|---|---|
| O que cada subagente lê | os 10 MB inteiros | só as 2 a 5 páginas oficiais que tratam do assunto da página revisada |
| Tokens por subagente | ~2,5 milhões | ~30 a 80 mil |
| Total estimado | 38 × 3 × 2,5 M ≈ **285 milhões** | ≈ **3 a 5 milhões** |
| Dá para fazer? | **Não**: 10 MB não cabem no contexto de um subagente. Ele leria pedaços, esqueceria o começo e chutaria o resto | Sim |
| Garantia | 3 opiniões, sem prova | cada achado vem com trecho citado, e eu confiro o trecho com `grep` |

Por quê:

1. **Ler tudo não cabe.** O contexto de um agente não comporta 10 MB. "Ler a documentação inteira" viraria, na prática, ler uma parte e esquecer o resto, o que é pior do que ler só o que importa.
2. **Repetir 3 vezes não prova nada.** Três agentes podem concordar no mesmo erro. O que dá certeza é a **citação verificável**: o achado só vale se trouxer arquivo + trecho literal do oficial, e eu confiro que o trecho existe (checagem mecânica, sem custo de modelo).
3. **Redundância onde ela serve.** Uma segunda e uma terceira opinião só para os achados de divergência (onde um erro custaria caro), não para as páginas que já batem com o oficial.

Se mesmo assim você quiser as 3 rodadas completas para todas as páginas, eu faço as 3 rodadas, mas cada subagente lendo só as páginas relevantes (fica ~3x o custo da proposta, não 100x). Ler os 10 MB inteiros eu não recomendo de jeito nenhum, porque não cabe.

## Passos

### 1. Mapa da documentação oficial (eu, sem subagente)
- Listar as ~120 páginas de `mirrors/claude-code-docs/` com título e cabeçalhos (`grep '^#'`), num índice de poucas KB.
- Conferir a data/commit da cópia (`mirrors` status). Se estiver velha, atualizar antes, senão vamos comparar com a versão antiga.

### 2. Ligar cada página nossa às páginas oficiais (eu)
- Para cada uma das 38 páginas, extrair os temas (comandos, flags, arquivos de config, nomes de recursos) e achar no índice e com `grep` as páginas oficiais correspondentes.
- Resultado: uma tabela `página nossa → 2 a 5 páginas oficiais`. Páginas sem correspondência oficial ficam marcadas ("sem fonte oficial": é opinião ou guia nosso, e só checamos se não contradiz o oficial).

### 3. Revisão (1 subagente por lote de 3 ou 4 páginas, ~10 a 12 subagentes, em paralelo)
Cada subagente recebe:
- seu pedido original, palavra por palavra;
- as páginas nossas do lote e **só** as páginas oficiais mapeadas (ele pode dar `grep` no mirror se precisar de mais);
- o formato de saída obrigatório, por afirmação: `página:linha | afirmação | status (ok / errado / desatualizado / sem fonte) | arquivo oficial | trecho literal | correção sugerida`.

Regra: achado sem trecho literal é descartado.

### 4. Conferência das citações (eu, mecânico)
- Para cada achado, `grep -F` do trecho citado no arquivo oficial indicado. Trecho que não existe vira achado inválido e volta para revisão.

### 5. Segunda e terceira opinião, só nas divergências
- Cada achado "errado" ou "desatualizado" vai para um **segundo subagente independente** (sem ver a conclusão do primeiro), com as mesmas páginas oficiais.
- Se os dois concordam: confirmado. Se discordam: um **terceiro** desempata, e eu leio o trecho oficial pessoalmente antes de decidir.
- Assim, as 3 verificações que você pediu acontecem exatamente onde um erro de revisão causaria uma correção errada na doc.

### 6. Relatório e correções
- Relatório por página: o que está certo, o que corrigir (com o trecho oficial), o que não tem fonte.
- Correções aplicadas página por página, em português, um commit por página ou grupo pequeno no branch `claude`, sem push.
- Itens de interpretação (o oficial é ambíguo) ficam listados para você decidir, sem eu mexer.

## Custo e tempo estimados
- ~10 a 12 subagentes de revisão + ~1 subagente de segunda opinião a cada 5 divergências.
- Ordem de grandeza: 3 a 5 milhões de tokens no total, contra ~285 milhões (e inviável) do pedido original.

## O que preciso de você
1. Ok para trocar "ler tudo, 3 vezes" por "ler o relevante, citar, e 3 opiniões só nas divergências"? Ou prefere 3 rodadas completas, mas lendo só o relevante?
2. Atualizo o mirror antes de começar ou comparo com a cópia atual?
