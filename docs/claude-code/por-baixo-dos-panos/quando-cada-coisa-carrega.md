# Quando cada coisa entra no contexto

Uma dúvida comum: "o Claude relê meu `CLAUDE.md` a cada mensagem?". **Não.**
O arquivo é lido **uma vez, no início da sessão**, e fica guardado.
(Isso não quer dizer que ele deixa de ir junto a cada pedido: veja
[a cada mensagem o contexto vai junto](./a-cada-mensagem-o-contexto-vai-junto.md).)

> "Your project-root and user-level CLAUDE.md files are read once at session
> start and held in memory."
> (página de [prompt caching](https://code.claude.com/docs/en/prompt-caching))

## Tabela: o que entra, e quando

| O quê | Quando entra | Observação |
|---|---|---|
| Instruções do sistema e ferramentas | Início da sessão | Parte do próprio Claude Code |
| `CLAUDE.md` da máquina (*managed*), do usuário e do projeto, e `CLAUDE.local.md` | **Início da sessão** | Os arquivos da pasta onde você abriu o Claude **e de todas as pastas acima dela** |
| `CLAUDE.md` de **subpastas** | Quando o Claude lê, grava ou edita um arquivo naquela subpasta | Não entram no início |
| Rules em `.claude/rules/` sem `paths:` | Início da sessão | |
| Rules com `paths:` | Quando o Claude mexe num arquivo que combina com o padrão | |
| `AGENTS.md` | Início da sessão, **no lugar** do `CLAUDE.md` | Só se não houver nenhum `CLAUDE.md` na pasta ou acima; senão ele é ignorado |
| Memória automática (`MEMORY.md`) | Início da sessão | Só as primeiras 200 linhas ou 25 KB. Os outros arquivos de memória são lidos sob demanda |
| Skills | **Descrição** no início; o **texto completo** só quando a skill é usada | Com `disable-model-invocation: true`, nem a descrição entra até você chamar |
| Ferramentas de MCP | Só os nomes no início; o resto sob demanda | |

## Em que ordem aparecem

Os arquivos de instruções são **somados**, não substituídos. Eles entram do
mais amplo para o mais específico: máquina, depois usuário, depois projeto, e
dentro da árvore de pastas, da raiz até a pasta onde você abriu o Claude.
O que está mais perto de você é lido por último.

Se dois arquivos se contradizem, a documentação avisa que o Claude "may pick
one arbitrarily" (pode escolher um qualquer). Evite instruções conflitantes.

## Editar o `CLAUDE.md` com a sessão aberta

A edição **não** vale na hora. O Claude continua com a versão que carregou
no início. A nova entra depois de `/clear`, `/compact` ou de reabrir o Claude.

## Dica: comentários

Comentários HTML em bloco (`<!-- nota para mim -->`) são removidos antes de
o texto entrar no contexto. Servem para deixar notas para humanos sem gastar
tokens.

## Não é uma trava

> "Claude treats them as context, not enforced configuration."

Instruções são lidas e seguidas na maior parte das vezes, sem garantia. Para
algo que **precisa** acontecer (bloquear um comando, por exemplo), use um hook.

## No dev-sandbox

O `/etc/claude-code/CLAUDE.md` da imagem é o arquivo *managed* do Linux. Ele
entra no início de toda sessão dentro do container, e o desenvolvedor não
consegue excluí-lo com `claudeMdExcludes`. A
[prova de que carrega sozinho](../../aprendizados/2026-10-etc-claude-md-carrega-sozinho.md)
mostra isso numa sessão real.

Para conferir o que carregou na sua sessão: `/context` (lista *Memory files*)
ou `/memory`.

## Fontes

Conferido em outubro/2026 (Claude Code 2.1.310):
[memória](https://code.claude.com/docs/en/memory),
[janela de contexto](https://code.claude.com/docs/en/context-window),
[prompt caching](https://code.claude.com/docs/en/prompt-caching),
[como o Claude Code funciona](https://code.claude.com/docs/en/how-claude-code-works).
Veja também [memória e instruções](../memoria-e-instrucoes.md).
