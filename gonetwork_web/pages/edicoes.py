import pandas as pd
import streamlit as st

from utils.database import Database
from utils.formatters import formatar_data_hora, truncar_texto


def show():
    """Renderiza a página de edições."""
    st.title("🎬 Edições")

    # Obter dados de edições
    # Adaptando a consulta para obter dados relevantes para edições de vídeo
    edicoes = Database.execute_query(
        """
        SELECT d.id, d.title, d.event_id, d.client_id, d.deadline, d.status,
               d.progress, d.created_at, d.updated_at,
               e.name as event_name, c.company as client_name
        FROM deliverables d
        LEFT JOIN events e ON d.event_id = e.id
        LEFT JOIN clients c ON d.client_id = c.id
        WHERE d.title LIKE '%vídeo%' OR d.title LIKE '%video%'
        ORDER BY d.deadline DESC
    """
    )

    # Obter responsáveis (editores)
    editores = Database.execute_query(
        """
        SELECT id, name, role FROM team_members
        WHERE role LIKE '%editor%' OR role LIKE '%vídeo%' OR role LIKE '%video%'
        ORDER BY name
    """
    )

    if not editores:
        # Se não encontrar editores específicos, usar todos os membros da equipe
        editores = Database.execute_query(
            "SELECT id, name, role FROM team_members ORDER BY name"
        )

    # Adicionar botão para criar nova edição
    if st.button("➕ Nova Edição", use_container_width=True):
        st.session_state.show_edicao_form = True

    # Exibir formulário se solicitado
    if "show_edicao_form" in st.session_state and st.session_state.show_edicao_form:
        show_edicao_form(editores)

    # Filtros
    st.subheader("Filtros")
    col1, col2 = st.columns(2)

    with col1:
        # Lista de status disponíveis
        todos_status = ["Todos"] + sorted(
            list(set([e.get("status", "") for e in edicoes if e.get("status")]))
        )
        status_selecionado = st.selectbox("Status:", todos_status)

    with col2:
        # Lista de clientes disponíveis
        todos_clientes = ["Todos"] + sorted(
            list(
                set([e.get("client_name", "") for e in edicoes if e.get("client_name")])
            )
        )
        cliente_selecionado = st.selectbox("Cliente:", todos_clientes)

    # Aplicar filtros
    edicoes_filtradas = edicoes
    if status_selecionado != "Todos":
        edicoes_filtradas = [
            e for e in edicoes_filtradas if e.get("status") == status_selecionado
        ]
    if cliente_selecionado != "Todos":
        edicoes_filtradas = [
            e for e in edicoes_filtradas if e.get("client_name") == cliente_selecionado
        ]

    # Exibir edições em formato adequado
    if not edicoes_filtradas:
        st.info("Nenhuma edição encontrada com os filtros selecionados.")
    else:
        # Personalizar exibição
        st.subheader(f"Edições ({len(edicoes_filtradas)})")

        # Usar cards para cada edição
        for i, edicao in enumerate(edicoes_filtradas):
            with st.expander(
                f"{edicao['title']} - {formatar_data_hora(edicao['deadline'])}"
            ):
                col1, col2 = st.columns([1, 3])

                with col1:
                    # Ícone representativo
                    st.image(
                        "https://img.icons8.com/color/96/000000/video-editing.png",
                        width=80,
                    )

                    # Status e progresso
                    st.markdown(f"**Status:** {edicao['status'].capitalize()}")
                    st.progress(float(edicao["progress"] or 0) / 100)
                    st.caption(f"Progresso: {edicao['progress'] or 0}%")

                with col2:
                    # Informações detalhadas
                    st.markdown(f"**Evento:** {edicao['event_name']}")
                    st.markdown(f"**Cliente:** {edicao['client_name']}")
                    st.markdown(f"**Prazo:** {formatar_data_hora(edicao['deadline'])}")
                    st.markdown(
                        f"**Criado em:** {formatar_data_hora(edicao['created_at'])}"
                    )
                    st.markdown(
                        f"**Atualizado em:** {formatar_data_hora(edicao['updated_at'])}"
                    )

                # Exibir responsáveis associados
                responsaveis = Database.execute_query(
                    """
                    SELECT tm.name, tm.role
                    FROM event_team_members etm
                    JOIN team_members tm ON etm.team_member_id = tm.id
                    WHERE etm.event_id = ?
                    AND tm.role LIKE '%editor%' OR tm.role LIKE '%vídeo%' OR tm.role LIKE '%video%'
                    ORDER BY tm.name
                """,
                    (edicao["event_id"],),
                )

                if responsaveis:
                    st.write("**Responsáveis:**")
                    for resp in responsaveis:
                        st.markdown(f"- {resp['name']} ({resp['role']})")

                # Botões de ação
                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button(
                        "✏️ Editar", key=f"edit_{edicao['id']}", use_container_width=True
                    ):
                        st.session_state.show_edicao_form = True
                        st.session_state.edit_edicao_id = edicao["id"]

                with col2:
                    if st.button(
                        "📊 Atualizar Progresso",
                        key=f"progress_{edicao['id']}",
                        use_container_width=True,
                    ):
                        st.session_state.update_progress = True
                        st.session_state.progress_edicao_id = edicao["id"]
                        st.session_state.current_progress = edicao["progress"] or 0

                with col3:
                    if st.button(
                        "🗑️ Excluir",
                        key=f"delete_{edicao['id']}",
                        use_container_width=True,
                    ):
                        if delete_edicao(edicao["id"]):
                            st.success("Edição excluída com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao excluir a edição.")

                # Formulário para atualizar o progresso
                if (
                    "update_progress" in st.session_state
                    and st.session_state.update_progress
                    and "progress_edicao_id" in st.session_state
                    and st.session_state.progress_edicao_id == edicao["id"]
                ):

                    with st.form(key=f"progress_form_{edicao['id']}"):
                        progress = st.slider(
                            "Progresso:", 0, 100, int(st.session_state.current_progress)
                        )

                        col1, col2 = st.columns(2)

                        with col1:
                            if st.form_submit_button(
                                "Salvar", use_container_width=True
                            ):
                                if update_edicao_progress(edicao["id"], progress):
                                    st.success("Progresso atualizado com sucesso!")
                                    st.session_state.update_progress = False
                                    st.session_state.progress_edicao_id = None
                                    st.rerun()
                                else:
                                    st.error("Erro ao atualizar o progresso.")

                        with col2:
                            if st.form_submit_button(
                                "Cancelar", use_container_width=True
                            ):
                                st.session_state.update_progress = False
                                st.session_state.progress_edicao_id = None
                                st.rerun()


def show_edicao_form(editores):
    """Exibe o formulário para criar ou editar uma edição."""
    edit_mode = "edit_edicao_id" in st.session_state and st.session_state.edit_edicao_id

    # Buscar dados da edição existente se estiver no modo de edição
    edicao_data = {}
    if edit_mode:
        edicao = Database.execute_query(
            "SELECT * FROM deliverables WHERE id = ?",
            (st.session_state.edit_edicao_id,),
        )
        if edicao:
            edicao_data = edicao[0]

    st.subheader(f"{'Editar' if edit_mode else 'Nova'} Edição")

    with st.form("edicao_form"):
        # Buscar eventos e clientes para os selects
        eventos = Database.execute_query(
            "SELECT id, name FROM events ORDER BY date DESC"
        )
        clientes = Database.execute_query(
            "SELECT id, company FROM clients ORDER BY company"
        )

        # Título da edição
        titulo = st.text_input(
            "Título do Vídeo", value=edicao_data.get("title", "") if edit_mode else ""
        )

        col1, col2 = st.columns(2)

        with col1:
            evento_id = st.selectbox(
                "Evento",
                [e["id"] for e in eventos],
                index=(
                    next(
                        (
                            i
                            for i, e in enumerate(eventos)
                            if e["id"] == edicao_data.get("event_id")
                        ),
                        0,
                    )
                    if edit_mode and edicao_data.get("event_id")
                    else 0
                ),
                format_func=lambda id: next(
                    (e["name"] for e in eventos if e["id"] == id), id
                ),
            )

        with col2:
            cliente_id = st.selectbox(
                "Cliente",
                [c["id"] for c in clientes],
                index=(
                    next(
                        (
                            i
                            for i, c in enumerate(clientes)
                            if c["id"] == edicao_data.get("client_id")
                        ),
                        0,
                    )
                    if edit_mode and edicao_data.get("client_id")
                    else 0
                ),
                format_func=lambda id: next(
                    (c["company"] for c in clientes if c["id"] == id), id
                ),
            )

        col1, col2 = st.columns(2)

        with col1:
            data_prazo = st.date_input(
                "Prazo de Entrega",
                value=(
                    pd.to_datetime(edicao_data.get("deadline")).date()
                    if edit_mode and edicao_data.get("deadline")
                    else None
                ),
            )

        with col2:
            status = st.selectbox(
                "Status",
                ["pendente", "em andamento", "concluído", "atrasado"],
                index=(
                    ["pendente", "em andamento", "concluído", "atrasado"].index(
                        edicao_data.get("status", "pendente")
                    )
                    if edit_mode and edicao_data.get("status")
                    else 0
                ),
            )

        progress = st.slider(
            "Progresso (%)",
            0,
            100,
            value=int(edicao_data.get("progress", 0)) if edit_mode else 0,
        )

        # Botões de ação
        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("Salvar")

        with col2:
            if st.form_submit_button("Cancelar"):
                st.session_state.show_edicao_form = False
                if "edit_edicao_id" in st.session_state:
                    st.session_state.edit_edicao_id = None
                st.rerun()

        # Processar o formulário
        if submit:
            # Preparar os dados para inserção ou atualização
            prazo_str = data_prazo.isoformat() if data_prazo else None

            if edit_mode:
                # Atualizar edição existente
                success = Database.execute_write_query(
                    """
                    UPDATE deliverables
                    SET title = ?, event_id = ?, client_id = ?, deadline = ?,
                        status = ?, progress = ?, updated_at = datetime('now')
                    WHERE id = ?
                    """,
                    (
                        titulo,
                        evento_id,
                        cliente_id,
                        prazo_str,
                        status,
                        progress,
                        st.session_state.edit_edicao_id,
                    ),
                )

                if success:
                    st.success("Edição atualizada com sucesso!")
                    st.session_state.show_edicao_form = False
                    st.session_state.edit_edicao_id = None
                    st.rerun()
                else:
                    st.error("Erro ao atualizar a edição.")
            else:
                # Criar nova edição
                success = Database.execute_write_query(
                    """
                    INSERT INTO deliverables (title, event_id, client_id, deadline, status, progress, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                    """,
                    (titulo, evento_id, cliente_id, prazo_str, status, progress),
                )

                if success:
                    st.success("Edição criada com sucesso!")
                    st.session_state.show_edicao_form = False
                    st.rerun()
                else:
                    st.error("Erro ao criar a edição.")


def delete_edicao(edicao_id):
    """Exclui uma edição do banco de dados."""
    return Database.execute_write_query(
        "DELETE FROM deliverables WHERE id = ?", (edicao_id,)
    )


def update_edicao_progress(edicao_id, progress):
    """Atualiza o progresso de uma edição."""
    return Database.execute_write_query(
        """
        UPDATE deliverables
        SET progress = ?, updated_at = datetime('now')
        WHERE id = ?
        """,
        (progress, edicao_id),
    )
