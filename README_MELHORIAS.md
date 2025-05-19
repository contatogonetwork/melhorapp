# GoNetwork AI

Um sistema de gerenciamento para produção audiovisual com recursos avançados de gerenciamento de eventos, briefings, timelines e entregas.

## Melhorias Implementadas

O projeto recebeu as seguintes melhorias de código e estrutura, focando na qualidade e performance sem alterar a funcionalidade:

### 1. Qualidade de Código

- **Formatação Consistente**: Todo o código foi formatado usando Black e isort, garantindo um estilo consistente em todo o projeto.
- **Documentação**: Adicionadas docstrings detalhadas para classes e funções, facilitando a compreensão e manutenção.
- **Tratamento de Erros**: Implementado tratamento robusto de erros nos pontos críticos do sistema, especialmente em operações de banco de dados.
- **Logging**: Adicionado sistema de logging centralizado para rastreamento de operações e diagnóstico de problemas.

### 2. Performance e Otimização

- **Transações em Banco de Dados**: Implementado suporte a transações para operações em lote, garantindo integridade de dados e melhor performance.
- **Sistema de Cache**: Adicionado módulo de cache para dados frequentemente acessados, reduzindo consultas ao banco de dados.
- **Otimizações de UI**: Implementadas técnicas para melhorar a fluidez da interface de usuário em operações que atualizam múltiplos elementos.

### 3. Ferramentas de Desenvolvimento

- **Configuração VSCode**: Adicionadas configurações otimizadas para desenvolvimento com VSCode.
- **Scripts de Diagnóstico**: Criados scripts para diagnóstico do sistema e verificação de integridade.
- **Ambiente de Desenvolvimento**: Script de configuração automatizada do ambiente de desenvolvimento.

## Arquivos-Chave Adicionados

- `utils/logger.py`: Sistema de logging centralizado
- `utils/cache.py`: Implementação de cache para melhorar performance
- `gui/utils/optimization.py`: Utilitários para otimização da interface gráfica
- `setup_dev_environment.py`: Configuração automatizada do ambiente de desenvolvimento
- `.vscode/`: Configurações para melhor experiência com VSCode

## Arquivos-Chave Aprimorados

- `database/Database.py`: Adicionado suporte a transações e melhorado tratamento de erros
- `database/UserRepository.py`: Melhor documentação e tratamento de erros
- `gui/login_dialog.py`: Implementados indicadores visuais e melhor feedback ao usuário
- `setup_database.py`: Melhorado sistema de inicialização do banco de dados

## Executando o Projeto

### Pré-requisitos
- Python 3.8+
- PySide6
- SQLite3

### Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/seu-usuario/gonetwork-ai.git
   cd gonetwork-ai
   ```

2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o ambiente de desenvolvimento:
   ```
   python setup_dev_environment.py
   ```

5. Inicialize o banco de dados:
   ```
   python setup_database.py
   ```

6. Execute a aplicação:
   ```
   python main.py
   ```

## Scripts de Diagnóstico

Utilize os scripts a seguir para diagnosticar o estado do sistema:

1. Diagnóstico completo:
   ```
   python diagnostico_completo.py
   ```

2. Verificação de dependências:
   ```
   python verificar_dependencias.py
   ```

3. Testes interativos:
   ```
   python testes_interativos.py
   ```

## Credenciais de Exemplo

- **Admin:** username=admin, senha=admin123
- **Editor:** username=maria, senha=editor123
- **Cliente:** username=cliente, senha=client123
