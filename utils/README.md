# Ferramentas para qualquer projeto

Skills e agentes do Claude Code que não dependem do dev-sandbox. Funcionam
dentro ou fora do container, em qualquer repositório.

| Ferramenta | Tipo | Para quê | Como usar |
|---|---|---|---|
| [`montar-consultor`](./skills/montar-consultor/SKILL.md) | Skill | Montar os arquivos que fazem uma conversa nova já saber o projeto | [Guia](../docs/claude-code/montar-consultor.md) |
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

A pasta de cada skill tem só o que a IA usa; os guias para você ficam em
[`docs/claude-code/`](../docs/claude-code/README.md).

Conferir: numa sessão nova, digite `/` e o começo do nome. A skill deve
aparecer na lista.
