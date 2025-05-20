import streamlit as st


def display_footer():
    """
    Exibe o rodapé padrão da aplicação com links e informações de copyright
    """
    footer_html = """
    <div class="footer">
        <p>© 2025 GoNetwork AI - Todos os direitos reservados</p>
        <p>Versão 1.0.0 | <a href="mailto:suporte@gonetwork.com.br">Suporte</a></p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


def show_toast(title, message, icon="info"):
    """
    Exibe uma notificação toast na interface

    Args:
        title: Título da notificação
        message: Mensagem da notificação
        icon: Ícone a ser exibido (info, success, warning, error)
    """
    if icon == "success":
        st.success(f"**{title}**: {message}")
    elif icon == "warning":
        st.warning(f"**{title}**: {message}")
    elif icon == "error":
        st.error(f"**{title}**: {message}")
    else:  # info
        st.info(f"**{title}**: {message}")


def create_card(title, content, icon=None, color="blue"):
    """
    Cria um card estilizado

    Args:
        title: Título do card
        content: Conteúdo do card (texto ou HTML)
        icon: Ícone opcional para o card
        color: Cor do card (blue, green, orange, red)
    """
    # Validar cor
    valid_colors = ["blue", "green", "orange", "red"]
    if color not in valid_colors:
        color = "blue"

    # Ícone padrão para cada cor se não for especificado
    if not icon:
        icons = {"blue": "ℹ️", "green": "✅", "orange": "⚠️", "red": "❌"}
        icon = icons[color]

    # HTML do card
    card_html = f"""
    <div class="card card-{color}">
        <div class="card-header">
            <div class="card-icon">{icon}</div>
            <h3>{title}</h3>
        </div>
        <div class="card-content">
            {content}
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)


def data_table(df, key=None, selection="single", height=400):
    """
    Exibe uma tabela de dados interativa

    Args:
        df: DataFrame pandas
        key: Chave única para o componente
        selection: Modo de seleção ('single', 'multi', None)
        height: Altura da tabela em pixels

    Returns:
        Linhas selecionadas
    """
    # Verificar se o DataFrame é válido
    if df is None or df.empty:
        st.info("Sem dados para exibir")
        return None

    # Verificar se tem o recurso AgGrid
    try:
        from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

        gb = GridOptionsBuilder.from_dataframe(df)

        # Configurar seleção
        if selection == "single":
            gb.configure_selection(selection_mode="single", use_checkbox=False)
        elif selection == "multi":
            gb.configure_selection(selection_mode="multiple", use_checkbox=True)

        # Outras configurações
        gb.configure_pagination(
            enabled=True, paginationAutoPageSize=False, paginationPageSize=10
        )
        gb.configure_grid_options(domLayout="normal")
        grid_options = gb.build()

        # Renderizar tabela
        grid_response = AgGrid(
            df,
            gridOptions=grid_options,
            height=height,
            theme="streamlit",
            update_mode=GridUpdateMode.MODEL_CHANGED,
            key=key,
            allow_unsafe_jscode=False,
        )

        return grid_response.selected_rows

    except ImportError:
        # Fallback para a tabela do Streamlit
        st.write("Visualização de tabela simplificada:")
        st.dataframe(df, height=height)
        return None
