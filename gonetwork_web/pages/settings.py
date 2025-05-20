import json
import os

import pandas as pd
import streamlit as st
from config import load_config, save_config

from utils.database import Database


def show():
    """Renderiza a página de configurações do aplicativo."""
    st.title("⚙️ Configurações")

    # Carregar as configurações atuais
    config = load_config()

    # Criar abas para diferentes tipos de configurações
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Configurações Gerais",
            "Banco de Dados",
            "Aparência",
            "Informações do Sistema",
        ]
    )

    with tab1:
        st.header("Configurações Gerais")

        with st.form("general_settings"):
            # Nome da aplicação
            app_name = st.text_input(
                "Nome da Aplicação", value=config.get("app_name", "GoNetwork AI Web")
            )

            # Outros ajustes gerais
            show_splash = st.checkbox(
                "Mostrar tela de splash", value=config.get("show_splash", True)
            )
            auto_refresh = st.checkbox(
                "Atualização automática", value=config.get("auto_refresh", False)
            )
            refresh_interval = st.number_input(
                "Intervalo de atualização (segundos)",
                min_value=30,
                max_value=600,
                value=config.get("refresh_interval", 300),
                disabled=not auto_refresh,
            )

            # Botão para salvar configurações gerais
            if st.form_submit_button("Salvar Configurações Gerais"):
                # Atualizar configurações
                config["app_name"] = app_name
                config["show_splash"] = show_splash
                config["auto_refresh"] = auto_refresh
                config["refresh_interval"] = refresh_interval

                # Salvar as configurações
                if save_config(config):
                    st.success("Configurações salvas com sucesso!")
                else:
                    st.error("Erro ao salvar configurações.")

    with tab2:
        st.header("Configurações do Banco de Dados")

        # Exibir informações sobre o banco de dados atual
        db_path = Database.get_db_path()
        st.markdown(f"**Caminho do Banco de Dados:** `{db_path}`")

        # Verificar se o arquivo existe
        if os.path.exists(db_path):
            db_size = os.path.getsize(db_path) / (1024 * 1024)  # Tamanho em MB
            st.markdown(f"**Tamanho do Banco de Dados:** {db_size:.2f} MB")

            # Listar tabelas
            tabelas = Database.get_table_names()
            st.markdown(f"**Número de Tabelas:** {len(tabelas)}")

            # Exibir tabelas em um expander
            with st.expander("Ver Tabelas"):
                for tabela in tabelas:
                    # Para cada tabela, exibir o número de registros
                    count = Database.execute_query(
                        f"SELECT COUNT(*) as count FROM {tabela}"
                    )
                    count_value = count[0]["count"] if count else 0
                    st.markdown(f"- **{tabela}**: {count_value} registros")
        else:
            st.error(
                f"O arquivo de banco de dados não existe no caminho especificado: {db_path}"
            )

        # Ações de manutenção do banco de dados
        st.subheader("Manutenção do Banco de Dados")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("📊 Otimizar Banco de Dados", use_container_width=True):
                # Executar otimização
                try:
                    success = Database.execute_write_query("VACUUM")
                    if success:
                        st.success("Banco de dados otimizado com sucesso!")
                    else:
                        st.error("Erro ao otimizar o banco de dados.")
                except Exception as e:
                    st.error(f"Erro: {e}")

        with col2:
            if st.button("🔄 Verificar Integridade", use_container_width=True):
                # Verificar integridade do banco
                try:
                    result = Database.execute_query("PRAGMA integrity_check")
                    if result and result[0].get("integrity_check") == "ok":
                        st.success(
                            "Verificação de integridade concluída: banco de dados íntegro!"
                        )
                    else:
                        st.error(
                            "Problemas de integridade detectados no banco de dados."
                        )
                except Exception as e:
                    st.error(f"Erro: {e}")

    with tab3:
        st.header("Aparência")

        with st.form("appearance_settings"):
            # Configurações de tema
            theme_config = config.get("theme", {})

            # Cores principais
            primary_color = st.color_picker(
                "Cor Primária", value=theme_config.get("primary_color", "#1E88E5")
            )

            secondary_color = st.color_picker(
                "Cor Secundária", value=theme_config.get("secondary_color", "#64B5F6")
            )

            accent_color = st.color_picker(
                "Cor de Destaque", value=theme_config.get("accent_color", "#FFC107")
            )

            # Opções de layout
            layout_options = ["wide", "centered"]
            layout = st.selectbox(
                "Layout Padrão",
                layout_options,
                index=(
                    layout_options.index(config.get("layout", "wide"))
                    if config.get("layout") in layout_options
                    else 0
                ),
            )

            # Opções de fonte
            font_options = ["Default", "Roboto", "Open Sans", "Lato", "Montserrat"]
            font = st.selectbox(
                "Fonte",
                font_options,
                index=(
                    font_options.index(theme_config.get("font", "Default"))
                    if theme_config.get("font") in font_options
                    else 0
                ),
            )

            # Botão para salvar configurações de aparência
            if st.form_submit_button("Salvar Configurações de Aparência"):
                # Atualizar configurações
                if "theme" not in config:
                    config["theme"] = {}

                config["theme"]["primary_color"] = primary_color
                config["theme"]["secondary_color"] = secondary_color
                config["theme"]["accent_color"] = accent_color
                config["theme"]["font"] = font
                config["layout"] = layout

                # Salvar as configurações
                if save_config(config):
                    st.success("Configurações de aparência salvas com sucesso!")
                    st.info(
                        "Algumas alterações podem exigir reiniciar a aplicação para terem efeito."
                    )
                else:
                    st.error("Erro ao salvar configurações de aparência.")

    with tab4:
        st.header("Informações do Sistema")

        # Versão da aplicação
        st.markdown(f"**Versão do GoNetwork AI Web:** {config.get('version', '1.0.0')}")

        # Diretórios importantes
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        web_dir = os.path.dirname(os.path.abspath(__file__))

        st.markdown(f"**Diretório Raiz:** `{base_dir}`")
        st.markdown(f"**Diretório Web:** `{web_dir}`")

        # Estatísticas do banco de dados
        if os.path.exists(Database.get_db_path()):
            st.subheader("Estatísticas do Banco de Dados")

            # Obter algumas estatísticas
            eventos_count = Database.execute_query(
                "SELECT COUNT(*) as count FROM events"
            )[0]["count"]
            clientes_count = Database.execute_query(
                "SELECT COUNT(*) as count FROM clients"
            )[0]["count"]
            equipe_count = Database.execute_query(
                "SELECT COUNT(*) as count FROM team_members"
            )[0]["count"]
            entregas_count = Database.execute_query(
                "SELECT COUNT(*) as count FROM deliverables"
            )[0]["count"]

            # Exibir estatísticas em colunas
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Eventos", eventos_count)

            with col2:
                st.metric("Clientes", clientes_count)

            with col3:
                st.metric("Equipe", equipe_count)

            with col4:
                st.metric("Entregas", entregas_count)

            # Mostrar gráfico simples de eventos por mês
            eventos_por_mes = Database.execute_query(
                """
                SELECT strftime('%Y-%m', date) as mes, COUNT(*) as total
                FROM events
                GROUP BY mes
                ORDER BY mes
            """
            )

            if eventos_por_mes:
                st.subheader("Eventos por Mês")

                df = pd.DataFrame(eventos_por_mes)
                df.rename(columns={"mes": "Mês", "total": "Eventos"}, inplace=True)

                st.bar_chart(df.set_index("Mês"))

        # Sobre a aplicação
        with st.expander("Sobre o GoNetwork AI Web"):
            st.markdown(
                """
            **GoNetwork AI Web** é a versão web do sistema de gerenciamento audiovisual de eventos GoNetwork AI.

            Esta versão utiliza o framework Streamlit para proporcionar uma interface web moderna e responsiva,
            mantendo todas as funcionalidades principais da versão desktop.

            © 2025 GoNetwork. Todos os direitos reservados.
            """
            )
