# Dúvida: o `/etc/claude-code/CLAUDE.md` é carregado de verdade?

- **Data:** 2026-10
- **Ambiente:** container do dev-sandbox (Debian bookworm), Claude Code 2.1.310
- **Base:** evidência (sessão real de 2026-10-25, descrita abaixo)

## Sintoma
A imagem copia o `sandbox/AGENTS.md` para `/etc/claude-code/CLAUDE.md` e a
documentação diz que o Claude Code "carrega sozinho". Mas nada provava isso:
o agente podia só ter lido o arquivo porque alguém pediu.

## Causa
Não havia problema; faltava a prova. No Linux, `/etc/claude-code/CLAUDE.md` é o
local de instruções "managed" do Claude Code, carregado no início de toda sessão
aberta dentro do container.

## Prova
Numa sessão aberta no container, **antes** de qualquer pergunta sobre o assunto:

- O conteúdo do arquivo já estava no contexto do agente, rotulado como
  *organization-managed policy instructions*. O agente não abriu o arquivo com
  nenhuma ferramenta.
- O agente conhecia fatos que só existem nesse arquivo (sem `sudo`, `$HOME` em
  `/tmp/dev-home`, a regra de listar no fim da resposta os arquivos que rodam no
  host) e agiu conforme eles em tarefas que não tinham nada a ver com o ambiente.

Para repetir o teste: abra uma sessão nova, sem mencionar o arquivo, e pergunte
"o que você sabe sobre este ambiente?". Se ele descrever o container sem ler
nada, o arquivo foi carregado.

## Limites
- Carrega **no início da sessão**. Mudar o arquivo exige reconstruir a imagem e
  abrir um container novo; a sessão em andamento continua com o texto antigo.
- Não dá para desligar por projeto ([detalhes](../claude-code/memoria-e-instrucoes.md)).

## O que mudou no dev-sandbox
- Esta prova, apontada nos lugares onde a documentação afirma que carrega sozinho.
- `sandbox/AGENTS.md` ficou mais claro, porque o agente estava sem saber três
  coisas: `~/.claude`, `~/.gemini` e `~/.codex` são as pastas reais do host
  (montadas direto), enquanto o resto de `$HOME` é uma pasta só da sandbox; o
  diretório temporário do Claude Code persiste de propósito e é compartilhado
  entre sessões; e, por isso, não vale copiar arquivos dele para o projeto "para
  não perder" (isso suja o repositório).
