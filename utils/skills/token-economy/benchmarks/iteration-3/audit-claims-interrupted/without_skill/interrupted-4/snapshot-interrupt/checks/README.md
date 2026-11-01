# Contrato dos checks
Um arquivo por módulo: `checks/check_<modulo>.py` (só stdlib, Python 3.11).
- Roda da raiz do projeto: `python3 checks/check_<modulo>.py [ID ...]` (sem IDs = todas as 19 do módulo).
- Uma função por afirmação, registrada em um dict `CHECKS = {'T01': fn, ...}`.
- Cada função retorna `(verdadeira: bool, contraexemplo: str|None)`; contraexemplo é o repr de entradas concretas + saída obtida/esperada.
- Afirmações universais ("para qualquer s"): combine casos de borda fixos escolhidos à mão (unicode, vazio, espaços, negativos, etc.) com busca aleatória usando `random.Random(SEED)` onde SEED é uma constante no topo do arquivo (ex.: 20261101). Nunca use random global nem hash/ordem não determinísticos.
- Veredito "verdadeira" para universais significa "nenhum contraexemplo encontrado" — use busca ampla (>= 20000 casos, alfabeto que inclua unicode/acentos/espaços/símbolos/emoji/combining). Se achar contraexemplo, minimize-o e fixe-o no arquivo como caso fixo.
- Saída: uma linha JSON por afirmação: {"id","verdict":"verdadeira"|"falsa","counterexample":...,"command":"python3 checks/check_<modulo>.py <ID>"}. Exit code 0 sempre que rodou.
- Exceção inesperada do código sob teste que contradiga a afirmação conta como contraexemplo (registre a exceção).
- Ler o código ajuda a escolher entradas, mas o veredito vem da execução. Não modifique kit/ nem claims.md.
- Ao final escreva também `checks/results_<modulo>.jsonl` (saída do script) e confirme rodando duas vezes que o resultado é idêntico.
