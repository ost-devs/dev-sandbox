# Um bom comportamento do Claude nem sempre vem das memórias

- **Data:** 2026-11
- **Ambiente:** Claude Code 2.1.316 (Opus 5.5) neste repositório
- **Base:** evidência (o registro de uma sessão de 2026-11-04,
  `~/.claude/projects/-dev-sandbox/b81c4361-….jsonl`, lido em outra sessão do
  mesmo dia) e análise (o peso de cada fonte não dá para medir de dentro)

## Sintoma
Numa sessão, o Claude propôs pôr um passo que precisa rodar em todo container
novo num hook `SessionStart`, e não no `CLAUDE.md`: "se ficar como instrução,
o agente pode esquecer". Na mesma resposta, escreveu as linhas do `CLAUDE.md`
em inglês, "como pede a regra". Pareceu efeito das memórias e dos guias do
repositório, que defendem as duas coisas.

## Causa
O registro da sessão mostra tudo o que entrou no contexto antes da resposta.
Separando as duas partes:

| Comportamento | Estava no contexto? | De onde veio, provavelmente |
|---|---|---|
| Linhas em inglês | Sim: a memória "AI files in English", no índice | Da memória. A resposta cita a regra |
| Hook em vez de instrução | Não: nenhuma memória diz isso, e os arquivos do repositório que dizem ([instrução ou mecanismo](../claude-code/instrucao-ou-mecanismo.md), o mapa do projeto) não foram lidos | Do próprio modelo: a documentação oficial já diz que hook é determinístico e instrução é pedido |

O guia do repositório sobre instrução e mecanismo descreve o que o modelo já
faz. Naquela sessão ele foi efeito, não causa.

O registro mostra o que estava disponível, não o que causou a resposta. Para
medir de verdade, faça a mesma pergunta num projeto que não tem a memória e
compare.

## Solução
Antes de creditar um comportamento a uma memória, ou de escrever uma instrução
nova:

- **Regra explícita e específica** (idioma, formato, um caminho do projeto): a
  memória ou instrução faz diferença. Mantenha.
- **Princípio geral de engenharia** (hook para o que precisa acontecer sempre,
  testar antes de afirmar): o modelo provavelmente já sabe. Uma instrução só
  repete, e ocupa contexto em toda sessão.
- **Fato de versão** (limites, o que volta depois da compactação): o modelo
  não sabe com certeza. Aí a doc conferida no repositório vale.

Para descobrir o que entrou numa sessão, os registros ficam em
`~/.claude/projects/<pasta do projeto>/<id>.jsonl`. Um `grep` pelo texto da
resposta acha a sessão.

## O que mudou no dev-sandbox
Nada no código. O critério já está no
[teste da linha](../claude-code/instrucao-ou-mecanismo.md): a linha só fica se
o agente não descobriria a coisa sozinho.
