# GoNetwork AI Web

Versão web da plataforma de produção de vídeo da GoNetwork, implementada com Streamlit.

## Sobre o Projeto

GoNetwork AI Web é a versão web da ferramenta de gerenciamento de produção de vídeos da GoNetwork. Esta versão permite o acesso remoto e multiplataforma a todas as funcionalidades presentes na versão desktop, com uma interface moderna e responsiva.

## Estrutura do Projeto

O projeto segue as melhores práticas para aplicações Streamlit:

```
gonetwork_web/
├── app.py                  # Ponto de entrada principal
├── requirements.txt        # Lista de dependências
├── .streamlit/             # Configurações do Streamlit
│   ├── config.toml         # Configurações de tema e interface
│   └── secrets.toml        # Segredos (não incluído no Git)
├── pages/                  # Páginas da aplicação
│   ├── dashboard.py        # Dashboard principal
│   ├── briefings.py        # Gestão de briefings
│   ├── timeline.py         # Timeline de produção
│   ├── edicoes.py          # Controle de edições
│   ├── projetos.py         # Gerenciamento de projetos
│   ├── clientes.py         # Gestão de clientes
│   ├── relatorios.py       # Relatórios e análises
│   ├── settings.py         # Configurações do sistema
│   └── ajuda.py            # Documentação e ajuda
├── components/             # Componentes reutilizáveis
│   ├── sidebar.py          # Componente da barra lateral
│   ├── authentication.py   # Sistema de autenticação
│   ├── common.py           # Componentes comuns (cards, footer, etc)
│   ├── project_card.py     # Card de projetos
│   └── file_uploader.py    # Componente de upload
├── utils/                  # Funções utilitárias
│   ├── database.py         # Conexão com banco de dados
│   ├── state_management.py # Gerenciamento de estado
│   ├── notifications.py    # Sistema de notificações
│   ├── formatters.py       # Formatadores de texto/data
│   └── initialize_database.py # Inicialização do banco de dados
├── styles/                 # Recursos de estilo
│   └── main.css            # CSS personalizado
├── assets/                 # Recursos estáticos
│   └── logo_gonetwork.png  # Logo da aplicação
└── data/                   # Dados locais
    └── gonetwork.db        # Banco de dados SQLite
```

## Funcionalidades Principais

- **Dashboard interativo**: Visão geral do status dos projetos com métricas e gráficos
- **Gestão de briefings**: Criação e acompanhamento de briefings de clientes
- **Timeline de produção**: Planejamento e acompanhamento visual das etapas
- **Controle de edições**: Gerenciamento do processo de edição de vídeos
- **Projetos**: Visão consolidada de todos os aspectos de um projeto
- **Clientes**: Cadastro e gestão de relacionamento com clientes
- **Relatórios**: Geração de relatórios e análises de produção
- **Multi-user**: Suporte a múltiplos usuários com controle de acesso

## Requisitos

- Python 3.9+
- Streamlit 1.29.0+
- SQLite 3

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/contatogonetwork/melhorapp.git
   ```

2. Entre na pasta do projeto:
   ```
   cd melhorapp/gonetwork_web
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

4. Configure o arquivo de segredos:
   ```
   cp .streamlit/secrets.toml.template .streamlit/secrets.toml
   ```
   Edite o arquivo `.streamlit/secrets.toml` com suas credenciais e configurações.

5. Execute a aplicação:
   ```
   # Usando scripts de inicialização automática
   # PowerShell:
   ./start_web.ps1

   # Ou CMD:
   start_web.bat

   # Ou diretamente:
   streamlit run app.py
   ```

## Desenvolvimento

Para desenvolvedores que desejam contribuir com o projeto:

1. Crie uma branch a partir da `main`:
   ```
   git checkout -b feature/sua-funcionalidade
   ```

2. Faça suas alterações seguindo os padrões do projeto

3. Execute os testes:
   ```
   python run_tests.py
   ```

4. Envie um pull request para revisão

## Deploy

A aplicação está configurada para deploy no Streamlit Community Cloud:

1. Faça login no [Streamlit Community Cloud](https://share.streamlit.io/)
2. Conecte ao repositório GitHub
3. Selecione o diretório `gonetwork_web` e o arquivo `app.py`
4. Configure os segredos necessários no painel de administração

## Contato

- Suporte: suporte@gonetwork.com.br
- Site: [gonetwork.ai](https://gonetwork.ai)

## Licença

Este é um software proprietário da GoNetwork. Todos os direitos reservados.

© 2025 GoNetwork
