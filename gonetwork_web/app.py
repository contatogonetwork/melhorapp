"""
GoNetwork AI Web - Aplicação principal
Versão 1.0.0
Última atualização: 2025-05-20
"""

import importlib
import os
import sys
import traceback
from datetime import datetime

import streamlit as st

# Verificar dependências e implementar fallbacks
DEPENDENCIES = {"streamlit_option_menu": False}

# Tentar importar streamlit_option_menu
try:
    from streamlit_option_menu import option_menu

    DEPENDENCIES["streamlit_option_menu"] = True
except ImportError:
    # Fallback simples para option_menu
    def option_menu(menu_title, options, icons, default_index, orientation, **kwargs):
        selected = st.selectbox(
            label=menu_title if menu_title else "Navegação",
            options=options,
            index=default_index,
        )
        return selected


# ------------------ CONFIGURAÇÃO INICIAL ------------------

# Adicionar diretório raiz ao PYTHONPATH para importações relativas
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuração da página
st.set_page_config(
    page_title="GoNetwork AI Web",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": "# GoNetwork AI\nVersão web da plataforma de produção de vídeo da GoNetwork",
        "Report a bug": "https://github.com/contatogonetwork/melhorapp/issues",
        "Get help": "mailto:suporte@gonetwork.com.br",
    },
)

# Verificar dependências ausentes
missing_dependencies = [
    name for name, installed in DEPENDENCIES.items() if not installed
]
if missing_dependencies:
    st.warning(
        f"""
    ⚠️ **Dependências ausentes detectadas:** {', '.join(missing_dependencies)}

    Para melhor experiência, instale as dependências necessárias:
    ```
    pip install {' '.join(missing_dependencies)}
    ```
    A aplicação continuará funcionando, mas com funcionalidades limitadas.
    """
    )

# ------------------ CARREGAMENTO DE RECURSOS ------------------


# Função para carregar CSS com cache
@st.cache_resource
def load_css():
    """Carrega e aplica o CSS personalizado uma única vez"""
    try:
        css_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "styles", "main.css"
        )
        if os.path.exists(css_path):
            with open(css_path, "r", encoding="utf-8") as f:
                st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Aviso: Não foi possível carregar o CSS personalizado: {str(e)}")


# Carregar CSS
load_css()

# ------------------ INICIALIZAÇÃO DO BANCO DE DADOS ------------------


# Função para inicializar o banco de dados
@st.cache_resource
def initialize_database():
    """Inicializa o banco de dados se necessário"""
    try:
        # Importar módulo de inicialização do banco de dados
        from utils.initialize_database import setup_database_schema

        # Configurar esquema do banco de dados
        setup_database_schema()

        return True
    except Exception as e:
        st.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        return False


# Inicializar banco de dados
db_initialized = initialize_database()

# ------------------ INICIALIZAÇÃO DO ESTADO DA SESSÃO ------------------

# Definir valores padrão para o estado da sessão
DEFAULT_SESSION_STATE = {
    "authenticated": False,
    "user_id": None,
    "username": None,
    "user_role": None,
    "current_page": "Dashboard",
    "last_activity": datetime.now().isoformat(),
    "page_history": [],
    "selected_client_id": None,
    "selected_briefing_id": None,
    "notifications": [],
    "show_sidebar": True,
    "theme": "light",
    "database_initialized": db_initialized,
}

# Inicializar estado da sessão de forma segura
for key, value in DEFAULT_SESSION_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ------------------ FUNÇÕES AUXILIARES ------------------


def load_module_safely(module_path):
    """
    Carrega um módulo Python de forma segura, com tratamento de erros.

    Args:
        module_path: Caminho do módulo (ex: 'components.sidebar')

    Returns:
        O módulo carregado ou None se falhar
    """
    try:
        return importlib.import_module(module_path)
    except ImportError as e:
        st.error(f"Erro ao importar módulo {module_path}: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Erro inesperado ao carregar {module_path}: {str(e)}")
        return None


def update_last_activity():
    """Atualiza o timestamp da última atividade do usuário"""
    st.session_state.last_activity = datetime.now().isoformat()


def check_session_timeout():
    """Verifica se a sessão expirou por inatividade"""
    if "last_activity" in st.session_state and st.session_state.authenticated:
        last_activity = datetime.fromisoformat(st.session_state.last_activity)
        time_diff = (datetime.now() - last_activity).total_seconds()

        # Sessão expira após 2 horas de inatividade (7200 segundos)
        if time_diff > 7200:
            logout_user()
            st.warning(
                "Sua sessão expirou devido à inatividade. Por favor, faça login novamente."
            )
            st.rerun()


def logout_user():
    """Realiza o logout do usuário atual"""
    # Preservar apenas algumas configurações para conveniência
    preserved_settings = {"theme": st.session_state.get("theme", "light")}

    # Limpar o estado da sessão
    for key in list(st.session_state.keys()):
        if key not in preserved_settings:
            del st.session_state[key]

    # Restaurar configurações preservadas
    for key, value in preserved_settings.items():
        st.session_state[key] = value

    # Garantir que o usuário não está autenticado
    st.session_state.authenticated = False


# ------------------ SISTEMA DE AUTENTICAÇÃO ------------------


def default_auth():
    """Sistema de autenticação simplificado para uso emergencial"""
    st.title("🌐 GoNetwork AI - Login (Modo Emergência)")

    with st.form("emergency_login"):
        username = st.text_input("Usuário", placeholder="Digite seu nome de usuário")
        password = st.text_input(
            "Senha", type="password", placeholder="Digite sua senha"
        )
        submit = st.form_submit_button("Entrar")

        if submit:
            if username == "admin" and password == "admin":
                st.success("Login bem-sucedido!")
                st.session_state.authenticated = True
                st.session_state.username = "admin"
                st.session_state.user_id = 1
                st.session_state.user_role = "admin"
                st.session_state.last_activity = datetime.now().isoformat()
                st.rerun()
                return True
            else:
                st.error("Credenciais inválidas")
                return False
    return False


# Carregar módulo de autenticação
auth_module = load_module_safely("components.authentication")


# Função de autenticação (com fallback)
def authenticate_user():
    """Autentica o usuário usando o módulo de autenticação ou fallback"""
    # Verificar se já está autenticado
    if st.session_state.get("authenticated", False):
        update_last_activity()
        return True

    # Tentar usar o módulo de autenticação
    if auth_module and hasattr(auth_module, "authenticate_user"):
        try:
            return auth_module.authenticate_user()
        except Exception as e:
            st.error(f"Erro no sistema de autenticação: {str(e)}")

    # Fallback para autenticação simples
    st.warning("Usando sistema de autenticação de emergência")
    return default_auth()


# ------------------ SIDEBAR E NAVEGAÇÃO ------------------


# Função para renderizar sidebar (com fallback)
def render_sidebar():
    """Renderiza a barra lateral com informações do usuário e navegação"""
    with st.sidebar:
        try:
            # Tentar carregar o módulo de sidebar
            sidebar_module = load_module_safely("components.sidebar")
            if sidebar_module and hasattr(sidebar_module, "render_sidebar"):
                sidebar_module.render_sidebar()
                return

            # Implementação de fallback se o módulo não estiver disponível
            st.title("GoNetwork AI")

            # Logo (se disponível)
            try:
                st.image("assets/logo_gonetwork.png", width=200)
            except:
                pass

            # Informações do usuário
            st.subheader(f"Olá, {st.session_state.username}")

            if st.session_state.user_role == "admin":
                st.write("👑 Administrador")
            elif st.session_state.user_role == "editor":
                st.write("✂️ Editor")
            else:
                st.write("👤 Usuário")

            st.divider()

            # Navegação rápida
            st.subheader("Navegação")

            pages = {
                "📊 Dashboard": "Dashboard",
                "📋 Briefings": "Briefings",
                "🗓️ Timeline": "Timeline",
                "🎬 Edições": "Edições",
                "👥 Clientes": "Clientes",
                "⚙️ Configurações": "Configurações",
            }

            # Criar botões para navegação
            col1, col2 = st.columns(2)
            count = 0
            for label, page in pages.items():
                col = col1 if count % 2 == 0 else col2
                with col:
                    if st.button(label):
                        st.session_state.current_page = page
                        st.rerun()
                count += 1

            st.divider()

            # Opções do usuário
            if st.button("🚪 Logout"):
                logout_user()
                st.rerun()

        except Exception as e:
            st.error(f"Erro na sidebar: {str(e)}")

            # Sempre exibir opção de logout em caso de erro
            if st.button("🚪 Logout (Emergência)"):
                logout_user()
                st.rerun()


# ------------------ CARREGAMENTO DE PÁGINAS ------------------


# Função para carregar e exibir uma página
def load_and_show_page(page_name):
    """
    Carrega e exibe uma página específica com tratamento de erro.

    Args:
        page_name: Nome da página a carregar (ex: 'dashboard')
    """
    try:
        # Tentar importar o módulo da página
        module_path = f"pages.{page_name.lower()}"
        page_module = load_module_safely(module_path)

        if page_module and hasattr(page_module, "show"):
            # Registrar navegação no histórico
            if st.session_state.current_page not in st.session_state.page_history:
                st.session_state.page_history.append(st.session_state.current_page)

            # Atualizar página atual
            st.session_state.current_page = page_name

            # Exibir a página
            with st.spinner(f"Carregando {page_name}..."):
                page_module.show()
            return True

        # Fallback: página básica se o módulo não tiver função show()
        st.title(f"{page_name}")
        st.warning(f"A página {page_name} está em construção.")
        return False

    except Exception as e:
        st.error(f"Erro ao carregar página {page_name}: {str(e)}")
        st.code(traceback.format_exc(), language="python")

        # Página de emergência
        st.title(f"{page_name} - Modo de Emergência")
        st.warning("Esta página está em modo de emergência devido a um erro.")
        st.write(f"Usuário: {st.session_state.username}")
        st.write(f"Data atual: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        return False


# ------------------ INTERFACE PRINCIPAL ------------------

# Verificar timeout de sessão
check_session_timeout()

# Verificar autenticação
if not st.session_state.authenticated:
    authenticate_user()

# Interface principal quando autenticado
if st.session_state.authenticated:
    # Atualizar tempo de atividade
    update_last_activity()

    # Renderizar sidebar
    render_sidebar()

    try:
        # Menu de navegação principal (horizontal ou dropdown dependendo da disponibilidade do módulo)
        pages = [
            "Dashboard",
            "Briefings",
            "Timeline",
            "Edições",
            "Clientes",
            "Relatórios",
            "Configurações",
            "Ajuda",
        ]
        icons = [
            "house",
            "file-earmark-text",
            "calendar3",
            "camera-reels",
            "people",
            "graph-up",
            "gear",
            "question-circle",
        ]

        if DEPENDENCIES["streamlit_option_menu"]:
            # Usar option_menu se disponível
            selected = option_menu(
                menu_title=None,
                options=pages,
                icons=icons,
                menu_icon="cast",
                default_index=0,
                orientation="horizontal",
            )
        else:
            # Fallback para selectbox
            st.write("### Navegação")
            selected = st.selectbox("Selecione uma página:", pages, index=0)
            st.divider()

        # Carregar a página selecionada
        load_and_show_page(selected)

    except Exception as e:
        st.error(f"Erro na navegação principal: {str(e)}")

        # Interface de emergência
        st.title("GoNetwork AI Web - Modo de Emergência")
        st.warning(
            "A interface principal encontrou um erro. Usando modo de emergência."
        )

        # Menu de navegação simplificado
        options = [
            "Dashboard",
            "Briefings",
            "Timeline",
            "Edições",
            "Clientes",
            "Configurações",
        ]
        selected = st.selectbox("Selecione uma página:", options)

        if st.button("Ir para a página"):
            load_and_show_page(selected)

else:
    # Mensagem para usuários não autenticados
    st.info("Faça login para acessar a plataforma GoNetwork AI.")

# ------------------ RODAPÉ ------------------

# Exibir rodapé
footer_html = """
<div class="footer">
    <p>© 2025 GoNetwork AI - Todos os direitos reservados</p>
    <p>Versão 1.0.0 | <a href="mailto:suporte@gonetwork.com.br">Suporte</a></p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)

# Exibir mensagem de depuração se necessário (apenas para desenvolvimento)
debug_mode = False
if debug_mode:
    with st.expander("Informações de Debug"):
        st.write(
            "Estado da Sessão:",
            {k: v for k, v in st.session_state.items() if k != "authenticated"},
        )
        st.write("Data e hora atual:", datetime.now().isoformat())
        st.write("Caminho do aplicativo:", os.path.dirname(os.path.abspath(__file__)))
        st.write("Dependências:", DEPENDENCIES)
