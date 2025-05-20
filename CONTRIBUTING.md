# Guia de Contribuição para o GoNetwork AI

Este documento fornece diretrizes para contribuir com o desenvolvimento do GoNetwork AI. Seguir estas práticas garantirá uma colaboração eficiente e a manutenção da qualidade do código.

## 🌍 Ambiente de Desenvolvimento

### Configuração Inicial

1. Clone o repositório:
   ```bash
   git clone https://github.com/contatogonetwork/melhorapp.git
   cd melhorapp
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as ferramentas de desenvolvimento:
   ```bash
   pre-commit install
   ```

### Extensões VS Code Recomendadas

- Python (Microsoft)
- Pylance
- Python Docstring Generator
- Python Test Explorer
- SQLite Viewer
- Error Lens
- GitLens
- Black Formatter

## 🧪 Testes

Execute os testes antes de enviar qualquer alteração:

```bash
python run_tests.py
```

Para testes específicos:

```bash
pytest tests/database
pytest tests/gui/widgets -v
```

## 🖌️ Estilo de Código

Este projeto segue as convenções do PEP 8 com algumas modificações:

- Comprimento máximo de linha: 88 caracteres (padrão Black)
- Docstrings no formato Google Style
- Tipagem estática com anotações de tipo do Python 3.9+

### Ferramentas de Formatação

- **Black**: Formatador de código
  ```bash
  black .
  ```

- **isort**: Ordenação de importações
  ```bash
  isort .
  ```

- **mypy**: Verificação de tipos
  ```bash
  mypy .
  ```

## 📝 Commits e Pull Requests

### Mensagens de Commit

Use mensagens de commit claras e descritivas seguindo o formato:

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
```

Tipos de commit:
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação, ponto-e-vírgula, etc.
- `refactor`: Refatoração de código
- `test`: Adição/correção de testes
- `chore`: Tarefas de manutenção

### Processo de Pull Request

1. Crie um branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```

2. Faça seus commits seguindo as convenções acima
3. Execute os testes para garantir que nada foi quebrado
4. Envie o branch para o repositório:
   ```bash
   git push origin feature/nome-da-feature
   ```
5. Abra um Pull Request descrevendo as alterações

## 📚 Documentação

Atualize a documentação para qualquer nova funcionalidade ou alteração:

1. Docstrings para funções e classes
2. Atualização do README.md quando necessário
3. Para documentação mais abrangente, atualize/crie arquivos .md na pasta `docs/`

Para gerar a documentação completa:

```bash
python generate_docs.py
```

## 🔄 Workflows Padrão

### Desenvolvimento de Novas Features

1. Atualize sua branch principal:
   ```bash
   git checkout main
   git pull
   ```

2. Crie um branch para sua feature:
   ```bash
   git checkout -b feature/nome-da-feature
   ```

3. Implemente a feature e escreva testes
4. Execute os testes localmente
5. Envie para revisão

### Correção de Bugs

1. Identifique o problema e crie um issue se não existir
2. Crie um branch para o bug:
   ```bash
   git checkout -b fix/nome-do-bug
   ```

3. Corrija o bug e adicione um teste que demonstre a correção
4. Execute todos os testes
5. Envie para revisão

## 📱 Problemas e Suporte

Se você encontrar problemas ou tiver dúvidas:

1. Verifique os issues existentes
2. Crie um novo issue com detalhes e passos para reproduzir o problema
3. Para suporte técnico, entre em contato com a equipe de desenvolvimento
