# Pasta com vários repositórios: hooks do git sem proteção

- **Data:** 2026-10
- **Ambiente:** dev-sandbox v0.2 (antes de instalado), projeto Rust com
  repositórios de referência clonados ao lado, numa mesma pasta montada
- **Base:** análise (lendo o `dev-docker` v0.2 contra uma pasta real); a
  correção foi testada só a seco, com um `sudo` falso

## Sintoma
Nenhum visível, e esse é o problema. Numa pasta assim:

```text
meu-workspace/
├── projeto/          (repositório principal)
├── biblioteca-a/     (repositório de referência)
└── biblioteca-b/     (repositório de referência)
```

a proteção do `.git` da v0.2 olhava só `meu-workspace/.git`, que não existe.
Os hooks de `projeto/`, `biblioteca-a/` e `biblioteca-b/` ficavam graváveis
pelo agente, e rodam no host no próximo `git commit` ou `git pull` neles.

## Causa
A v0.2 supunha "uma pasta montada = um repositório".

## Solução
O `dev-docker` protege o `.git/hooks` e o `.git/config` de todo repositório
até dois níveis abaixo da pasta montada, e mostra quantos protegeu. Continuam
de fora (documentado em [segurança](../guias/seguranca.md)): repositórios mais
fundos, hooks de submódulos e repositórios clonados durante a sessão.

## O que mudou no dev-sandbox
`dev-docker` (proteção de `.git` aninhados), [segurança](../guias/seguranca.md),
`DOCUMENTACAO.md`.
