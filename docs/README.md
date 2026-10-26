# Documentação do dev-sandbox

Comece pelo [README](../README.md) para instalar. O *porquê* de cada linha do
script e do `Dockerfile` está em [`DOCUMENTACAO.md`](../DOCUMENTACAO.md).

## Guias

| Guia | Para quando você quer... |
|---|---|
| [Segurança](./guias/seguranca.md) | Saber o que o container protege, o que não protege e onde estão as brechas |
| [Backup e git](./guias/backup-e-git.md) | Desfazer besteira do agente e guardar as configs dos agentes sem vazar tokens |
| [Portas e sessões paralelas](./guias/portas-e-sessoes-paralelas.md) | Ver o app no navegador, lidar com Tauri, rodar vários containers ou agentes |
| [Filosofia da imagem](./guias/filosofia-da-imagem.md) | Entender o tamanho da imagem, adicionar linguagens, liberar disco |
| [Atualização](./guias/atualizacao.md) | Atualizar agentes, imagem e host, e voltar atrás se algo quebrar |

## Claude Code

| Guia | Para quando você quer... |
|---|---|
| [Memória e instruções](./claude-code/memoria-e-instrucoes.md) | Entender memória automática, `CLAUDE.md`, `AGENTS.md` e rules |
| [Sessões e persistência](./claude-code/sessoes-e-persistencia.md) | Saber o que sobrevive ao `exit` e retomar trabalho depois |
| [Trabalhar por projeto](./claude-code/projetos.md) | Organizar projetos, instruções e memória ao longo do tempo |
| [Preservar conversas](./claude-code/preservar-conversas.md) | Não perder sessões valiosas para a faxina de 30 dias |
| [Migrar memórias](./claude-code/migrar-memorias.md) | Levar memórias de um caminho de projeto para outro |
| [Por baixo dos panos](./claude-code/por-baixo-dos-panos/README.md) | Entender contexto, cache, compactação e subagentes, e por que conversas longas custam mais |
| [Modelo e esforço](./claude-code/modelo-e-esforco.md) | Escolher modelo e esforço sem usar bazuca para matar mosca |

## Aprendizados

[`aprendizados/`](./aprendizados/README.md): problemas reais, causas e
soluções. Contribuições são bem-vindas.
