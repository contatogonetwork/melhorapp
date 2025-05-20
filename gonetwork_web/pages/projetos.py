from datetime import datetime

import pandas as pd
import streamlit as st
from components.project_card import show_project_card, show_team_assignment_section

from utils.database import Database
from utils.formatters import formatar_data_iso, formatar_status


def show():
    """Renderiza a página de projetos."""
    st.title("📽️ Projetos")

    # Verificar permissões
    is_admin = st.session_state.get("is_admin", False)
    can_edit = st.session_state.get("can_edit_projects", True)

    # Tabs para diferentes seções
    tab1, tab2, tab3 = st.tabs(
        ["📋 Visão Geral", "🔍 Detalhes do Projeto", "➕ Novo Projeto"]
    )

    # Tab 1: Visão geral dos projetos
    with tab1:
        show_projects_overview()

    # Tab 2: Detalhes de um projeto específico
    with tab2:
        # Buscar projeto selecionado ou da sessão
        selected_project_id = st.session_state.get("selected_project_id", None)

        if selected_project_id:
            show_project_details(selected_project_id, can_edit)
        else:
            st.info("Selecione um projeto na aba 'Visão Geral' para ver os detalhes.")

    # Tab 3: Formulário para criar novo projeto
    with tab3:
        if can_edit:
            new_project = show_project_card(project_id=None, view_only=False)

            # Se um novo projeto foi criado, atualizar sessão e mostrar detalhes
            if new_project:
                st.session_state.selected_project_id = new_project["id"]
                st.session_state.show_project_tab = "detalhes"
                st.rerun()
        else:
            st.warning("Você não tem permissão para criar novos projetos.")


def show_projects_overview():
    """Exibe a visão geral de todos os projetos."""

    # Filtros de busca
    st.subheader("Filtrar Projetos")

    col1, col2 = st.columns(2)
    with col1:
        search_term = st.text_input("Busca por nome:", "")

    with col2:
        # Filtro por cliente
        clients = Database.execute_query(
            "SELECT id, company FROM clients ORDER BY company"
        )

        client_options = {"": "Todos os Clientes"}
        if clients:
            client_options.update({c["id"]: c["company"] for c in clients})

        client_filter = st.selectbox(
            "Filtrar por cliente:",
            options=list(client_options.keys()),
            format_func=lambda c_id: client_options.get(c_id, ""),
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        # Filtro por status
        status_options = [
            "Todos",
            "planejamento",
            "em andamento",
            "concluído",
            "cancelado",
        ]
        status_filter = st.selectbox("Status:", status_options)

    with col2:
        # Ordenação
        sort_options = {
            "date_desc": "Data (mais recente)",
            "date_asc": "Data (mais antiga)",
            "name_asc": "Nome (A-Z)",
            "name_desc": "Nome (Z-A)",
        }
        sort_by = st.selectbox(
            "Ordenar por:",
            options=list(sort_options.keys()),
            format_func=lambda k: sort_options[k],
            index=0,
        )

    with col3:
        # Mostrar apenas os meus projetos
        my_projects = st.checkbox("Apenas meus projetos")

    # Montando a query com filtros
    query = """
    SELECT e.id, e.name, e.date, e.status, e.location, e.tags,
           c.company as client_name,
           (SELECT COUNT(*) FROM deliverables WHERE event_id = e.id) as deliverables_count,
           (SELECT COUNT(*) FROM event_team_members WHERE event_id = e.id) as team_count
    FROM events e
    LEFT JOIN clients c ON e.client_id = c.id
    WHERE 1=1
    """
    params = []

    # Aplicar filtros
    if search_term:
        query += " AND (e.name LIKE ? OR e.description LIKE ? OR e.tags LIKE ?)"
        search_param = f"%{search_term}%"
        params.extend([search_param, search_param, search_param])

    if client_filter:
        query += " AND e.client_id = ?"
        params.append(client_filter)

    if status_filter != "Todos":
        query += " AND e.status = ?"
        params.append(status_filter)

    if my_projects and st.session_state.get("user_id"):
        query += """
        AND e.id IN (
            SELECT DISTINCT event_id FROM event_team_members
            WHERE member_id = ?
        )
        """
        params.append(st.session_state.get("user_id"))

    # Aplicar ordenação
    if sort_by == "date_desc":
        query += " ORDER BY e.date DESC"
    elif sort_by == "date_asc":
        query += " ORDER BY e.date ASC"
    elif sort_by == "name_asc":
        query += " ORDER BY e.name ASC"
    elif sort_by == "name_desc":
        query += " ORDER BY e.name DESC"

    # Executar a query
    projects = Database.execute_query(query, params)

    if not projects:
        st.info("Nenhum projeto encontrado com os filtros aplicados.")
        return

    # Exibir projetos em cartões
    st.subheader(f"Projetos Encontrados: {len(projects)}")

    # Preparar dados para exibição em dataframe
    display_data = []
    for proj in projects:
        display_data.append(
            {
                "ID": proj["id"],
                "Nome": proj["name"],
                "Cliente": proj["client_name"] or "Não atribuído",
                "Data": formatar_data_iso(proj["date"]),
                "Status": formatar_status(proj["status"]),
                "Entregas": proj["deliverables_count"],
                "Equipe": proj["team_count"],
            }
        )

    # Criar DataFrame para exibição
    df = pd.DataFrame(display_data)

    # Usar DataEditor para mostrar os dados
    project_df = st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "ID": st.column_config.TextColumn("ID", width="small"),
            "Nome": st.column_config.TextColumn("Nome"),
            "Cliente": st.column_config.TextColumn("Cliente"),
            "Data": st.column_config.TextColumn("Data", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Entregas": st.column_config.NumberColumn("Entregas", width="small"),
            "Equipe": st.column_config.NumberColumn("Equipe", width="small"),
        },
    )

    # Seleção de projeto
    selected_proj_id = st.selectbox(
        "Selecione um projeto para ver detalhes:",
        options=[p["id"] for p in projects],
        format_func=lambda p_id: next(
            (p["name"] for p in projects if p["id"] == p_id), p_id
        ),
    )

    if selected_proj_id:
        st.session_state.selected_project_id = selected_proj_id

        # Botões para ações rápidas
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔍 Ver Detalhes", use_container_width=True):
                st.session_state.selected_project_id = selected_proj_id
                st.session_state.show_project_tab = "detalhes"
                st.rerun()

        with col2:
            if st.session_state.get("can_edit_projects", False):
                if st.button("✏️ Editar", use_container_width=True):
                    st.session_state.selected_project_id = selected_proj_id
                    st.session_state.edit_project_mode = True
                    st.session_state.show_project_tab = "detalhes"
                    st.rerun()

        with col3:
            if st.session_state.get("is_admin", False):
                if st.button("🗑️ Excluir", use_container_width=True):
                    st.session_state.confirm_delete_project = selected_proj_id
                    st.warning(
                        "Esta ação não pode ser desfeita. Deseja realmente excluir este projeto?"
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Confirmar", key="confirm_delete"):
                            # Verificar se há entregas associadas
                            deliverables = Database.execute_query(
                                "SELECT COUNT(*) as count FROM deliverables WHERE event_id = ?",
                                (selected_proj_id,),
                            )

                            if deliverables[0]["count"] > 0:
                                st.error(
                                    f"Este projeto tem {deliverables[0]['count']} entregas associadas. Exclua-as primeiro."
                                )
                            else:
                                # Excluir membros da equipe primeiro (restrições de chave estrangeira)
                                Database.execute_write_query(
                                    "DELETE FROM event_team_members WHERE event_id = ?",
                                    (selected_proj_id,),
                                )

                                # Excluir comentários
                                Database.execute_write_query(
                                    "DELETE FROM comments WHERE item_id = ? AND item_type = 'event'",
                                    (selected_proj_id,),
                                )

                                # Excluir o projeto
                                success = Database.execute_write_query(
                                    "DELETE FROM events WHERE id = ?",
                                    (selected_proj_id,),
                                )

                                if success:
                                    st.success("Projeto excluído com sucesso!")
                                    if "selected_project_id" in st.session_state:
                                        del st.session_state.selected_project_id
                                    st.rerun()
                                else:
                                    st.error("Erro ao excluir o projeto.")

                    with col2:
                        if st.button("❌ Cancelar", key="cancel_delete"):
                            if "confirm_delete_project" in st.session_state:
                                del st.session_state.confirm_delete_project
                            st.rerun()


def show_project_details(project_id, can_edit=True):
    """
    Exibe os detalhes completos de um projeto específico

    Args:
        project_id: ID do projeto
        can_edit: Se o usuário pode editar o projeto
    """
    project = Database.execute_query(
        """
        SELECT e.*, c.company as client_name
        FROM events e
        LEFT JOIN clients c ON e.client_id = c.id
        WHERE e.id = ?
        """,
        (project_id,),
    )

    if not project:
        st.error("Projeto não encontrado.")
        return

    project = project[0]

    # Mostrar opções de edição
    if can_edit:
        col1, col2 = st.columns([8, 2])
        with col1:
            st.title(project["name"])
        with col2:
            if st.button("✏️ Editar Projeto", use_container_width=True):
                st.session_state.edit_project_mode = True
                st.rerun()
    else:
        st.title(project["name"])

    # Se estiver em modo de edição, mostrar o formulário
    if st.session_state.get("edit_project_mode", False) and can_edit:
        updated_project = show_project_card(project_id=project_id, view_only=False)

        if updated_project:
            st.session_state.edit_project_mode = False
            # Recarregar dados do projeto
            st.rerun()

        # Botão para cancelar edição
        if st.button("Cancelar Edição"):
            st.session_state.edit_project_mode = False
            st.rerun()

        return

    # Mostrar detalhes do projeto
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Detalhes")
        st.text(f"Cliente: {project['client_name']}")
        st.text(f"Data: {formatar_data_iso(project['date'])}")
        st.text(f"Local: {project['location']}")
        st.text(f"Status: {formatar_status(project['status'])}")

        # Tags do projeto
        if project.get("tags"):
            st.markdown("**Tags:**")
            tags_html = " ".join(
                [
                    f"<span class='tag'>{tag.strip()}</span>"
                    for tag in project["tags"].split(",")
                ]
            )
            st.markdown(tags_html, unsafe_allow_html=True)

    with col2:
        # Estatísticas do projeto
        st.markdown("### Estatísticas")

        # Buscar contagens
        deliverables = Database.execute_query(
            "SELECT COUNT(*) as count FROM deliverables WHERE event_id = ?",
            (project_id,),
        )
        deliverable_count = deliverables[0]["count"] if deliverables else 0

        # Contar por status
        status_counts = Database.execute_query(
            """
            SELECT status, COUNT(*) as count
            FROM deliverables
            WHERE event_id = ?
            GROUP BY status
            """,
            (project_id,),
        )

        status_dict = (
            {s["status"]: s["count"] for s in status_counts} if status_counts else {}
        )

        # Calcular progresso
        completed = status_dict.get("concluído", 0) + status_dict.get("completed", 0)
        total = deliverable_count
        progress = (completed / total * 100) if total > 0 else 0

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Entregas", deliverable_count)
        with col2:
            st.metric("Concluídas", f"{completed} ({progress:.1f}%)")

        # Prazo mais próximo
        next_deadline = Database.execute_query(
            """
            SELECT deadline FROM deliverables
            WHERE event_id = ? AND status NOT IN ('concluído', 'completed')
            ORDER BY deadline ASC
            LIMIT 1
            """,
            (project_id,),
        )

        if next_deadline:
            st.info(f"Próximo prazo: {formatar_data_iso(next_deadline[0]['deadline'])}")

    # Descrição do projeto
    st.markdown("### Descrição")
    st.write(project.get("description", "Sem descrição disponível."))

    # Mostrar tabs para outras seções
    tab1, tab2, tab3 = st.tabs(["👥 Equipe", "📦 Entregas", "💬 Comentários"])

    # Tab Equipe
    with tab1:
        show_team_assignment_section(project_id)

    # Tab Entregas
    with tab2:
        show_deliverables_section(project_id, can_edit)

    # Tab Comentários
    with tab3:
        # Mostrar comentários
        from components.comments import show_comments_section

        show_comments_section(
            project_id,
            "event",
            can_edit=st.session_state.get("logged_in", False),
            is_admin=st.session_state.get("is_admin", False),
        )


def show_deliverables_section(project_id, can_edit=True):
    """
    Exibe a seção de entregas do projeto

    Args:
        project_id: ID do projeto
        can_edit: Se o usuário pode adicionar/editar entregas
    """
    st.subheader("📦 Entregas do Projeto")

    # Buscar entregas do projeto
    deliverables = Database.execute_query(
        """
        SELECT d.*, tm.name as responsible_name
        FROM deliverables d
        LEFT JOIN team_members tm ON d.responsible_id = tm.id
        WHERE d.event_id = ?
        ORDER BY d.deadline
        """,
        (project_id,),
    )

    if not deliverables:
        st.info("Nenhuma entrega cadastrada para este projeto.")
    else:
        # Preparar dados para exibição
        display_data = []
        for del_item in deliverables:
            display_data.append(
                {
                    "ID": del_item["id"],
                    "Título": del_item["title"],
                    "Prazo": formatar_data_iso(del_item["deadline"]),
                    "Status": formatar_status(del_item["status"]),
                    "Responsável": del_item["responsible_name"] or "Não atribuído",
                    "Progresso": f"{del_item['progress']}%",
                }
            )

        # Criar DataFrame para exibição
        df = pd.DataFrame(display_data)

        # Exibir tabela
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "ID": st.column_config.TextColumn("ID", width="small"),
                "Título": st.column_config.TextColumn("Título"),
                "Prazo": st.column_config.TextColumn("Prazo", width="medium"),
                "Status": st.column_config.TextColumn("Status", width="small"),
                "Responsável": st.column_config.TextColumn("Responsável"),
                "Progresso": st.column_config.ProgressColumn(
                    "Progresso", width="small"
                ),
            },
        )

    # Botão para adicionar nova entrega
    if can_edit:
        with st.expander("➕ Adicionar Nova Entrega", expanded=not deliverables):
            with st.form("add_deliverable"):
                title = st.text_input("Título*")

                col1, col2 = st.columns(2)
                with col1:
                    deadline = st.date_input(
                        "Prazo", value=datetime.now() + timedelta(days=7)
                    )
                with col2:
                    status_options = [
                        "não iniciado",
                        "em andamento",
                        "concluído",
                        "atrasado",
                        "aguardando",
                    ]
                    status = st.selectbox("Status", status_options, index=0)

                # Selecionar responsável
                team_members = Database.execute_query(
                    """
                    SELECT tm.id, tm.name, tm.role
                    FROM team_members tm
                    JOIN event_team_members etm ON tm.id = etm.member_id
                    WHERE etm.event_id = ?
                    ORDER BY tm.name
                    """,
                    (project_id,),
                )

                member_options = {"": "Selecione um responsável"}
                if team_members:
                    member_options.update(
                        {m["id"]: f"{m['name']} ({m['role']})" for m in team_members}
                    )

                responsible_id = st.selectbox(
                    "Responsável",
                    options=list(member_options.keys()),
                    format_func=lambda m_id: member_options.get(m_id, ""),
                )

                progress = st.slider("Progresso", 0, 100, 0, 5)
                description = st.text_area("Descrição")

                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button(
                        "Adicionar Entrega", use_container_width=True
                    )

                if submit:
                    if not title:
                        st.error("O título é obrigatório.")
                    else:
                        now = datetime.now().isoformat()
                        deadline_str = deadline.isoformat()

                        # Gerar ID para a entrega
                        deliverable_id = f"del_{int(datetime.now().timestamp())}"

                        # Inserir no banco de dados
                        success = Database.execute_write_query(
                            """
                            INSERT INTO deliverables
                            (id, event_id, title, description, deadline,
                            status, progress, responsible_id, created_at, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                deliverable_id,
                                project_id,
                                title,
                                description,
                                deadline_str,
                                status,
                                progress,
                                responsible_id or None,
                                now,
                                now,
                            ),
                        )

                        if success:
                            st.success("Entrega adicionada com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao adicionar entrega.")
