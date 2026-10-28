# Memória compartilhada por link aparece e abre igual a uma nota comum

- **Data:** 2026-10
- **Ambiente:** Claude Code dentro do dev-sandbox, projeto `-dev-sandbox` (grupo `dev`)
- **Base:** evidência: teste feito em 28/10/2026 numa sessão normal, só com as ferramentas do
  próprio Claude (sem script). A parte sobre o gatilho espontâneo é análise (ver abaixo).

## Sintoma
Dúvida: uma memória compartilhada pela skill [`share-memories`](../../utils/skills/share-memories/SKILL.md)
é um link simbólico na pasta de memória do projeto. Será que o Claude a enxerga e a ativa como
enxerga uma nota criada ali mesmo, sem sair do projeto para procurar?

## O que foi observado

| Teste | Resultado |
|---|---|
| Linha da memória linkada no `MEMORY.md` do projeto | Aparece no contexto desde o início da sessão, igual às notas comuns (com a marca `(group dev)`) |
| `Read` em `feedback-ai-files-in-english.md` (link, grupo `todos`) | Abriu pelo caminho do projeto; frontmatter e corpo íntegros |
| `Read` em `honest-security-tradeoffs.md` (memória exclusiva de outro projeto) | "File does not exist": o projeto não enxerga o que não foi linkado nele |

## Causa
Para o Claude, o link é um arquivo comum: o `Read` o segue. O que a sessão carrega sozinha é o
índice `MEMORY.md`; o corpo só é lido quando o Claude abre o arquivo. Como o índice trata
memória linkada e memória local do mesmo jeito, a descrição (o gatilho "Use when...") fica
visível nos dois casos. Isso é dedução desse mecanismo, não algo que a documentação afirme.

## Solução
Nada a consertar. Compartilhar por link não perde nada em relação a criar a nota no projeto, e
o isolamento funciona: o projeto só vê o que foi linkado nele.

## O que não ficou provado
Só abrir a memória por ordem do usuário foi testado. Falta observar o gatilho disparando sozinho
numa tarefa real (por exemplo, validar um script à mão e o Claude lembrar de transformar o teste
em arquivo versionado). Quando isso acontecer, vale acrescentar aqui.

## O que mudou no dev-sandbox
Nada: só documentação. Complementa [o Write e o Edit se recusam a escrever num link](./2026-10-write-edit-recusam-symlink.md)
(escrita) com a leitura e a ativação.
