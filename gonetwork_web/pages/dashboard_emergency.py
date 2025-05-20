# Este arquivo pode ser usado se o dashboard principal falhar
import streamlit as st
from datetime import datetime

def show():
    """
    Dashboard minimalista para uso em caso de falha do dashboard principal.
    """
    st.title("📊 Dashboard (Modo de Emergência)")
    st.write("Esta é uma versão simplificada do dashboard devido a problemas no carregamento do módulo principal.")
    
    # Informações básicas
    st.subheader("Informações do Sistema")
    st.write(f"Data atual: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    st.write(f"Usuário: {st.session_state.username}")
    st.write(f"Função: {st.session_state.user_role}")
    
    # Métricas simples
    st.subheader("Métricas")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Projetos Ativos", "10", "")
    with col2:
        st.metric("Usuários Online", "3", "")
        
    # Placeholder para ações rápidas
    st.subheader("Ações Rápidas")
    if st.button("📝 Novo Briefing"):
        st.success("Esta funcionalidade será implementada em breve")
        
    if st.button("📋 Ver Projetos"):
        st.success("Esta funcionalidade será implementada em breve")