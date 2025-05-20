import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(
    page_title="GoNetwork AI", 
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo personalizado
st.markdown("""
<style>
    .main-header {color: #0066cc; font-size: 36px}
    .subheader {font-size: 24px; margin-bottom: 20px}
    .stApp {background-color: #f8f9fa}
</style>
""", unsafe_allow_html=True)

# Título com estilo
st.markdown("<h1 class='main-header'>GoNetwork AI – Web</h1>", unsafe_allow_html=True)

# Sidebar com logo (opcional)
# st.sidebar.image("logo.png", width=200)
aba = st.sidebar.radio("Menu de Navegação", ["Dashboard", "Briefing", "Edições"])

if aba == "Dashboard":
    st.markdown("<h2 class='subheader'>📊 Visão Geral do Evento</h2>", unsafe_allow_html=True)
    
    # Exemplo de métricas
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Eventos Ativos", value="5")
    col2.metric(label="Vídeos em Edição", value="12")
    col3.metric(label="Projetos Concluídos", value="27", delta="+3")
    
    # Exemplo de gráfico simples
    st.subheader("Status de Projetos")
    chart_data = pd.DataFrame({
        'Status': ['Em Andamento', 'Concluído', 'Não Iniciado'],
        'Quantidade': [4, 7, 2]
    })
    st.bar_chart(chart_data.set_index('Status'))

elif aba == "Briefing":
    st.markdown("<h2 class='subheader'>📝 Briefing</h2>", unsafe_allow_html=True)
    
    evento_nome = st.text_input("Nome do evento")
    cliente = st.text_input("Nome do cliente")
    data_evento = st.date_input("Data do evento")
    descricao = st.text_area("Descrição do briefing")
    
    col1, col2 = st.columns(2)
    with col1:
        duracao = st.number_input("Duração estimada (horas)", min_value=1, max_value=24)
    with col2:
        formato = st.selectbox("Formato de entrega", ["MP4", "MOV", "AVI", "Outro"])
    
    if st.button("Salvar Briefing"):
        # Aqui você adicionaria código para salvar os dados
        st.success(f"Briefing para '{evento_nome}' salvo com sucesso!")

elif aba == "Edições":
    st.markdown("<h2 class='subheader'>🎬 Edições de Vídeo</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Upload de Vídeo", "Revisão"])
    
    with tab1:
        uploaded_file = st.file_uploader("Envie um vídeo para revisar", type=['mp4', 'mov', 'avi'])
        if uploaded_file is not None:
            st.video(uploaded_file)
            st.text("Arquivo carregado: " + uploaded_file.name)
            
            comentario = st.text_area("Comentários sobre o vídeo")
            if st.button("Enviar para Revisão"):
                st.success("Vídeo enviado para revisão!")
    
    with tab2:
        st.info("Aqui aparecerão os vídeos disponíveis para revisão.")
        # Esta parte seria integrada com seu sistema backend