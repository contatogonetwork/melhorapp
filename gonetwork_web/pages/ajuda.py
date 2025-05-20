import streamlit as st


def show():
    """Renderiza a página de ajuda e documentação da aplicação."""
    st.title("❓ Ajuda e Documentação")

    # Seções da documentação
    sections = {
        "Introdução": show_introduction,
        "Dashboard": show_dashboard_help,
        "Briefings": show_briefings_help,
        "Timeline": show_timeline_help,
        "Edições": show_edicoes_help,
        "Projetos": show_projetos_help,
        "Clientes": show_clientes_help,
        "FAQ": show_faq,
        "Suporte": show_support,
    }

    # Seleção da seção
    section = st.sidebar.radio("Navegação da Ajuda", list(sections.keys()))

    # Mostrar a seção selecionada
    sections[section]()

    # Rodapé comum a todas as páginas de ajuda
    st.markdown("---")
    st.caption(
        "Se você não encontrou o que procurava, entre em contato com o suporte técnico."
    )


def show_introduction():
    """Exibe a introdução e visão geral da aplicação."""
    st.header("Bem-vindo ao GoNetwork AI Web")

    st.write(
        """
    Esta é a versão web da plataforma de produção de conteúdo da GoNetwork.
    Aqui você pode gerenciar todos os aspectos da produção de vídeos, desde o briefing
    inicial até a entrega final.
    """
    )

    st.subheader("Funcionalidades Principais")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        * **Dashboard**: Visão geral do status dos projetos
        * **Briefings**: Gerenciamento de briefings de clientes
        * **Timeline**: Planejamento e acompanhamento de produção
        * **Edições**: Controle do processo de edição de vídeos
        """
        )

    with col2:
        st.markdown(
            """
        * **Projetos**: Gerenciamento completo de projetos
        * **Clientes**: Cadastro e gestão de clientes
        * **Relatórios**: Geração de relatórios e análises
        * **Configurações**: Personalização da plataforma
        """
        )

    st.subheader("Primeiros Passos")

    st.info(
        """
    1. Explore o Dashboard para ter uma visão geral
    2. Verifique os briefings e projetos em andamento
    3. Utilize a barra lateral para navegação rápida
    4. Personalize suas configurações na seção Configurações
    """
    )


def show_dashboard_help():
    """Exibe ajuda sobre o Dashboard."""
    st.header("Dashboard")

    st.write(
        """
    O Dashboard fornece uma visão geral do status atual de todos os projetos e atividades
    na plataforma GoNetwork AI Web.
    """
    )

    st.subheader("Elementos do Dashboard")

    st.markdown(
        """
    * **Métricas Principais**: Resumo quantitativo de briefings, edições, eventos e clientes
    * **Gráfico de Atividades**: Visualização das atividades da semana
    * **Próximos Eventos**: Lista de eventos agendados nos próximos dias
    * **Projetos Recentes**: Últimos projetos atualizados ou criados
    * **Notificações**: Alertas e lembretes importantes
    """
    )

    st.subheader("Dicas de Uso")

    st.success(
        """
    * O Dashboard é atualizado automaticamente a cada acesso
    * Clique nas métricas para acessar diretamente as seções correspondentes
    * Utilize os filtros para personalizar a visualização do Dashboard
    * Adicione notas do dia para lembretes rápidos
    """
    )


def show_briefings_help():
    """Exibe ajuda sobre a seção de Briefings."""
    st.header("Briefings")

    st.write(
        """
    A seção de Briefings permite gerenciar todas as informações iniciais dos projetos,
    incluindo requisitos do cliente, prazos e especificações técnicas.
    """
    )

    st.subheader("Recursos Principais")

    st.markdown(
        """
    * **Cadastro de Briefings**: Criação e edição de briefings completos
    * **Anexos**: Upload de arquivos de referência e documentos complementares
    * **Aprovação**: Fluxo de aprovação com cliente e equipe interna
    * **Histórico**: Registro de todas as alterações e comentários
    * **Exportação**: Geração de PDF ou compartilhamento de link do briefing
    """
    )

    st.subheader("Processo de Trabalho")

    st.info(
        """
    1. Crie um novo briefing com as informações básicas do projeto
    2. Adicione detalhes específicos e anexos relevantes
    3. Compartilhe com o cliente para revisão e aprovação
    4. Após aprovação, inicie o planejamento na Timeline
    5. Mantenha o briefing atualizado durante todo o projeto
    """
    )


def show_timeline_help():
    """Exibe ajuda sobre a seção de Timeline."""
    st.header("Timeline")

    st.write(
        """
    A Timeline permite planejar e visualizar todo o fluxo de trabalho da produção,
    desde o briefing até a entrega final.
    """
    )

    st.subheader("Funcionalidades")

    st.markdown(
        """
    * **Visualização de Calendário**: Planejamento visual das etapas de produção
    * **Alocação de Equipe**: Designação de responsáveis para cada atividade
    * **Dependências**: Definição de relações entre atividades
    * **Status**: Acompanhamento do progresso de cada etapa
    * **Alertas**: Notificações de prazos e atrasos
    """
    )

    st.subheader("Como Utilizar")

    st.success(
        """
    * Arraste e solte atividades para reorganizar o calendário
    * Use as cores para identificar rapidamente o status de cada etapa
    * Configure alertas para receber notificações sobre prazos importantes
    * Exporte a timeline para compartilhar com a equipe ou clientes
    """
    )


def show_edicoes_help():
    """Exibe ajuda sobre a seção de Edições."""
    st.header("Edições")

    st.write(
        """
    A seção de Edições é dedicada ao controle e gerenciamento do processo de
    edição e pós-produção dos vídeos.
    """
    )

    st.subheader("Recursos Disponíveis")

    st.markdown(
        """
    * **Cadastro de Edições**: Registro de todos os projetos de edição
    * **Versões**: Controle de versões de cada vídeo
    * **Comentários**: Feedback e solicitações de ajustes
    * **Aprovação**: Fluxo de aprovação interna e do cliente
    * **Entrega**: Controle de formatos e especificações técnicas
    """
    )

    st.subheader("Fluxo de Trabalho")

    st.info(
        """
    1. Crie uma nova edição associada a um briefing
    2. Designe o editor responsável
    3. Registre cada versão do vídeo
    4. Colete e implemente feedback
    5. Obtenha aprovação final
    6. Entregue os arquivos finais
    """
    )


def show_projetos_help():
    """Exibe ajuda sobre a seção de Projetos."""
    st.header("Projetos")

    st.write(
        """
    A seção de Projetos oferece uma visão completa e integrada de todos os aspectos
    de cada projeto, incluindo briefing, timeline, edições e entregas.
    """
    )

    st.subheader("Características Principais")

    st.markdown(
        """
    * **Visão Consolidada**: Agregação de todas as informações do projeto
    * **Equipe**: Gerenciamento da equipe envolvida
    * **Documentos**: Repositório centralizado de arquivos
    * **Comunicação**: Histórico de comentários e interações
    * **Status**: Acompanhamento geral do progresso
    """
    )

    st.subheader("Gerenciamento Eficiente")

    st.success(
        """
    * Use a visão geral para ter um panorama completo de todos os projetos
    * Filtre por status, cliente ou membro da equipe
    * Acesse rapidamente qualquer aspecto do projeto
    * Gere relatórios de progresso e desempenho
    """
    )


def show_clientes_help():
    """Exibe ajuda sobre a seção de Clientes."""
    st.header("Clientes")

    st.write(
        """
    A seção de Clientes permite gerenciar todos os dados e relacionamentos
    com os clientes da GoNetwork.
    """
    )

    st.subheader("Funcionalidades")

    st.markdown(
        """
    * **Cadastro de Clientes**: Informações completas sobre cada cliente
    * **Contatos**: Gestão de múltiplos contatos por cliente
    * **Histórico**: Registro de todos os projetos e interações
    * **Documentos**: Contratos e outros documentos importantes
    * **Preferências**: Configurações específicas para cada cliente
    """
    )

    st.subheader("Dicas de Uso")

    st.info(
        """
    1. Mantenha as informações de contato sempre atualizadas
    2. Registre todas as interações importantes com o cliente
    3. Use tags para categorizar clientes
    4. Consulte o histórico antes de iniciar novos projetos
    """
    )


def show_faq():
    """Exibe perguntas frequentes."""
    st.header("Perguntas Frequentes")

    faq = [
        {
            "pergunta": "Como recuperar minha senha?",
            "resposta": "Entre em contato com o administrador do sistema para redefinir sua senha.",
        },
        {
            "pergunta": "É possível acessar a plataforma pelo celular?",
            "resposta": "Sim, a interface é responsiva e funciona em dispositivos móveis, mas recomendamos o uso em desktops para melhor experiência.",
        },
        {
            "pergunta": "Como adicionar um novo membro à equipe?",
            "resposta": "Apenas administradores podem adicionar novos usuários. Acesse Configurações > Usuários > Adicionar Novo Usuário.",
        },
        {
            "pergunta": "Posso exportar dados para Excel?",
            "resposta": "Sim, a maioria das tabelas possui um botão de exportação para CSV ou Excel.",
        },
        {
            "pergunta": "Como compartilhar um briefing com um cliente?",
            "resposta": "Na página do briefing, clique em 'Compartilhar', selecione as permissões desejadas e copie o link gerado.",
        },
    ]

    for item in faq:
        with st.expander(item["pergunta"]):
            st.write(item["resposta"])


def show_support():
    """Exibe informações de suporte."""
    st.header("Suporte Técnico")

    st.write(
        """
    Se você encontrou um problema ou precisa de assistência adicional,
    entre em contato com nossa equipe de suporte.
    """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Canais de Atendimento")
        st.markdown(
            """
        * **E-mail**: suporte@gonetwork.com.br
        * **Telefone**: (11) 3456-7890
        * **Chat**: Disponível em dias úteis, das 9h às 18h
        """
        )

    with col2:
        st.subheader("Recursos Adicionais")
        st.markdown(
            """
        * [Documentação Completa](https://docs.gonetwork.ai)
        * [Tutoriais em Vídeo](https://gonetwork.ai/tutoriais)
        * [Base de Conhecimento](https://gonetwork.ai/kb)
        """
        )

    # Formulário de contato
    st.subheader("Formulário de Contato")

    with st.form("support_form"):
        assunto = st.text_input("Assunto")
        descricao = st.text_area("Descrição do problema")
        prioridade = st.select_slider(
            "Prioridade", options=["Baixa", "Média", "Alta", "Crítica"]
        )
        anexo = st.file_uploader(
            "Anexar arquivo (opcional)", type=["png", "jpg", "pdf"]
        )

        if st.form_submit_button("Enviar"):
            st.success("Sua solicitação foi enviada! Em breve entraremos em contato.")
