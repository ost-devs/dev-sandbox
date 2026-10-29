# Plano: migrar 200 testes de integração para a nova API do cliente HTTP

Objetivo: os 200 testes convertidos para a nova API, gastando o mínimo de tokens.

Resumo: dá para gastar bem menos do que "Haiku convertendo arquivo por arquivo" sem abrir mão de saber se a migração funcionou. O que mais pesa é o modelo **ler e reescrever 200 arquivos**, não rodar os testes. Por isso o plano troca a conversão manual por um script, e mantém uma rodada de testes que custa quase nada.

## Antes: o que você pediu e o que eu mudei

Você pediu três cortes. Dois deles quase não economizam e podem custar caro depois. A escolha é sua; abaixo, o custo de cada um.

| Seu pedido | Quanto economiza | O que você perde | Minha proposta |
|---|---|---|---|
| Pular a rodada final dos testes | Quase nada. Rodar a suíte é um comando; o gasto é ler a saída, e a saída vai para um arquivo. Só entram na conversa os nomes dos testes que falharam. | Você não fica sabendo se a migração quebrou algo. Descobre depois, numa sessão nova, que precisa reler os arquivos do zero (muito mais tokens). | Manter uma rodada, com saída em arquivo (passo 5). |
| Haiku em tudo | Bastante, na parte de converter. | Na parte de decidir o padrão de conversão, um erro do Haiku se repete nos 200 arquivos. | Haiku (ou nem modelo, um script) na conversão em massa; o modelo atual só no passo 1, que é curto. |
| Não conferir nada | Pouco, se a conferência for a rodada de testes. | Mesmo do primeiro item. | Nenhuma conferência manual arquivo por arquivo (concordo com você); só a rodada de testes. |

Se mesmo assim quiser pular os testes, é só apagar o passo 5. O resto do plano continua igual.

## Passos

### 1. Montar a regra de conversão (modelo atual, uma vez)
- Ler o changelog/guia de migração do cliente HTTP (só a parte das mudanças de API) e **2 ou 3 testes** representativos.
- Escrever em `migration-rules.md` a tabela "API antiga → API nova" (ex.: `client.get(url, params)` → `client.request("GET", url, query=params)`), com os casos especiais encontrados.
- Esse arquivo é lido uma vez por quem for converter; ninguém redescobre as regras.

### 2. Converter por script, não por modelo (onde der)
- A maior parte de uma migração de API é troca mecânica de chamadas. Um codemod (sed, script Python, ou a ferramenta de codemod da linguagem) converte os 200 arquivos sem o modelo ler nenhum deles.
- Custo em tokens: escrever o script (pequeno) + a lista dos arquivos que ele não conseguiu converter.
- O script grava em `migration-leftovers.txt` os trechos que não casaram com nenhuma regra.

### 3. Piloto: medir antes de escalar
- Rodar o script em **5 testes**, rodar só esses 5 testes.
- Se passarem: seguir para todos. Se falharem: ajustar `migration-rules.md` e o script, que é bem mais barato do que corrigir 200 arquivos depois.

### 4. Sobras com Haiku, em lotes
- Só os trechos de `migration-leftovers.txt` vão para subagentes Haiku, com `migration-rules.md` como única instrução.
- Lotes de uns 20 arquivos (ajustar pelo custo medido no primeiro lote). Cada subagente grava direto nos arquivos e anota em `migration-progress.txt` o que terminou: se bater o limite de uso, você perde só o lote em andamento, não a migração inteira.
- Rodar os lotes em sequência, não todos em paralelo: em paralelo eles batem no limite juntos.
- Resposta de cada subagente: uma linha ("lote 3: 18 convertidos, 2 pendentes: a.test, b.test").

### 5. Uma rodada dos testes, saída em arquivo
- Rodar a suíte inteira uma vez, saída em `test-run.log`.
- Para a conversa vai só a lista de testes que falharam (ex.: `grep FAIL test-run.log`), não o log.
- Falhas: corrigir só esses arquivos, rodar só esses testes de novo.

## O que fica de fora (de propósito)
- Revisão manual de cada arquivo: os testes já dizem se a conversão funcionou.
- Ler o projeto inteiro: só o guia de migração e os 2 ou 3 exemplos do passo 1.
- Relatórios longos dos subagentes: uma linha por lote.

## Se o limite da semana acabar no meio
`migration-progress.txt` diz onde parou. Na próxima sessão: ler esse arquivo e `migration-rules.md`, e continuar do próximo lote.
