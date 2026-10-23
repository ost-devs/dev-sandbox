[GEMINI](./GEMINI.md)
# Ambiente de Execução e Fronteiras de Dependência

Você está executando dentro de um contêiner Docker efêmero iniciado com a flag `--rm`.
Apenas arquivos mapeados via volumes persistentes sobrevivem entre execuções.

## 1. Fronteiras de Persistência e Armazenamento
- **Arquivos do Projeto (`/workspace`)**: Totalmente persistente (montado na pasta do repositório no host).
- **Caches de Pacotes (`/root/.npm`, `/usr/local/cargo/registry`)**: Persistente via volumes de cache no host.
- **Credenciais e Configurações (`/root/.gemini`)**: Persistente. Contém `Dockerfile.template`.
- **Sistema Operacional (`/`, `/usr`, `/lib`, `/etc`)**: NÃO PERSISTENTE. Destruído ao sair da sessão.

## 2. Regras para Resolução de Dependências
- **Ferramentas de Nível de Projeto**: Sempre instale via gerenciadores do repositório local (`npm`, `cargo`, `pip`) dentro de `/workspace`.
- **Dependências de Sistema (SO/Compiladores/Bibliotecas C-C++)**:
  - NÃO leia `/root/.gemini/Dockerfile.template` durante o fluxo normal para economizar tokens de contexto.
  - Se uma compilação ou comando falhar por falta de dependência a nível de SO:
    1. **Parar e Explicar**: Identifique a dependência ausente, explique por que o repositório exige isso e informe se é algo recorrente para essa stack.
    2. **Aguardar Confirmação**: NÃO instale pacotes nem edite arquivos antes da confirmação explícita do usuário.
    3. **Após a Confirmação do Usuário**:
       - Execute o comando de instalação temporária na sessão atual (ex: `apt-get install -y <pacote>`) para que o trabalho continue sem interromper o fluxo nem reiniciar o container.
       - Leia `/root/.gemini/Dockerfile.template`, adicione a instrução de instalação de forma limpa e salve o arquivo atualizado.
