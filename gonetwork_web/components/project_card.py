from datetime import datetime

import pandas as pd
import streamlit as st
from components.comments import show_comments_section

from utils.database import Database
from utils.formatters import formatar_data_iso, formatar_status


def show_project_card(project_id=None, view_only=False):
    """
    Exibe um cartão de projeto com todas as informações relacionadas

    Args:
        project_id: ID do projeto para exibir (None para criar novo)
        view_only: Se True, os campos não serão editáveis

    Returns:
        dict: Dados do projeto ou None
    """
    edit_mode = project_id is not None
    is_admin = st.session_state.get("is_admin", False)

    # Carregar dados do projeto se for edição
    project_data = {}
    client_name = ""
    if edit_mode:
        # Buscar dados do projeto
        result = Database.execute_query(
            """
            SELECT e.*, c.company as client_name
            FROM events e
            LEFT JOIN clients c ON e.client_id = c.id
            WHERE e.id = ?
            """,
            (project_id,),
        )

        if result:
            project_data = result[0]
            client_name = project_data.get("client_name", "")

    # Container para o cartão do projeto
    with st.container():
        # Cabeçalho do cartão
        if edit_mode:
            st.subheader(f"📽️ {project_data.get('name', 'Projeto sem nome')}")
            st.caption(f"Cliente: {client_name}")
        else:
            st.subheader("📽️ Novo Projeto")

        # Informações básicas do projeto
        col1, col2 = st.columns(2)

        with col1:
            # Informações do evento
            st.markdown("### Informações Básicas")
            st.text(f"Data: {formatar_data_iso(project_data.get('date', ''))}")
            st.text(f"Local: {project_data.get('location', '')}")
            st.text(f"Status: {formatar_status(project_data.get('status', ''))}")

            # Tags do projeto
            if "tags" in project_data and project_data["tags"]:
                tags = project_data["tags"].split(",")
                st.markdown("**Tags:**")
                for tag in tags:
                    st.caption(f"#{tag.strip()}")

        with col2:
            # Estatísticas do projeto
            st.markdown("### Estatísticas")

            # Buscar contagens relacionadas
            if edit_mode:
                # Contar entregas
                deliverables = Database.execute_query(
                    "SELECT COUNT(*) as count FROM deliverables WHERE event_id = ?",
                    (project_id,),
                )
                deliverable_count = deliverables[0]["count"] if deliverables else 0

                # Contar membros da equipe
                members = Database.execute_query(
                    "SELECT COUNT(*) as count FROM event_team_members WHERE event_id = ?",
                    (project_id,),
                )
                member_count = members[0]["count"] if members else 0

                # Contar comentários
                comments = Database.execute_query(
                    "SELECT COUNT(*) as count FROM comments WHERE item_id = ? AND item_type = 'event'",
                    (project_id,),
                )
                comment_count = comments[0]["count"] if comments else 0

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Entregas", deliverable_count)
                with col2:
                    st.metric("Equipe", member_count)
                with col3:
                    st.metric("Comentários", comment_count)

    # Se for apenas visualização, mostrar descrição e não o formulário de edição
    if view_only:
        st.markdown("### Descrição")
        st.write(project_data.get("description", "Sem descrição disponível."))

        # Mostrar seção de comentários se estiver no modo de visualização
        if edit_mode:
            show_comments_section(
                project_id,
                "event",
                can_edit=st.session_state.get("logged_in", False),
                is_admin=st.session_state.get("is_admin", False),
            )

        return project_data

    # Formulário de edição de projeto
    with st.form("project_form"):
        st.markdown("### Editar Projeto")

        # Campos do formulário
        name = st.text_input(
            "Nome do Projeto/Evento*", value=project_data.get("name", "")
        )

        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input(
                "Data",
                value=(
                    datetime.fromisoformat(
                        project_data.get("date", datetime.now().isoformat())
                    )
                    if project_data.get("date")
                    else datetime.now()
                ),
            )
        with col2:
            location = st.text_input("Local", value=project_data.get("location", ""))

        # Seleção de cliente
        clients = Database.execute_query(
            "SELECT id, company FROM clients ORDER BY company"
        )
        client_options = {c["id"]: c["company"] for c in clients} if clients else {}
        client_list = list(client_options.keys())

        selected_index = 0
        if edit_mode and project_data.get("client_id"):
            if project_data["client_id"] in client_list:
                selected_index = client_list.index(project_data["client_id"])

        client_id = st.selectbox(
            "Cliente*",
            options=client_list,
            format_func=lambda c_id: client_options.get(c_id, ""),
            index=selected_index,
        )

        # Status do projeto
        status_options = ["planejamento", "em andamento", "concluído", "cancelado"]
        current_status = project_data.get("status", "planejamento")
        if current_status not in status_options:
            status_options.append(current_status)

        status = st.selectbox(
            "Status", options=status_options, index=status_options.index(current_status)
        )

        # Tags do projeto
        tags = st.text_input(
            "Tags (separadas por vírgula)", value=project_data.get("tags", "")
        )

        # Descrição do projeto
        description = st.text_area(
            "Descrição", value=project_data.get("description", ""), height=150
        )

        # Botões de controle
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Salvar Projeto")
        with col2:
            cancel = st.form_submit_button("Cancelar")

        if cancel:
            return None

        if submit:
            # Validar campos obrigatórios
            if not name or not client_id:
                st.error("Os campos marcados com * são obrigatórios.")
                return None

            # Preparar dados para salvar
            now = datetime.now().isoformat()
            date_str = date.isoformat()

            updated_data = {
                "name": name,
                "date": date_str,
                "location": location,
                "client_id": client_id,
                "status": status,
                "tags": tags,
                "description": description,
            }

            # Salvar no banco
            if edit_mode:
                # Atualizar projeto existente
                query = """
                UPDATE events
                SET name = ?, date = ?, location = ?, client_id = ?,
                    status = ?, tags = ?, description = ?, updated_at = ?
                WHERE id = ?
                """
                params = (
                    updated_data["name"],
                    updated_data["date"],
                    updated_data["location"],
                    updated_data["client_id"],
                    updated_data["status"],
                    updated_data["tags"],
                    updated_data["description"],
                    now,
                    project_id,
                )
            else:
                # Criar novo projeto
                project_id = f"proj_{int(datetime.now().timestamp())}"
                query = """
                INSERT INTO events (id, name, date, location, client_id,
                                   status, tags, description, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (
                    project_id,
                    updated_data["name"],
                    updated_data["date"],
                    updated_data["location"],
                    updated_data["client_id"],
                    updated_data["status"],
                    updated_data["tags"],
                    updated_data["description"],
                    now,
                    now,
                )

            success = Database.execute_write_query(query, params)

            if success:
                st.success(
                    f"Projeto '{name}' {'atualizado' if edit_mode else 'criado'} com sucesso!"
                )
                updated_data["id"] = project_id
                # Atualiza os dados em session_state para projetos recém-criados
                if not edit_mode:
                    st.session_state.new_project_id = project_id
                return updated_data
            else:
                st.error(f"Erro ao {'atualizar' if edit_mode else 'criar'} projeto.")
                return None

    return None


def show_team_assignment_section(project_id):
    """
    Exibe seção para atribuir membros da equipe ao projeto

    Args:
        project_id: ID do projeto
    """
    st.subheader("👥 Membros da Equipe")

    # Buscar membros atuais do projeto
    current_members = Database.execute_query(
        """
        SELECT etm.*, tm.name, tm.role
        FROM event_team_members etm
        JOIN team_members tm ON etm.member_id = tm.id
        WHERE etm.event_id = ?
        """,
        (project_id,),
    )

    # Exibir membros atuais
    if current_members:
        member_df = pd.DataFrame(
            [
                {
                    "Nome": m["name"],
                    "Função": m["role"],
                    "Papel no Projeto": m["project_role"],
                }
                for m in current_members
            ]
        )

        st.dataframe(member_df, hide_index=True, use_container_width=True)
    else:
        st.info("Nenhum membro atribuído a este projeto.")

    # Buscar todos os membros da equipe para seleção
    all_members = Database.execute_query(
        "SELECT id, name, role FROM team_members ORDER BY name"
    )

    # Formulário para adicionar membro
    with st.expander("➕ Adicionar Membro à Equipe", expanded=not current_members):
        member_options = {m["id"]: f"{m['name']} ({m['role']})" for m in all_members}

        with st.form("add_team_member"):
            member_id = st.selectbox(
                "Membro",
                options=list(member_options.keys()),
                format_func=lambda m_id: member_options.get(m_id, ""),
            )

            project_role = st.text_input(
                "Papel no Projeto", placeholder="Ex: Diretor, Operador, etc."
            )

            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Adicionar", use_container_width=True)
            with col2:
                pass

            if submit:
                if not project_role:
                    st.error("Por favor, especifique o papel no projeto.")
                else:
                    # Verificar se o membro já está atribuído
                    exists = any(m["member_id"] == member_id for m in current_members)

                    if exists:
                        st.warning("Este membro já está atribuído a este projeto.")
                    else:
                        # Adicionar membro ao projeto
                        now = datetime.now().isoformat()
                        success = Database.execute_write_query(
                            """
                            INSERT INTO event_team_members
                            (event_id, member_id, project_role, created_at)
                            VALUES (?, ?, ?, ?)
                            """,
                            (project_id, member_id, project_role, now),
                        )

                        if success:
                            st.success("Membro adicionado à equipe do projeto!")
                            st.rerun()
                        else:
                            st.error("Erro ao adicionar membro à equipe.")
