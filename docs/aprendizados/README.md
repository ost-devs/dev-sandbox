# Aprendizados

Coisas que custaram horas para descobrir e que mudaram (ou explicam) o
dev-sandbox. Cada aprendizado é um arquivo curto, com data no nome:
`AAAA-MM-assunto-curto.md`.

**Quer contribuir com o seu?** Abra um PR com um arquivo novo seguindo o
modelo abaixo. Vale tudo que outra pessoa usando o dev-sandbox poderia
encontrar: um bug, um conflito com outro programa, uma ferramenta que fazia
falta, um jeito melhor de trabalhar com algum agente. Não precisa ter a
solução: um problema bem descrito já ajuda.

## Modelo

```markdown
# Título que descreve o sintoma

- **Data:** AAAA-MM
- **Ambiente:** distro, versão do Docker, agente e versão (o que for relevante)
- **Base:** evidência (aconteceu com você: diga onde e como), documentação
  (link oficial e data em que leu) ou análise (raciocínio que ainda não foi
  testado: diga o que confirmaria)

## Sintoma
O que você viu. Mensagem de erro exata, se tiver.

## Causa
O que estava acontecendo de verdade. Se não descobriu, diga.

## Solução
O que resolveu. Comandos, se tiver.

## O que mudou no dev-sandbox
Link para o commit/arquivo, ou "nada: só documentação".
```

## Índice

| Data | Aprendizado |
|---|---|
| 2026-10 | [Disco cheio: o Timeshift copiava o Docker a cada snapshot](./2026-10-disco-cheio-timeshift-docker.md) |
| 2026-10 | [Memória e histórico do Claude misturados entre projetos](./2026-10-memoria-misturada-entre-projetos.md) |
| 2026-10 | [Auto-update do Claude baixava versões que nunca eram usadas](./2026-10-claude-autoupdate-orfao.md) |
| 2026-10 | [Portas fixas: conflito com o Syncthing e um container por vez](./2026-10-portas-fixas.md) |
| 2026-10 | [O agente contorna ferramenta que falta e não avisa](./2026-10-agente-contorna-ferramenta-faltando.md) |
| 2026-10 | [Pasta com vários repositórios: hooks do git sem proteção](./2026-10-pasta-com-varios-repositorios.md) |
| 2026-10 | [O `/etc/claude-code/CLAUDE.md` carrega sozinho: a prova](./2026-10-etc-claude-md-carrega-sozinho.md) |
| 2026-10 | [O Playwright ignora o Chromium da imagem e pede para baixar navegadores](./2026-10-playwright-ignora-chromium-da-imagem.md) |
| 2026-10 | [Conversa longa parece memória, mas não é](./2026-10-conversa-longa-nao-e-memoria.md) |
| 2026-10 | [O leitor de `robots.txt` do Python proibia um site que libera tudo](./2026-10-robots-txt-403-proibe-tudo.md) |
| 2026-10 | [O Write e o Edit do Claude se recusam a escrever num link simbólico](./2026-10-write-edit-recusam-symlink.md) |
| 2026-10 | [Memória compartilhada por link aparece e abre igual a uma nota comum](./2026-10-memoria-compartilhada-por-link-carrega-igual.md) |
