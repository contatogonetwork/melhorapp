import pandas as pd
import streamlit as st

from utils.database import Database
from utils.formatters import formatar_data_hora, truncar_texto


def show():
    """Renderiza a página de briefings."""
    st.title("📋 Briefings")

    # Obter dados dos briefings
    briefings = Database.execute_query(
        """
        SELECT b.id, b.project_name, e.name as event_name, b.delivery_date,
               c.company as client_name, tm.name as team_lead
        FROM briefings b
        LEFT JOIN events e ON b.event_id = e.id
        LEFT JOIN clients c ON b.client_id = c.id
        LEFT JOIN team_members tm ON b.team_lead_id = tm.id
        ORDER BY b.delivery_date DESC
    """
    )

    # Filtros
    col1, col2 = st.columns(2)

    with col1:
        # Filtro de cliente
        clientes = ["Todos"] + sorted(
            list(set([b["client_name"] for b in briefings if b["client_name"]]))
        )
        cliente_selecionado = st.selectbox("Filtrar por cliente:", clientes)

    with col2:
        # Filtro de equipe
        equipes = ["Todos"] + sorted(
            list(set([b["team_lead"] for b in briefings if b["team_lead"]]))
        )
        equipe_selecionada = st.selectbox("Filtrar por responsável:", equipes)

    # Aplicar filtros
    briefings_filtrados = briefings
    if cliente_selecionado != "Todos":
        briefings_filtrados = [
            b for b in briefings_filtrados if b["client_name"] == cliente_selecionado
        ]
    if equipe_selecionada != "Todos":
        briefings_filtrados = [
            b for b in briefings_filtrados if b["team_lead"] == equipe_selecionada
        ]

    # Exibir briefings
    if not briefings_filtrados:
        st.info("Nenhum briefing encontrado com os filtros selecionados.")
    else:
        # Adicionar botão para criar novo briefing
        if st.button("➕ Novo Briefing", use_container_width=True):
            st.session_state.show_form = True

        # Mostrar formulário se solicitado
        if "show_form" in st.session_state and st.session_state.show_form:
            show_briefing_form()

        # Lista de briefings
        st.subheader(f"Briefings ({len(briefings_filtrados)})")

        # Converter para dataframe para exibição
        df_briefings = pd.DataFrame(briefings_filtrados)
        df_briefings["delivery_date"] = df_briefings["delivery_date"].apply(
            formatar_data_hora
        )

        # Renomear colunas para exibição
        df_display = df_briefings.rename(
            columns={
                "project_name": "Projeto",
                "event_name": "Evento",
                "delivery_date": "Data de Entrega",
                "client_name": "Cliente",
                "team_lead": "Responsável",
            }
        )

        # Remover coluna id da exibição
        if "id" in df_display.columns:
            df_display = df_display.drop(columns=["id"])

        # Exibir dataframe
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        # Selecionar briefing para detalhes
        st.subheader("Detalhes do Briefing")
        briefing_ids = [b["id"] for b in briefings_filtrados]
        briefing_names = [
            f"{b['project_name']} - {b['event_name']}" for b in briefings_filtrados
        ]

        if briefing_ids:
            selected_index = st.selectbox(
                "Selecione um briefing para ver detalhes:",
                range(len(briefing_ids)),
                format_func=lambda i: briefing_names[i],
            )

            selected_id = briefing_ids[selected_index]

            # Obter detalhes completos do briefing selecionado
            briefing_detalhes = Database.execute_query(
                """
                SELECT b.*, e.name as event_name, c.company as client_name,
                       tm.name as team_lead_name, e.date as event_date,
                       e.location as event_location
                FROM briefings b
                LEFT JOIN events e ON b.event_id = e.id
                LEFT JOIN clients c ON b.client_id = c.id
                LEFT JOIN team_members tm ON b.team_lead_id = tm.id
                WHERE b.id = ?
            """,
                (selected_id,),
            )

            if briefing_detalhes:
                show_briefing_details(briefing_detalhes[0])


def show_briefing_form():
    """Exibe o formulário para criar um novo briefing."""
    st.subheader("Novo Briefing")

    with st.form("briefing_form"):
        # Obter eventos e clientes para os seletores
        eventos = Database.execute_query(
            "SELECT id, name FROM events ORDER BY date DESC"
        )
        clientes = Database.execute_query(
            "SELECT id, company FROM clients ORDER BY company"
        )
        responsaveis = Database.execute_query(
            "SELECT id, name FROM team_members ORDER BY name"
        )

        # Formulário
        nome_projeto = st.text_input("Nome do Projeto")

        col1, col2 = st.columns(2)

        with col1:
            evento_id = st.selectbox(
                "Evento",
                [e["id"] for e in eventos],
                format_func=lambda id: next(
                    (e["name"] for e in eventos if e["id"] == id), id
                ),
            )

        with col2:
            cliente_id = st.selectbox(
                "Cliente",
                [c["id"] for c in clientes],
                format_func=lambda id: next(
                    (c["company"] for c in clientes if c["id"] == id), id
                ),
            )

        col1, col2 = st.columns(2)

        with col1:
            data_entrega = st.date_input("Data de Entrega")

        with col2:
            responsavel_id = st.selectbox(
                "Responsável",
                [r["id"] for r in responsaveis],
                format_func=lambda id: next(
                    (r["name"] for r in responsaveis if r["id"] == id), id
                ),
            )

        conteudo = st.text_area("Conteúdo do Briefing", height=200)

        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("Salvar")

        with col2:
            if st.form_submit_button("Cancelar"):
                st.session_state.show_form = False
                st.rerun()

        if submit:
            # Inserir no banco de dados
            success = Database.execute_write_query(
                """
                INSERT INTO briefings (project_name, event_id, client_id, delivery_date, team_lead_id, content, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                """,
                (
                    nome_projeto,
                    evento_id,
                    cliente_id,
                    data_entrega.isoformat(),
                    responsavel_id,
                    conteudo,
                ),
            )

            if success:
                st.success("Briefing criado com sucesso!")
                st.session_state.show_form = False
                st.rerun()
            else:
                st.error("Erro ao criar briefing.")


def show_briefing_details(briefing):
    """Exibe os detalhes de um briefing selecionado."""
    # Criar abas para diferentes seções de informação
    tab1, tab2, tab3 = st.tabs(["Informações Básicas", "Conteúdo", "Timeline"])

    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Projeto:** {briefing['project_name']}")
            st.markdown(f"**Evento:** {briefing['event_name']}")
            st.markdown(f"**Local:** {briefing['event_location']}")

        with col2:
            st.markdown(f"**Cliente:** {briefing['client_name']}")
            st.markdown(
                f"**Data do Evento:** {formatar_data_hora(briefing['event_date'])}"
            )
            st.markdown(
                f"**Data de Entrega:** {formatar_data_hora(briefing['delivery_date'])}"
            )

        st.markdown(f"**Responsável:** {briefing['team_lead_name']}")

        # Verificar se existem patrocinadores associados
        patrocinadores = Database.execute_query(
            """
            SELECT s.name, s.logo_path, s.contact_name, s.contact_email
            FROM sponsors s
            WHERE s.briefing_id = ?
        """,
            (briefing["id"],),
        )

        if patrocinadores:
            st.subheader("Patrocinadores")
            for p in patrocinadores:
                st.markdown(f"- **{p['name']}** (Contato: {p['contact_name']})")

    with tab2:
        if briefing["content"]:
            st.markdown(briefing["content"])
        else:
            st.info("Nenhum conteúdo detalhado disponível para este briefing.")

    with tab3:
        # Obter itens de timeline relacionados a este evento
        timeline_items = Database.execute_query(
            """
            SELECT ti.title, ti.start_time, ti.end_time, ti.status,
                   tm.name as responsible_name
            FROM timeline_items ti
            LEFT JOIN team_members tm ON ti.responsible_id = tm.id
            WHERE ti.event_id = ?
            ORDER BY ti.start_time
        """,
            (briefing["event_id"],),
        )

        if timeline_items:
            # Converter para dataframe
            df_timeline = pd.DataFrame(timeline_items)
            df_timeline["start_time"] = df_timeline["start_time"].apply(
                formatar_data_hora
            )
            df_timeline["end_time"] = df_timeline["end_time"].apply(formatar_data_hora)

            # Renomear colunas
            df_timeline = df_timeline.rename(
                columns={
                    "title": "Título",
                    "start_time": "Início",
                    "end_time": "Fim",
                    "status": "Status",
                    "responsible_name": "Responsável",
                }
            )

            st.dataframe(df_timeline, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum item de timeline associado a este evento.")
