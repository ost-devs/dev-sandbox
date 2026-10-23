# Disco cheio: o Timeshift copiava o Docker a cada snapshot

- **Data:** 2026-10
- **Ambiente:** Linux Mint 22.3, `/` de 92 GB e `/home` separada, Docker com snapshotter do containerd, Timeshift em modo RSYNC

## Sintoma
A partição raiz ficou com 8,4 GB livres de 92 GB. O sistema em si ocupava uns 13 GB.

## Causa
| Item | Espaço |
|---|---|
| Snapshots do Timeshift | 49 GB, dos quais **~29 GB eram cópias de `/var/lib/containerd`** |
| `/var/lib/containerd` (imagem + cache de build) | 17 GB, sendo ~7 GB de cache de build antigo |
| Sistema | ~13 GB |

O Timeshift exclui `/var/lib/docker` por padrão, mas **não** `/var/lib/containerd`.
Com o Docker usando o snapshotter do containerd, é ali que as imagens ficam.
Cada rebuild da imagem do dev-sandbox virava mais GB nos snapshots seguintes.
O snapshot mais recente guardava 23 GB de containerd, mais do que o Docker ocupava
naquele momento: imagens e caches que já tinham sido apagados.

Um detalhe atrasou a correção: o filtro de exclusão foi digitado como
` /var/lib/containerd/**`, **com um espaço no começo**. O Timeshift aceitou e
simplesmente não excluiu nada.

## Solução
1. Filtros do Timeshift: `/var/lib/containerd/**` (sem espaço!).
2. Local dos snapshots mudado para a partição da `/home` (que tinha 264 GB livres).
3. Snapshot novo criado antes de apagar os antigos; depois, os 5 antigos apagados.
4. `sudo docker builder prune --filter until=96h`.

Resultado: de 8,4 GB para 58 GB livres na raiz.

## O que mudou no dev-sandbox
Documentação: [filosofia da imagem](../guias/filosofia-da-imagem.md#onde-a-imagem-ocupa-espaço-no-seu-disco).
