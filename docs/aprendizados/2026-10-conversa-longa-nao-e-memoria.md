# Conversa longa parece memória, mas não é

- **Data:** 2026-10
- **Ambiente:** Claude Code 2.1.310 (Sonnet 5.5 e Opus 5.5) neste repositório
- **Base:** evidência (uma sessão de dois dias neste repositório; a solução
  testada em sessões novas, [resultado](../claude-code/consultor-do-projeto.md#funcionou))
  e documentação
  ([compactação](../claude-code/por-baixo-dos-panos/compactacao.md),
  [contexto a cada pedido](../claude-code/por-baixo-dos-panos/a-cada-mensagem-o-contexto-vai-junto.md))

## Sintoma
Depois de horas, a conversa "sabe tudo" do projeto: responde com precisão, sem
reler nada. Começar outra parece um retrocesso, então a gente continua na
mesma para tudo, inclusive para assuntos sem relação. A conversa enche, fica
cara, e o resumo automático perde detalhes.

## Causa
O conhecimento estava **só no contexto** da conversa: arquivos lidos,
decisões, correções. O contexto vai inteiro a cada pedido e vira resumo quando
enche. Uma conversa nova não tem acesso a nada disso. Não é memória, é estado
temporário.

## Solução
Tirar o conhecimento da conversa e pôr em arquivos que o Claude lê sozinho,
cada um no lugar que carrega na hora certa: instruções, rules por pasta, uma
skill com o mapa do projeto, um agente que pesquisa fora do contexto principal,
e a memória automática para preferências pessoais. Antes de fechar uma
conversa longa, `/consolidar` faz a passagem. Guia completo:
[um consultor do projeto que não depende da conversa](../claude-code/consultor-do-projeto.md).

## O que mudou no dev-sandbox
`.claude/` com rules, as skills `dev-sandbox` e `consolidar`, o agente
`claude-code-pesquisador` com memória no git, e o guia acima.
