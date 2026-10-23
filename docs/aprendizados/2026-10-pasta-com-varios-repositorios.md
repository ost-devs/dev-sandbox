# Pasta com vários repositórios: caminhos absolutos e hooks sem proteção

- **Data:** 2026-10
- **Ambiente:** dev-sandbox v0.2 (antes de instalado), projeto Rust que usa
  outros repositórios clonados ao lado como referência
- **Base:** análise (lendo o `dev-docker` v0.2 contra uma pasta real); o
  script corrigido foi testado só a seco, com um `sudo` falso

## Sintoma
Dois problemas previstos ao trocar a v0.1 pela v0.2 numa pasta assim:

```text
~/Documentos/.../meu-workspace/
├── projeto/          (repositório principal)
├── biblioteca-a/     (repositório de referência)
└── biblioteca-b/     (repositório de referência)
```

1. A documentação e os scripts do projeto apontam tudo a partir de
   `/workspace/...`. Na v0.2 a pasta aparece no caminho do host, então
   `/workspace` não existe mais e os scripts quebram.
2. A proteção do `.git` da v0.2 olhava só `meu-workspace/.git`, que não
   existe. Os hooks de `projeto/`, `biblioteca-a/` e `biblioteca-b/` ficavam
   graváveis pelo agente, e rodam no host no próximo `git commit`.

## Causa
A v0.2 supunha "uma pasta montada = um repositório".

## Solução
- O `dev-docker` monta a pasta no caminho do host **e** em `/workspace`. Os
  caminhos absolutos da documentação funcionam sem tradução, e a memória do
  Claude continua separada por projeto, desde que ele seja aberto pelo
  caminho do host ([detalhes](../../DOCUMENTACAO.md#por-que-o-projeto-e-montado-no-mesmo-caminho-do-host)).
  Uma primeira versão usava uma variável (`DEV_MOUNT_AT`) e foi descartada:
  é mais uma coisa para lembrar ao abrir o container.
- O `dev-docker` protege o `.git/hooks` e o `.git/config` de todo repositório
  até dois níveis abaixo da pasta montada, e mostra quantos protegeu.

## O que mudou no dev-sandbox
`dev-docker` (`/workspace` como segundo ponto de montagem, proteção de `.git` aninhados),
[segurança](../guias/seguranca.md), `DOCUMENTACAO.md`.
