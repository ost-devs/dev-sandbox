# O agente contorna ferramenta que falta e não avisa

- **Data:** 2026-10

## Sintoma
Sem `rsync` na imagem, o agente escreveu um script Python para copiar
arquivos. O trabalho saiu, mas ninguém ficou sabendo que faltava `rsync`.
Na mesma auditoria, também faltavam `sqlite3`, `lsof`, `ip`, `dig`, `tmux` e `bc`.

## Causa
Agentes são treinados para resolver a tarefa, não para melhorar o ambiente.
Sem uma instrução explícita, contornar em silêncio é o comportamento esperado.

## Solução
1. Imagem mais completa por padrão ([filosofia da imagem](../guias/filosofia-da-imagem.md)).
2. Regra no [`sandbox/AGENTS.md`](../../sandbox/AGENTS.md): quando faltar algo que
   teria ajudado, dizer no fim da resposta e anotar em `~/.dev-sandbox/feedback.md`.
   O mantenedor revisa e decide o que entra no `Dockerfile`.

## O que mudou no dev-sandbox
`Dockerfile` e `sandbox/AGENTS.md` v0.2.
