# Ferramentas para qualquer projeto

Skills e agentes do Claude Code que não dependem do dev-sandbox. Funcionam
dentro ou fora do container, em qualquer repositório.

| Ferramenta | Tipo | Para quê | Como usar |
|---|---|---|---|
| [`montar-consultor`](./skills/montar-consultor/SKILL.md) | Skill | Montar os arquivos que fazem uma conversa nova já saber o projeto | [Guia](../docs/claude-code/montar-consultor.md) |
| [`estudar`](./skills/estudar/SKILL.md) | Skill | Transformar artigos da web (um, uma lista ou uma cadeia) em artigos do projeto, conferindo números e versões na fonte oficial. Precisa da `mirrors` | [Guia](../docs/claude-code/base-de-conhecimento.md#escrever-a-partir-de-artigos-estudar) |
| [`mirrors`](./skills/mirrors/SKILL.md) | Skill | Guardar cópias somente leitura de repositórios de fora (docs, código de referência) | [Guia](../docs/claude-code/mirrors.md) |

## Instalar

Uma skill instalada na sua pasta pessoal do Claude vale em todos os seus
projetos. Rode **no host**, trocando `~/dev-sandbox` pelo lugar onde você
clonou este repositório e `<nome>` pela ferramenta:

```bash
mkdir -p ~/.claude/skills
cp -r ~/dev-sandbox/utils/skills/<nome> ~/.claude/skills/
```

Para atualizar depois de um `git pull`, apague e copie de novo:

```bash
rm -rf ~/.claude/skills/<nome>
cp -r ~/dev-sandbox/utils/skills/<nome> ~/.claude/skills/
```

A `mirrors` tem um passo a mais para capturar artigos da web: depois de
copiar (e de cada atualização), rode
`npm ci --prefix ~/.claude/skills/mirrors --ignore-scripts`
([por quê](../docs/claude-code/mirrors-de-artigos.md#1-instalar-o-defuddle-uma-vez-só)).

Conferir: numa sessão nova, digite `/` e o começo do nome. A skill deve
aparecer na lista.
