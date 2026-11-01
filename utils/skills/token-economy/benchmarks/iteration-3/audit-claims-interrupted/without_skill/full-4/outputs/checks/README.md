# Convenção das checagens
- Um arquivo por módulo: `checks/<modulo>.py` (só stdlib, sem hypothesis). Rodar da raiz: `python3 -I checks/<modulo>.py [ID ...]`.
- Cada afirmação (ex. T05) tem uma função `check_T05()` que devolve `(True, None)` se verdadeira ou `(False, "contraexemplo legível com entradas exatas")` se falsa.
- Afirmações "para qualquer s/n": combine casos de borda fixos + geração aleatória com `random.Random(SEED)` (SEED constante registrada no arquivo, ex. 12345, ≥2000 amostras, incluindo unicode, vazio, espaços, negativos). Veredito falsa só com contraexemplo concreto executado; verdadeira só após busca sem falha (e raciocínio sobre o código).
- Saída (stdout), uma linha JSON por afirmação: `{"id":"T05","verdict":"verdadeira|falsa","counterexample":null|"...","command":"python3 -I checks/text.py T05"}`. Sem ID → roda todas. Saída determinística.
- `import sys; sys.path.insert(0, <raiz do projeto>)` calculado a partir de `__file__`, para importar `kit`.
