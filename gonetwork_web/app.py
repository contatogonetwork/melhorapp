import streamlit as st
from database_web import carregar_briefings, carregar_edicoes, carregar_timeline
from utils_web import formatar_data_hora, formatar_data_iso, truncar_texto

st.set_page_config(
    page_title="GoNetwork AI (Web)",
    page_icon="🎥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Configuração da barra lateral
st.sidebar.image(
    "https://raw.githubusercontent.com/contatogonetwork/melhorapp/main/resources/images/logo_gonetwork.png",
    width=200,
)
st.sidebar.title("Navegação")
aba = st.sidebar.radio("Escolha uma aba:", ["Briefing", "Timeline", "Edições"])

st.title("🌐 GoNetwork AI – Versão Web")

if aba == "Briefing":
    st.subheader("📋 Briefing")
    briefings = carregar_briefings()

    if not briefings:
        st.info("Nenhum briefing encontrado no banco de dados.")
    else:
        # Criar colunas para informações organizadas
        col1, col2, col3 = st.columns([3, 2, 2])

        with col1:
            st.subheader("Evento")
        with col2:
            st.subheader("Data")
        with col3:
            st.subheader("Local")

        for b in briefings:
            with col1:
                st.write(f"**{b['nome_evento']}**")
            with col2:
                st.write(formatar_data_iso(b["data"]))
            with col3:
                st.write(b["local"])
elif aba == "Timeline":
    st.subheader("🗓️ Timeline")
    timeline = carregar_timeline()

    if not timeline:
        st.info("Nenhum item de timeline encontrado no banco de dados.")
    else:
        # Criar um dataframe para a timeline
        import pandas as pd

        # Preparar dados formatados
        timeline_data = []
        for item in timeline:
            timeline_data.append(
                {
                    "Início": formatar_data_hora(item["inicio"]),
                    "Fim": formatar_data_hora(item["fim"]),
                    "Atividade": item["titulo"],
                    "Responsável": item["responsavel"],
                }
            )

        # Exibir como dataframe interativo
        df = pd.DataFrame(timeline_data)
        st.dataframe(df, use_container_width=True)
elif aba == "Edições":
    st.subheader("🎬 Edições")
    edicoes = carregar_edicoes()

    if not edicoes:
        st.info("Nenhuma edição de vídeo encontrada no banco de dados.")
    else:
        # Adicionar filtro por editor
        editores = sorted(list(set([ed["editor"] for ed in edicoes])))
        editor_selecionado = st.selectbox("Filtrar por editor:", ["Todos"] + editores)

        # Filtrar por editor se necessário
        if editor_selecionado != "Todos":
            edicoes_filtradas = [
                ed for ed in edicoes if ed["editor"] == editor_selecionado
            ]
        else:
            edicoes_filtradas = edicoes

        # Exibir edições em cards
        for ed in edicoes_filtradas:
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image(
                        "https://img.icons8.com/color/96/000000/video-editing.png",
                        width=50,
                    )
                with col2:
                    st.markdown(f"**{ed['video']}**")
                    st.markdown(
                        f"Editor: **{ed['editor']}** | Entregue: {formatar_data_hora(ed['hora'])}"
                    )
                st.divider()

# Adicionar rodapé com informações da versão
st.sidebar.divider()
st.sidebar.caption("© 2025 GoNetwork AI")
st.sidebar.caption("Versão Web 1.0")

# Adicionar seção de contato na barra lateral
with st.sidebar.expander("ℹ️ Contato"):
    st.write("Para suporte, entre em contato:")
    st.write("📧 suporte@gonetwork.com.br")
    st.write("📞 (11) 99999-9999")
