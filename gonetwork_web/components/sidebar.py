import os

import streamlit as st

from utils.notifications import Notifications


def render_sidebar():
    """Renderiza a barra lateral com menu de navegação e informações da aplicação."""

    # Logo e título
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "assets",
        "logo_gonetwork.png",
    )

    # Se o logo local não existir, usa o logo do GitHub
    if not os.path.exists(logo_path):
        st.sidebar.image(
            "https://raw.githubusercontent.com/contatogonetwork/melhorapp/main/resources/images/logo_gonetwork.png",
            width=200,
        )
    else:
        st.sidebar.image(logo_path, width=200)

    st.sidebar.title("GoNetwork AI")

    # Informações do usuário
    if "user_name" in st.session_state:
        st.sidebar.markdown(f"**Usuário:** {st.session_state.user_name}")

    # Exibir notificações não lidas, se houver
    unread_notifications = Notifications.get_all(include_read=False)
    if unread_notifications:
        with st.sidebar.container():
            col1, col2 = st.sidebar.columns([4, 1])
            with col1:
                st.markdown("### 📬 Notificações")
            with col2:
                st.markdown(f"### {len(unread_notifications)}")

            if st.sidebar.button("Ver notificações", key="btn_notifications"):
                st.session_state.show_notifications = True

    st.sidebar.divider()

    # Menu de navegação (alternativo ao menu horizontal)
    menu_options = {
        "Dashboard": {"icon": "📊", "text": "Dashboard"},
        "Briefings": {"icon": "📋", "text": "Briefings"},
        "Timeline": {"icon": "🗓️", "text": "Timeline"},
        "Edições": {"icon": "🎬", "text": "Edições"},
        "Clientes": {"icon": "👥", "text": "Clientes"},
        "Relatórios": {"icon": "📈", "text": "Relatórios"},
        "Configurações": {"icon": "⚙️", "text": "Configurações"},
    }

    # Renderizar opções do menu
    for key, option in menu_options.items():
        col1, col2 = st.sidebar.columns([1, 5])
        with col1:
            st.markdown(f"### {option['icon']}")
        with col2:
            if st.button(option["text"], key=f"menu_{key}", use_container_width=True):
                st.session_state.current_page = key
                st.rerun()

    # Seção de logout
    st.sidebar.divider()
    if st.sidebar.button("📤 Logout", use_container_width=True):
        for key in [
            "authenticated",
            "username",
            "user_name",
            "user_email",
            "current_page",
        ]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # Rodapé da barra lateral
    st.sidebar.divider()
    st.sidebar.caption("© 2025 GoNetwork AI")
    st.sidebar.caption("Versão Web 1.0")

    # Link para informações de contato
    with st.sidebar.expander("ℹ️ Contato"):
        st.write("Para suporte, entre em contato:")
        st.write("📧 suporte@gonetwork.com.br")
        st.write("📞 (11) 99999-9999")
