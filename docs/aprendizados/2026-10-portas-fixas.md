# Portas fixas: conflito com o Syncthing e um container por vez

- **Data:** 2026-10

## Sintoma
```text
docker: Error response from daemon: ... failed to bind host port 127.0.0.1:8080/tcp: address already in use
```
E, mesmo depois de trocar a porta, não dava para abrir um segundo container.

## Causa
O script publicava 3000, 5173, 8000 e 8080 em toda sessão. O Syncthing do host
já usava a 8080. E duas sessões não podem publicar a mesma porta.

## Solução
Portas viraram opcionais: `DEV_PORTS="5173" dev-docker`. Sem portas, quantos
containers quiser.

## O que mudou no dev-sandbox
`dev-docker` v0.2. Guia: [portas e sessões paralelas](../guias/portas-e-sessoes-paralelas.md).
