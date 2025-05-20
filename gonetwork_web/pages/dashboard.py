from datetime import datetime

import streamlit as st


def show():
    """
    Exibe o dashboard principal da aplicação.
    Versão simplificada sem dependências externas para garantir funcionamento.
    """
    st.title("📊 Dashboard")
    st.caption("Visão geral do sistema GoNetwork AI")

    try:
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Briefings", "10", "+3")
        with col2:
            st.metric("Edições", "5", "-2")
        with col3:
            st.metric("Eventos", "2", "+1")
        with col4:
            st.metric("Clientes", "15", "0")

        # Gráfico simplificado sem dependências de Plotly
        st.subheader("Atividades Recentes")

        # Dados de exemplo
        chart_data = {
            "Segunda": [5, 3, 2],
            "Terça": [7, 5, 3],
            "Quarta": [4, 6, 2],
            "Quinta": [9, 7, 5],
            "Sexta": [6, 4, 3],
            "Sábado": [2, 1, 0],
            "Domingo": [1, 0, 0],
        }

        # Criar tabela de dados
        st.write("Visão geral da semana:")
        st.table(
            {
                "Dia": list(chart_data.keys()),
                "Briefings": [data[0] for data in chart_data.values()],
                "Edições": [data[1] for data in chart_data.values()],
                "Entregas": [data[2] for data in chart_data.values()],
            }
        )

        # Próximos eventos
        st.subheader("Próximos Eventos")

        eventos = [
            {
                "nome": "Entrevista CEO",
                "data": "21/05/2025",
                "local": "Sede GoNetwork",
                "status": "Confirmado",
            },
            {
                "nome": "Lançamento Produto",
                "data": "23/05/2025",
                "local": "Centro de Convenções",
                "status": "Pendente",
            },
            {
                "nome": "Workshop Marketing",
                "data": "25/05/2025",
                "local": "Auditório Principal",
                "status": "Confirmado",
            },
        ]

        for evento in eventos:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"**{evento['nome']}**")
                with col2:
                    st.write(evento["data"])
                with col3:
                    if evento["status"] == "Confirmado":
                        st.success("✓")
                    else:
                        st.warning("⚠")
                st.write(f"Local: {evento['local']}")
                st.divider()

        # Notas do dia
        with st.expander("Adicionar nota"):
            note = st.text_area("Nota do dia", "")
            if st.button("Salvar nota"):
                st.success("Nota salva com sucesso!")

    except Exception as e:
        st.error(f"Erro ao renderizar dashboard: {str(e)}")
        st.info("Versão simplificada do dashboard disponível")

        st.write("Bem-vindo ao GoNetwork AI Web")
        st.write(f"Usuário logado: {st.session_state.username}")
        st.write(f"Data atual: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
