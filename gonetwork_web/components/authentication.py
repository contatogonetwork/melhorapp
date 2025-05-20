import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import os
import hashlib
from datetime import datetime

def authenticate_user():
    """
    Implementa autenticação de usuários usando streamlit-authenticator.
    Inclui autenticação simplificada como fallback.
    """
    # Verificar se já está autenticado
    if st.session_state.get('authenticated', False):
        return True
    
    # Tentar autenticação com streamlit-authenticator    
    try:
        return authenticate_with_stauth()
    except Exception as e:
        st.error(f"Erro no sistema de autenticação principal: {str(e)}")
        st.info("Usando sistema de autenticação alternativo...")
        return simple_auth_fallback()

def authenticate_with_stauth():
    """Autenticação usando o streamlit-authenticator"""
    # Caminho para o arquivo de configuração
    config_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'config',
        'credentials.yaml'
    )
    
    # Verificar se o arquivo existe; caso contrário, criar um arquivo padrão
    if not os.path.exists(config_file):
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        # CORREÇÃO: Usar Hasher.hash() em vez de Hasher().generate()
        hashed_password = stauth.Hasher.hash("admin")
        
        credentials = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'email': 'admin@gonetwork.com',
                        'name': 'Administrador',
                        'password': hashed_password
                    }
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'gonetwork_auth',
                'name': 'gonetwork_auth'
            }
        }
        
        with open(config_file, 'w') as file:
            yaml.dump(credentials, file, default_flow_style=False)
    
    # Carregar credenciais
    with open(config_file) as file:
        config = yaml.load(file, Loader=SafeLoader)
    
    # Configurar autenticador
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
    # Criar um formulário de login
    name, authentication_status, username = authenticator.login('Login', 'main')
    
    if authentication_status:
        st.success(f"Bem-vindo, {name}!")
        st.session_state.username = username
        st.session_state.user_id = 1  # Na implementação real, obter o ID do banco
        st.session_state.user_role = "admin"  # Na implementação real, obter do banco
        return True
    elif authentication_status is False:
        st.error("Nome de usuário/senha incorretos")
        return False
    else:
        st.warning("Por favor, entre com seu nome de usuário e senha")
        return False

def simple_auth_fallback():
    """Sistema de autenticação simplificado como fallback"""
    st.title("🌐 GoNetwork AI - Login")
    
    with st.form("login_form"):
        username = st.text_input("Usuário", placeholder="Digite seu nome de usuário")
        password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
        submit_button = st.form_submit_button("Entrar")
        
        if submit_button:
            # Para desenvolvimento, aceitar credenciais simples
            if username == "admin" and password == "admin":
                st.success("Login bem-sucedido!")
                st.session_state.authenticated = True
                st.session_state.username = "admin"
                st.session_state.user_id = 1
                st.session_state.user_role = "admin"
                st.rerun()
                return True
            else:
                st.error("Nome de usuário ou senha incorretos!")
                return False
    return False