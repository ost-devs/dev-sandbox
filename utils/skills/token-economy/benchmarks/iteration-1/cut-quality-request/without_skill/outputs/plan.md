# Plano: migrar 200 testes de integração para a nova API do cliente HTTP

Objetivo: o menor gasto possível de tokens, como você pediu. Não haverá rodada final dos testes. Haiku faz o trabalho. Não haverá revisão manual.

## A ideia central: quem converte é um script, não o modelo

Se o Haiku abrir e reescrever 200 arquivos um por um, o custo cresce com o tamanho de cada arquivo. Um script de conversão (sed ou um codemod pequeno) faz os 200 arquivos por quase nada. O modelo só entra nos casos que o script não cobre.

## Passos

1. **Mapear a mudança da API (1 vez, Haiku).** Ler o changelog ou o guia de migração do cliente HTTP e montar uma tabela "antigo → novo": nomes de métodos, parâmetros, como a resposta é lida, exceções e timeouts. Não ler os testes inteiros nesta etapa.
2. **Achar os padrões com grep, sem abrir arquivos.** Usar `grep -rn` nas chamadas antigas para contar quantas vezes cada padrão aparece. Assim dá para saber o que é mecânico (a maioria) e o que é exceção.
3. **Escrever o script de conversão (Haiku, 1 vez).** Um `sed -i` ou um codemod que aplica a tabela do passo 1 em todos os testes de uma vez. Rodar o script; isso não gasta tokens.
4. **Tratar as sobras (Haiku).** Rodar `grep` de novo procurando chamadas antigas que sobraram. Só os arquivos que aparecerem vão para o Haiku, e ele recebe só o trecho afetado, não o arquivo inteiro.
5. **Commit.** Um commit só, com a mensagem dizendo que a migração foi automática e que os testes não foram rodados.

Sem subagentes, sem conversa longa: cada passo começa e termina numa sessão curta.

## O que fica de fora (como você pediu)

- Rodada final da suíte de testes.
- Revisão dos arquivos convertidos.
- Modelo mais caro em qualquer etapa.

## Um aviso, e uma checagem quase de graça (opcional)

Sem conferir nada, um erro no script pode quebrar os 200 testes de uma vez, e você só descobre depois, quando consertar custa mais tokens do que conferir agora. Duas checagens não gastam tokens do modelo, porque é só você rodar um comando:

- **Checar só se compila ou se os testes são encontrados**, sem executar nada (por exemplo `pytest --collect-only -q`, `tsc --noEmit` ou `go vet ./...`, conforme a linguagem). Isso pega erro de sintaxe e import quebrado.
- **Rodar 2 ou 3 testes de amostra**, não a suíte inteira.

Se quiser pular essas também, tudo bem: o plano funciona sem elas. Só deixe o commit separado, assim `git revert` desfaz tudo num passo.
