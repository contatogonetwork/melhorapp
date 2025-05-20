from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.database import Database
from utils.formatters import calcular_duracao, formatar_data_hora, formatar_status


def show():
    """Renderiza a página da timeline."""
    st.title("🗓️ Timeline")

    # Obter lista de eventos
    eventos = Database.execute_query("SELECT id, name FROM events ORDER BY date DESC")

    if not eventos:
        st.info("Nenhum evento encontrado. Por favor, crie eventos primeiro.")
        return

    # Selecionar evento
    evento_selecionado = st.selectbox(
        "Selecione um evento:",
        [e["id"] for e in eventos],
        format_func=lambda id: next((e["name"] for e in eventos if e["id"] == id), id),
    )

    # Buscar detalhes do evento
    evento = Database.execute_query(
        "SELECT * FROM events WHERE id = ?", (evento_selecionado,)
    )

    if not evento:
        st.error("Evento não encontrado.")
        return

    evento = evento[0]

    # Exibir informações do evento
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"**Evento:** {evento['name']}")
    with col2:
        st.markdown(f"**Data:** {formatar_data_hora(evento['date'])}")
    with col3:
        st.markdown(f"**Local:** {evento['location']}")

    # Obter itens da timeline para o evento selecionado
    timeline_items = Database.execute_query(
        """
        SELECT ti.id, ti.title, ti.description, ti.start_time, ti.end_time,
               ti.status, ti.priority, ti.task_type, tm.name as responsible
        FROM timeline_items ti
        LEFT JOIN team_members tm ON ti.responsible_id = tm.id
        WHERE ti.event_id = ?
        ORDER BY ti.start_time
    """,
        (evento_selecionado,),
    )

    # Verificar se há itens na timeline
    if not timeline_items:
        st.info("Nenhum item de timeline encontrado para este evento.")

        # Adicionar botão para criar novo item
        if st.button("➕ Adicionar Item à Timeline", use_container_width=True):
            st.session_state.show_timeline_form = True
            st.session_state.edit_item_id = None
    else:
        # Adicionar botões de ação
        col1, col2 = st.columns(2)

        with col1:
            if st.button("➕ Novo Item", use_container_width=True):
                st.session_state.show_timeline_form = True
                st.session_state.edit_item_id = None

        with col2:
            if st.button("📊 Exportar Relatório", use_container_width=True):
                # Implementar exportação de relatório aqui
                st.info("Funcionalidade de exportação em desenvolvimento.")

        # Exibir timeline em diferentes formatos
        tab1, tab2, tab3 = st.tabs(["Visualização Gráfica", "Lista", "Calendário"])

        with tab1:
            # Converter para dataframe para plotagem
            df = pd.DataFrame(timeline_items)

            # Converter strings de data para objetos datetime
            df["start_time"] = pd.to_datetime(df["start_time"])
            df["end_time"] = pd.to_datetime(df["end_time"])

            # Calcular duração
            df["duration"] = df.apply(
                lambda row: calcular_duracao(row["start_time"], row["end_time"]), axis=1
            )

            # Adicionar formatação de status
            df["status_fmt"] = df["status"].apply(formatar_status)

            # Criar gráfico de Gantt
            fig = px.timeline(
                df,
                x_start="start_time",
                x_end="end_time",
                y="title",
                color="status_fmt",
                hover_name="description",
                hover_data={
                    "start_time": False,  # remove das informações de hover
                    "end_time": False,  # remove das informações de hover
                    "responsible": True,  # adiciona ao hover
                    "duration": True,  # adiciona ao hover
                    "status_fmt": False,  # remove das informações de hover
                },
                title="Cronograma do Evento",
            )

            # Personalizar layout
            fig.update_layout(
                xaxis_title="Data/Hora", yaxis_title="Atividade", height=500
            )

            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            # Exibir em formato de tabela
            df_display = pd.DataFrame(timeline_items)
            df_display["start_time"] = df_display["start_time"].apply(
                formatar_data_hora
            )
            df_display["end_time"] = df_display["end_time"].apply(formatar_data_hora)
            df_display["status"] = df_display["status"].apply(formatar_status)

            # Renomear colunas para exibição
            df_display = df_display.rename(
                columns={
                    "title": "Título",
                    "start_time": "Início",
                    "end_time": "Fim",
                    "status": "Status",
                    "priority": "Prioridade",
                    "task_type": "Tipo",
                    "responsible": "Responsável",
                }
            )

            # Remover colunas desnecessárias para a exibição
            columns_to_display = [
                "Título",
                "Início",
                "Fim",
                "Responsável",
                "Status",
                "Prioridade",
            ]
            df_display = df_display[columns_to_display]

            # Exibir tabela
            st.dataframe(df_display, use_container_width=True, hide_index=True)

            # Permitir seleção de um item para visualização/edição
            st.subheader("Detalhes do Item")

            item_id = st.selectbox(
                "Selecione um item para ver detalhes:",
                [i["id"] for i in timeline_items],
                format_func=lambda id: next(
                    (i["title"] for i in timeline_items if i["id"] == id), id
                ),
            )

            # Obter detalhes do item selecionado
            item_selecionado = next(
                (i for i in timeline_items if i["id"] == item_id), None
            )

            if item_selecionado:
                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(f"**Título:** {item_selecionado['title']}")
                    st.markdown(
                        f"**Início:** {formatar_data_hora(item_selecionado['start_time'])}"
                    )
                    st.markdown(
                        f"**Fim:** {formatar_data_hora(item_selecionado['end_time'])}"
                    )
                    st.markdown(f"**Responsável:** {item_selecionado['responsible']}")

                with col2:
                    st.markdown(
                        f"**Status:** {formatar_status(item_selecionado['status'])}"
                    )
                    st.markdown(f"**Prioridade:** {item_selecionado['priority']}")
                    st.markdown(f"**Tipo:** {item_selecionado['task_type']}")

                st.subheader("Descrição")
                st.markdown(
                    item_selecionado["description"]
                    if item_selecionado["description"]
                    else "Sem descrição"
                )

                # Botões de ação
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "✏️ Editar", key="edit_button", use_container_width=True
                    ):
                        st.session_state.show_timeline_form = True
                        st.session_state.edit_item_id = item_id

                with col2:
                    if st.button(
                        "🗑️ Excluir", key="delete_button", use_container_width=True
                    ):
                        if delete_timeline_item(item_id):
                            st.success("Item excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao excluir o item.")

        with tab3:
            st.info(
                "Visualização de calendário em desenvolvimento. Use a visualização gráfica ou de lista por enquanto."
            )

    # Exibir formulário para criação/edição de itens da timeline
    if "show_timeline_form" in st.session_state and st.session_state.show_timeline_form:
        edit_mode = (
            "edit_item_id" in st.session_state
            and st.session_state.edit_item_id is not None
        )

        st.divider()
        st.subheader(f"{'Editar' if edit_mode else 'Novo'} Item da Timeline")

        # Se estiver no modo de edição, carregar os dados do item
        item_data = {}
        if edit_mode:
            item_data = next(
                (i for i in timeline_items if i["id"] == st.session_state.edit_item_id),
                {},
            )

        show_timeline_item_form(evento_selecionado, item_data)


def show_timeline_item_form(evento_id, item_data=None):
    """Exibe o formulário para criar/editar um item da timeline."""
    edit_mode = bool(item_data)

    # Obter lista de responsáveis
    responsaveis = Database.execute_query(
        "SELECT id, name FROM team_members ORDER BY name"
    )

    with st.form("timeline_item_form"):
        # Campos do formulário
        titulo = st.text_input(
            "Título", value=item_data.get("title", "") if edit_mode else ""
        )

        col1, col2 = st.columns(2)

        with col1:
            data_inicio = st.datetime_input(
                "Data/Hora de Início",
                value=(
                    pd.to_datetime(item_data.get("start_time"))
                    if edit_mode and item_data.get("start_time")
                    else datetime.now()
                ),
            )

        with col2:
            data_fim = st.datetime_input(
                "Data/Hora de Término",
                value=(
                    pd.to_datetime(item_data.get("end_time"))
                    if edit_mode and item_data.get("end_time")
                    else datetime.now() + timedelta(hours=1)
                ),
            )

        col1, col2 = st.columns(2)

        with col1:
            status = st.selectbox(
                "Status",
                ["pendente", "em_andamento", "concluido", "atrasado", "cancelado"],
                index=(
                    [
                        "pendente",
                        "em_andamento",
                        "concluido",
                        "atrasado",
                        "cancelado",
                    ].index(item_data.get("status", "pendente"))
                    if edit_mode and item_data.get("status")
                    else 0
                ),
            )

        with col2:
            responsavel_id = st.selectbox(
                "Responsável",
                [r["id"] for r in responsaveis],
                index=(
                    next(
                        (
                            i
                            for i, r in enumerate(responsaveis)
                            if r["id"] == item_data.get("responsible_id")
                        ),
                        0,
                    )
                    if edit_mode and item_data.get("responsible_id")
                    else 0
                ),
                format_func=lambda id: next(
                    (r["name"] for r in responsaveis if r["id"] == id), id
                ),
            )

        col1, col2 = st.columns(2)

        with col1:
            prioridade = st.selectbox(
                "Prioridade",
                ["baixa", "média", "alta"],
                index=(
                    ["baixa", "média", "alta"].index(item_data.get("priority", "média"))
                    if edit_mode and item_data.get("priority")
                    else 1
                ),
            )

        with col2:
            tipo = st.selectbox(
                "Tipo",
                ["tarefa", "reunião", "entrega", "evento"],
                index=(
                    ["tarefa", "reunião", "entrega", "evento"].index(
                        item_data.get("task_type", "tarefa")
                    )
                    if edit_mode and item_data.get("task_type")
                    else 0
                ),
            )

        descricao = st.text_area(
            "Descrição", value=item_data.get("description", "") if edit_mode else ""
        )

        # Botões de ação
        col1, col2 = st.columns(2)

        with col1:
            submit = st.form_submit_button("Salvar")

        with col2:
            if st.form_submit_button("Cancelar"):
                st.session_state.show_timeline_form = False
                st.session_state.edit_item_id = None
                st.rerun()

        if submit:
            # Converter as datas para string formato ISO
            start_time_str = data_inicio.isoformat()
            end_time_str = data_fim.isoformat()

            # Se está no modo de edição, atualizar o item existente
            if edit_mode:
                success = Database.execute_write_query(
                    """
                    UPDATE timeline_items
                    SET title = ?, description = ?, start_time = ?, end_time = ?,
                        status = ?, priority = ?, task_type = ?, responsible_id = ?,
                        updated_at = datetime('now')
                    WHERE id = ?
                    """,
                    (
                        titulo,
                        descricao,
                        start_time_str,
                        end_time_str,
                        status,
                        prioridade,
                        tipo,
                        responsavel_id,
                        st.session_state.edit_item_id,
                    ),
                )

                if success:
                    st.success("Item atualizado com sucesso!")
                    st.session_state.show_timeline_form = False
                    st.session_state.edit_item_id = None
                    st.rerun()
                else:
                    st.error("Erro ao atualizar o item.")
            else:
                # Inserir novo item
                success = Database.execute_write_query(
                    """
                    INSERT INTO timeline_items (
                        event_id, title, description, start_time, end_time,
                        status, priority, task_type, responsible_id, created_at, updated_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
                    """,
                    (
                        evento_id,
                        titulo,
                        descricao,
                        start_time_str,
                        end_time_str,
                        status,
                        prioridade,
                        tipo,
                        responsavel_id,
                    ),
                )

                if success:
                    st.success("Item criado com sucesso!")
                    st.session_state.show_timeline_form = False
                    st.rerun()
                else:
                    st.error("Erro ao criar o item.")


def delete_timeline_item(item_id):
    """Exclui um item da timeline."""
    return Database.execute_write_query(
        "DELETE FROM timeline_items WHERE id = ?", (item_id,)
    )
