# checks/
Um script por módulo: `python3 checks/check_<modulo>.py [ID ...]` (rodar da raiz do projeto).
Saída: uma linha JSON por afirmação em stdout: {"id","verdict":"verdadeira|falsa","counterexample","note"}.
Também grava checks/results_<modulo>.json. Aleatoriedade só com `random.Random(SEED)`, SEED constante no topo do script.
