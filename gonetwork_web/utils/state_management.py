from datetime import datetime

import streamlit as st


def initialize_session_state():
    """
    Inicializa todos os estados necessários de uma vez para evitar reconstruções desnecessárias.
    """
    defaults = {
        # Estado de autenticação
        "authenticated": False,
        "user_id": None,
        "username": None,
        "user_name": None,  # Nome completo do usuário
        "user_role": None,
        "user_email": None,
        # Estado de navegação
        "current_page": "Dashboard",
        "sidebar_collapsed": False,
        "page_history": [],
        "last_activity": datetime.now().isoformat(),
        # Estado de seleção
        "selected_client_id": None,
        "selected_briefing_id": None,
        "selected_project_id": None,
        "selected_items": [],
        # Estado de configuração
        "filter_settings": {},
        "form_data": {},
        "theme": "light",
        # Estado de notificações
        "show_notifications": False,
        "notification_count": 0,
    }

    # Inicializar todos os estados necessários de uma vez
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


def check_session_state():
    """
    Verifica o estado da sessão e inicializa se necessário.
    Alias para initialize_session_state para compatibilidade.
    """
    initialize_session_state()
    check_session_timeout()


def check_session_timeout():
    """Verifica se a sessão expirou por inatividade"""
    if "last_activity" in st.session_state and st.session_state.authenticated:
        try:
            last_activity = datetime.fromisoformat(st.session_state.last_activity)
            time_diff = (datetime.now() - last_activity).total_seconds()

            # Sessão expira após 2 horas de inatividade (7200 segundos)
            if time_diff > 7200:
                logout_user()
                st.warning(
                    "Sua sessão expirou devido à inatividade. Por favor, faça login novamente."
                )
                st.rerun()
        except Exception as e:
            # Se houver erro ao analisar a data, apenas atualiza o timestamp
            update_last_activity()


def update_last_activity():
    """Atualiza o timestamp da última atividade do usuário"""
    st.session_state.last_activity = datetime.now().isoformat()


def logout_user():
    """Realiza o logout do usuário atual"""
    # Preservar apenas algumas configurações para conveniência
    preserved_settings = {
        "theme": st.session_state.get("theme", "light"),
        "sidebar_collapsed": st.session_state.get("sidebar_collapsed", False),
    }

    # Limpar o estado da sessão
    for key in list(st.session_state.keys()):
        if key not in preserved_settings:
            del st.session_state[key]

    # Restaurar configurações preservadas
    for key, value in preserved_settings.items():
        st.session_state[key] = value

    # Reinicializar estado padrão
    initialize_session_state()

    # Garantir que o usuário não está autenticado
    st.session_state.authenticated = False


def get_state(key, default=None):
    """Recupera um valor do estado com fallback seguro"""
    return st.session_state.get(key, default)


def set_state(key, value):
    """Define um valor de estado com tratamento de erro"""
    try:
        st.session_state[key] = value
        return True
    except Exception:
        return False
