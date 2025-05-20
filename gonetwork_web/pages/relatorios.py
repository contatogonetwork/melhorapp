import io
from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.database import Database
from utils.formatters import formatar_data_hora, formatar_data_iso, formatar_status
from utils.reports import generate_csv_download_link, generate_excel_download_link


def show():
    """Renderiza a página de relatórios."""
    st.title("📈 Relatórios")

    # Selecionar o tipo de relatório
    relatorio_tipo = st.selectbox(
        "Selecione o tipo de relatório:",
        [
            "Resumo de Eventos",
            "Entregas por Status",
            "Performance da Equipe",
            "Histórico de Edições",
            "Clientes e Projetos",
        ],
    )

    # Definir período do relatório
    st.subheader("Período do Relatório")
    col1, col2 = st.columns(2)

    with col1:
        data_inicial = st.date_input(
            "Data Inicial",
            value=datetime.now() - timedelta(days=30),
            max_value=datetime.now(),
        )

    with col2:
        data_final = st.date_input(
            "Data Final",
            value=datetime.now(),
            min_value=data_inicial,
            max_value=datetime.now() + timedelta(days=1),
        )

    # Botão para gerar relatório
    if st.button("Gerar Relatório", use_container_width=True):
        # Converter datas para formato ISO
        data_inicial_iso = data_inicial.isoformat()
        data_final_iso = (
            data_final + timedelta(days=1)
        ).isoformat()  # Incluir o dia final completo

        # Gerar o relatório com base no tipo selecionado
        if relatorio_tipo == "Resumo de Eventos":
            gerar_relatorio_eventos(data_inicial_iso, data_final_iso)
        elif relatorio_tipo == "Entregas por Status":
            gerar_relatorio_entregas(data_inicial_iso, data_final_iso)
        elif relatorio_tipo == "Performance da Equipe":
            gerar_relatorio_equipe(data_inicial_iso, data_final_iso)
        elif relatorio_tipo == "Histórico de Edições":
            gerar_relatorio_edicoes(data_inicial_iso, data_final_iso)
        elif relatorio_tipo == "Clientes e Projetos":
            gerar_relatorio_clientes(data_inicial_iso, data_final_iso)


def gerar_relatorio_eventos(data_inicial, data_final):
    """Gera relatório de resumo de eventos."""
    st.subheader("Resumo de Eventos")

    # Obter dados do banco de dados
    eventos = Database.execute_query(
        """
        SELECT e.id, e.name, e.description, e.date, e.location, e.status,
               e.created_at, e.updated_at, c.company as client_name
        FROM events e
        LEFT JOIN clients c ON e.client_id = c.id
        WHERE e.date BETWEEN ? AND ?
        ORDER BY e.date DESC
        """,
        (data_inicial, data_final),
    )

    if not eventos:
        st.info(
            f"Nenhum evento encontrado no período de {formatar_data_iso(data_inicial)} a {formatar_data_iso(data_final)}"
        )
        return

    # Mostrar resumo estatístico
    total_eventos = len(eventos)
    status_counts = {}
    clientes = set()

    for evento in eventos:
        status = evento.get("status", "Desconhecido")
        status_counts[status] = status_counts.get(status, 0) + 1
        clientes.add(evento.get("client_name", "Desconhecido"))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Eventos", total_eventos)
    with col2:
        st.metric("Clientes Atendidos", len(clientes))
    with col3:
        status_concluidos = status_counts.get("completed", 0) + status_counts.get(
            "concluído", 0
        )
        st.metric("Eventos Concluídos", status_concluidos)

    # Criar gráfico de status
    status_df = pd.DataFrame(
        {"Status": list(status_counts.keys()), "Contagem": list(status_counts.values())}
    )

    fig = px.pie(
        status_df, values="Contagem", names="Status", title="Eventos por Status"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar tabela de eventos
    eventos_df = pd.DataFrame(eventos)
    eventos_df["date"] = eventos_df["date"].apply(formatar_data_iso)
    eventos_df["status"] = eventos_df["status"].apply(formatar_status)

    # Renomear colunas
    eventos_df = eventos_df.rename(
        columns={
            "name": "Nome",
            "description": "Descrição",
            "date": "Data",
            "location": "Local",
            "status": "Status",
            "client_name": "Cliente",
        }
    )

    # Selecionar e reordenar colunas
    colunas = ["Nome", "Descrição", "Data", "Local", "Status", "Cliente"]
    eventos_df = eventos_df[colunas]

    st.dataframe(eventos_df, use_container_width=True)

    # Links para download
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            generate_csv_download_link(
                eventos_df, f"eventos_{data_inicial[:10]}_{data_final[:10]}.csv"
            ),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            generate_excel_download_link(
                eventos_df, f"eventos_{data_inicial[:10]}_{data_final[:10]}.xlsx"
            ),
            unsafe_allow_html=True,
        )


def gerar_relatorio_entregas(data_inicial, data_final):
    """Gera relatório de entregas por status."""
    st.subheader("Entregas por Status")

    # Obter dados do banco de dados
    entregas = Database.execute_query(
        """
        SELECT d.id, d.title, d.description, d.deadline, d.status, d.progress,
               d.created_at, d.updated_at,
               e.name as event_name, c.company as client_name
        FROM deliverables d
        LEFT JOIN events e ON d.event_id = e.id
        LEFT JOIN clients c ON d.client_id = c.id
        WHERE d.created_at BETWEEN ? AND ? OR d.updated_at BETWEEN ? AND ?
        ORDER BY d.deadline
        """,
        (data_inicial, data_final, data_inicial, data_final),
    )

    if not entregas:
        st.info(
            f"Nenhuma entrega encontrada no período de {formatar_data_iso(data_inicial)} a {formatar_data_iso(data_final)}"
        )
        return

    # Mostrar resumo estatístico
    total_entregas = len(entregas)
    status_counts = {}

    for entrega in entregas:
        status = entrega.get("status", "Desconhecido")
        status_counts[status] = status_counts.get(status, 0) + 1

    # Calcular média de progresso
    progresso_medio = (
        sum(float(e["progress"] or 0) for e in entregas) / total_entregas
        if total_entregas > 0
        else 0
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Entregas", total_entregas)
    with col2:
        st.metric("Progresso Médio", f"{progresso_medio:.1f}%")
    with col3:
        entregas_concluidas = status_counts.get("completed", 0) + status_counts.get(
            "concluído", 0
        )
        st.metric("Entregas Concluídas", entregas_concluidas)

    # Gráfico de status
    status_df = pd.DataFrame(
        {"Status": list(status_counts.keys()), "Contagem": list(status_counts.values())}
    )

    fig = px.bar(status_df, x="Status", y="Contagem", title="Entregas por Status")
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar tabela de entregas
    entregas_df = pd.DataFrame(entregas)
    entregas_df["deadline"] = entregas_df["deadline"].apply(formatar_data_iso)
    entregas_df["status"] = entregas_df["status"].apply(formatar_status)

    # Renomear colunas
    entregas_df = entregas_df.rename(
        columns={
            "title": "Título",
            "description": "Descrição",
            "deadline": "Prazo",
            "status": "Status",
            "progress": "Progresso (%)",
            "event_name": "Evento",
            "client_name": "Cliente",
        }
    )

    # Selecionar e reordenar colunas
    colunas = [
        "Título",
        "Descrição",
        "Prazo",
        "Status",
        "Progresso (%)",
        "Evento",
        "Cliente",
    ]
    entregas_df = entregas_df[colunas]

    st.dataframe(entregas_df, use_container_width=True)

    # Links para download
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            generate_csv_download_link(
                entregas_df, f"entregas_{data_inicial[:10]}_{data_final[:10]}.csv"
            ),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            generate_excel_download_link(
                entregas_df, f"entregas_{data_inicial[:10]}_{data_final[:10]}.xlsx"
            ),
            unsafe_allow_html=True,
        )


def gerar_relatorio_equipe(data_inicial, data_final):
    """Gera relatório de performance da equipe."""
    st.subheader("Performance da Equipe")

    # Obter dados do banco de dados
    membros_equipe = Database.execute_query(
        """
        SELECT tm.id, tm.name, tm.role, tm.email,
               (SELECT COUNT(*) FROM event_team_members etm WHERE etm.member_id = tm.id) as total_events,
               (SELECT COUNT(*) FROM deliverables d WHERE d.responsible_id = tm.id) as total_deliveries
        FROM team_members tm
        ORDER BY tm.name
        """
    )

    if not membros_equipe:
        st.info("Nenhum membro da equipe encontrado.")
        return

    # Selecionar membro específico (opcional)
    todos_membros = ["Todos"] + [m["name"] for m in membros_equipe]
    membro_selecionado = st.selectbox("Filtrar por membro da equipe:", todos_membros)

    if membro_selecionado != "Todos":
        # Filtrar para o membro específico
        membro_id = next(
            (m["id"] for m in membros_equipe if m["name"] == membro_selecionado), None
        )

        if membro_id:
            # Carregar entregas desse membro
            entregas_membro = Database.execute_query(
                """
                SELECT d.id, d.title, d.deadline, d.status, d.progress,
                       e.name as event_name
                FROM deliverables d
                LEFT JOIN events e ON d.event_id = e.id
                WHERE d.responsible_id = ? AND (d.created_at BETWEEN ? AND ? OR d.updated_at BETWEEN ? AND ?)
                ORDER BY d.deadline
                """,
                (membro_id, data_inicial, data_final, data_inicial, data_final),
            )

            # Exibir estatísticas individuais
            if entregas_membro:
                total_entregas = len(entregas_membro)

                # Contar por status
                status_counts = {}
                for e in entregas_membro:
                    status = e.get("status", "Desconhecido")
                    status_counts[status] = status_counts.get(status, 0) + 1

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Entregas", total_entregas)
                with col2:
                    concluidas = status_counts.get("completed", 0) + status_counts.get(
                        "concluído", 0
                    )
                    st.metric("Entregas Concluídas", concluidas)
                    if total_entregas > 0:
                        st.metric(
                            "Taxa de Conclusão",
                            f"{(concluidas/total_entregas)*100:.1f}%",
                        )
                with col3:
                    st.metric(
                        "Função",
                        next(
                            (
                                m["role"]
                                for m in membros_equipe
                                if m["name"] == membro_selecionado
                            ),
                            "",
                        ),
                    )

                # Gráfico de status
                if status_counts:
                    status_df = pd.DataFrame(
                        {
                            "Status": list(status_counts.keys()),
                            "Contagem": list(status_counts.values()),
                        }
                    )
                    fig = px.pie(
                        status_df,
                        values="Contagem",
                        names="Status",
                        title=f"Entregas de {membro_selecionado} por Status",
                    )
                    st.plotly_chart(fig, use_container_width=True)

                # Tabela de entregas
                entregas_df = pd.DataFrame(entregas_membro)
                entregas_df["deadline"] = entregas_df["deadline"].apply(
                    formatar_data_iso
                )
                entregas_df["status"] = entregas_df["status"].apply(formatar_status)

                # Renomear colunas
                entregas_df = entregas_df.rename(
                    columns={
                        "title": "Título",
                        "deadline": "Prazo",
                        "status": "Status",
                        "progress": "Progresso (%)",
                        "event_name": "Evento",
                    }
                )

                st.dataframe(entregas_df, use_container_width=True)

                # Links para download
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        generate_csv_download_link(
                            entregas_df,
                            f"entregas_{membro_selecionado}_{data_inicial[:10]}_{data_final[:10]}.csv",
                        ),
                        unsafe_allow_html=True,
                    )
                with col2:
                    st.markdown(
                        generate_excel_download_link(
                            entregas_df,
                            f"entregas_{membro_selecionado}_{data_inicial[:10]}_{data_final[:10]}.xlsx",
                        ),
                        unsafe_allow_html=True,
                    )
            else:
                st.info(
                    f"Nenhuma entrega encontrada para {membro_selecionado} no período selecionado."
                )

    else:
        # Mostrar estatísticas de toda a equipe
        equipe_df = pd.DataFrame(membros_equipe)

        # Renomear colunas
        equipe_df = equipe_df.rename(
            columns={
                "name": "Nome",
                "role": "Função",
                "email": "Email",
                "total_events": "Eventos",
                "total_deliveries": "Entregas",
            }
        )

        # Selecionar colunas relevantes
        equipe_df = equipe_df[["Nome", "Função", "Email", "Eventos", "Entregas"]]

        # Exibir resumo da equipe
        st.metric("Total de Membros", len(equipe_df))

        # Gráfico de eventos/entregas por membro
        fig = px.bar(
            equipe_df,
            x="Nome",
            y=["Eventos", "Entregas"],
            title="Participação da Equipe",
            barmode="group",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Tabela completa
        st.dataframe(equipe_df, use_container_width=True)

        # Links para download
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                generate_csv_download_link(
                    equipe_df, f"equipe_{data_inicial[:10]}_{data_final[:10]}.csv"
                ),
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                generate_excel_download_link(
                    equipe_df, f"equipe_{data_inicial[:10]}_{data_final[:10]}.xlsx"
                ),
                unsafe_allow_html=True,
            )


def gerar_relatorio_edicoes(data_inicial, data_final):
    """Gera relatório de histórico de edições."""
    st.subheader("Histórico de Edições")

    # Obter dados do banco de dados - adaptando para as edições de vídeo
    edicoes = Database.execute_query(
        """
        SELECT d.id, d.title, d.description, d.deadline, d.status, d.progress,
               d.created_at, d.updated_at,
               e.name as event_name, c.company as client_name,
               tm.name as editor_name
        FROM deliverables d
        LEFT JOIN events e ON d.event_id = e.id
        LEFT JOIN clients c ON d.client_id = c.id
        LEFT JOIN team_members tm ON d.responsible_id = tm.id
        WHERE (d.title LIKE '%vídeo%' OR d.title LIKE '%video%')
        AND (d.created_at BETWEEN ? AND ? OR d.updated_at BETWEEN ? AND ?)
        ORDER BY d.updated_at DESC
        """,
        (data_inicial, data_final, data_inicial, data_final),
    )

    if not edicoes:
        st.info(
            f"Nenhuma edição de vídeo encontrada no período de {formatar_data_iso(data_inicial)} a {formatar_data_iso(data_final)}"
        )
        return

    # Resumo estatístico
    total_edicoes = len(edicoes)
    editores = set([e["editor_name"] for e in edicoes if e["editor_name"]])
    clientes = set([e["client_name"] for e in edicoes if e["client_name"]])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Edições", total_edicoes)
    with col2:
        st.metric("Editores", len(editores))
    with col3:
        st.metric("Clientes", len(clientes))

    # Agrupar por editor
    editor_counts = {}
    for edicao in edicoes:
        editor = edicao.get("editor_name", "Não atribuído")
        editor_counts[editor] = editor_counts.get(editor, 0) + 1

    # Gráfico de editores
    editor_df = pd.DataFrame(
        {"Editor": list(editor_counts.keys()), "Edições": list(editor_counts.values())}
    )

    fig = px.bar(editor_df, x="Editor", y="Edições", title="Edições por Editor")
    st.plotly_chart(fig, use_container_width=True)

    # Tabela de edições
    edicoes_df = pd.DataFrame(edicoes)
    edicoes_df["deadline"] = edicoes_df["deadline"].apply(formatar_data_iso)
    edicoes_df["updated_at"] = edicoes_df["updated_at"].apply(formatar_data_hora)
    edicoes_df["status"] = edicoes_df["status"].apply(formatar_status)

    # Renomear colunas
    edicoes_df = edicoes_df.rename(
        columns={
            "title": "Título",
            "description": "Descrição",
            "deadline": "Prazo",
            "status": "Status",
            "progress": "Progresso (%)",
            "event_name": "Evento",
            "client_name": "Cliente",
            "editor_name": "Editor",
            "updated_at": "Última Atualização",
        }
    )

    # Selecionar colunas
    colunas = [
        "Título",
        "Prazo",
        "Status",
        "Progresso (%)",
        "Evento",
        "Cliente",
        "Editor",
        "Última Atualização",
    ]
    edicoes_df = edicoes_df[colunas]

    st.dataframe(edicoes_df, use_container_width=True)

    # Links para download
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            generate_csv_download_link(
                edicoes_df, f"edicoes_{data_inicial[:10]}_{data_final[:10]}.csv"
            ),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            generate_excel_download_link(
                edicoes_df, f"edicoes_{data_inicial[:10]}_{data_final[:10]}.xlsx"
            ),
            unsafe_allow_html=True,
        )


def gerar_relatorio_clientes(data_inicial, data_final):
    """Gera relatório de clientes e projetos."""
    st.subheader("Clientes e Projetos")

    # Obter dados do banco de dados
    clientes = Database.execute_query(
        """
        SELECT c.id, c.company, c.contact_name, c.email, c.phone,
               COUNT(DISTINCT e.id) as total_events,
               COUNT(DISTINCT d.id) as total_deliverables
        FROM clients c
        LEFT JOIN events e ON c.id = e.client_id AND e.date BETWEEN ? AND ?
        LEFT JOIN deliverables d ON (c.id = d.client_id OR e.id = d.event_id) AND
                                    (d.created_at BETWEEN ? AND ? OR d.updated_at BETWEEN ? AND ?)
        GROUP BY c.id
        ORDER BY c.company
        """,
        (data_inicial, data_final, data_inicial, data_final, data_inicial, data_final),
    )

    if not clientes:
        st.info("Nenhum cliente encontrado.")
        return

    # Resumo estatístico
    total_clientes = len(clientes)
    clientes_ativos = sum(1 for c in clientes if c["total_events"] > 0)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Clientes", total_clientes)
    with col2:
        st.metric("Clientes Ativos no Período", clientes_ativos)
    with col3:
        if total_clientes > 0:
            st.metric(
                "Taxa de Clientes Ativos",
                f"{(clientes_ativos/total_clientes)*100:.1f}%",
            )

    # Gráfico de projetos por cliente
    clientes_projetos = [
        (c["company"], c["total_events"]) for c in clientes if c["total_events"] > 0
    ]
    if clientes_projetos:
        clientes_projetos.sort(key=lambda x: x[1], reverse=True)
        clientes_projetos = clientes_projetos[:10]  # Top 10

        clientes_df = pd.DataFrame(clientes_projetos, columns=["Cliente", "Projetos"])
        fig = px.bar(
            clientes_df, x="Cliente", y="Projetos", title="Top Clientes por Projetos"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Tabela de clientes
    clientes_df = pd.DataFrame(clientes)

    # Renomear colunas
    clientes_df = clientes_df.rename(
        columns={
            "company": "Empresa",
            "contact_name": "Contato",
            "email": "Email",
            "phone": "Telefone",
            "total_events": "Projetos",
            "total_deliverables": "Entregas",
        }
    )

    # Selecionar colunas
    colunas = ["Empresa", "Contato", "Email", "Telefone", "Projetos", "Entregas"]
    clientes_df = clientes_df[colunas]

    st.dataframe(clientes_df, use_container_width=True)

    # Links para download
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            generate_csv_download_link(
                clientes_df, f"clientes_{data_inicial[:10]}_{data_final[:10]}.csv"
            ),
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            generate_excel_download_link(
                clientes_df, f"clientes_{data_inicial[:10]}_{data_final[:10]}.xlsx"
            ),
            unsafe_allow_html=True,
        )
