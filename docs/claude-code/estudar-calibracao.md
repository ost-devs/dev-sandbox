# Calibração da `/estudar`

O que a skill [`/estudar`](../../utils/skills/estudar/SKILL.md) aprendeu
transformando artigos da web em guias deste repositório. Ela lê este arquivo
**antes** de cada estudo e o atualiza **depois**. Você também escreve aqui.
O objetivo é que cada estudo precise de menos correção que o anterior.

## Como calibrar

| Quem | Como |
|---|---|
| Você | Escreva uma regra em [Regras](#regras), ou diga `/estudar calibrar: <regra>`. Exemplo: "guias com no máximo duas tabelas" |
| Você, sem escrever nada | Corrija os guias que a skill escreveu e faça o commit. No estudo seguinte, ela compara o que escreveu com o que você mudou e propõe regras para as diferenças que se repetem |
| A skill | Ao fim de cada estudo, registra em [Estudos](#estudos) e em [Fontes](#fontes) quantos fatos se confirmaram, e só cria uma regra quando a lição teria mudado aquele estudo |

**Como saber se está melhorando:** a coluna "Sua revisão" de [Estudos](#estudos)
(quanto você mudou depois). Ela deve cair com o tempo. O mesmo princípio do
[diário de campo](./modelo-e-esforco.md#diário-de-campo) do guia de modelo:
medir em vez de supor.

## Regras

Valem em todo estudo. Cada uma diz de onde veio.

1. **Só o que se aplica ao dev-sandbox, sempre com as referências** (o artigo
   e as páginas oficiais usadas). Usuário, 28/10/2026.
2. **A data "modified" do artigo não é confiável.** Na SSD Nodes, 3 de 7
   artigos tinham modificação **anterior** à publicação. Use a data de
   publicação. Agente, 28/10/2026.
3. **Confira primeiro os artigos mais antigos.** O de julho trazia preços e
   modelos superados; os de outubro estavam quase todos certos. Agente,
   28/10/2026.
4. **Confira também os guias do próprio projeto.** A conferência achou um
   guia nosso desatualizado (o `modelo-e-esforco.md` dizia que não havia
   modelo Mythos) e um erro escrito no mesmo dia ("trocar de modelo não
   adianta no limite", sem a exceção do limite por família). Agente,
   28/10/2026.
5. **Frase geral só entra com as exceções da documentação.** Mesma
   evidência da regra 4. Agente, 28/10/2026.
6. **Mande ao pesquisador a lista inteira de uma vez.** Cada lote de 15 a 17
   fatos levou ~1 minuto e ~60 mil tokens do contexto dele, sem pesar na
   conversa principal. Agente, 28/10/2026.

## Fontes

| Fonte | Estudos | Fatos conferidos | Confirmados | Em parte | Sem fonte oficial | Errados ou velhos | Observação |
|---|---|---|---|---|---|---|---|
| SSD Nodes (ssdnodes.com/learn) | 2 | 32 | 20 | 8 | 3 | 1 (+1 artigo inteiro de julho) | Artigos de outubro, recentes e precisos; datas soltas ("desde 7/10") às vezes sem fonte oficial |

## Estudos

| Data | Artigos | Escrito | Fatos (confirmados / em parte / sem fonte / errados) | Commit | Sua revisão |
|---|---|---|---|---|---|
| 28/10/2026 | [Tokens no Claude Code](https://www.ssdnodes.com/learn/lang/pt/claude-code-token-usage-explained) | `por-baixo-dos-panos/quanto-custa.md` (novo), `cache-de-prompt.md` | 12 / 4 / 1 / 0 | `7a8d0d9` | pendente |
| 28/10/2026 | 6 da mesma série; usados: [limite atingido](https://www.ssdnodes.com/learn/lang/pt/claude-limit-reached-what-to-do) e [qual modelo](https://www.ssdnodes.com/learn/lang/pt/opus-sonnet-haiku-which-model). Descartados: Claude × ChatGPT (fora do escopo), VPS com tmux (o dev-sandbox já usa tmux no host), 1M de tokens (coberto pelo `quanto-custa.md`), Claude no Linux (instalação; credenciais já tratadas) | `limite-de-uso.md` (novo), `modelo-e-esforco.md`, `quanto-custa.md`, `projetos.md` | 8 / 4 / 2 / 1 | `86c7f8d` | pendente |
