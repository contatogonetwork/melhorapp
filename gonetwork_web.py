import streamlit as st
import pandas as pd
from datetime import datetime
import sqlite3
import os
import uuid
import json
from PIL import Image
from io import BytesIO
import base64

# Configuração inicial
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.current_page = "Dashboard"
    st.session_state.current_event_id = None
    st.session_state.current_client_id = None
    st.session_state.user_id = "admin"  # Simplificado para web
    st.session_state.search_query = ""

# Configuração da página
st.set_page_config(
    page_title="GoNetwork AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para carregar a configuração
def load_config():
    try:
        # Na versão web, podemos usar um arquivo config.json ou definir valores padrão
        if os.path.exists("config.json"):
            with open("config.json", "r") as f:
                return json.load(f)
        return {
            "db_path": "database/gonetwork.db",
            "default_project_path": "data/projects/",
            "theme": "light"
        }
    except Exception as e:
        st.error(f"Erro ao carregar configuração: {e}")
        return {}

config = load_config()

# Conexão com o banco de dados
def get_db_connection():
    try:
        conn = sqlite3.connect(config.get("db_path", "database/gonetwork.db"))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        st.error(f"Erro de conexão com o banco de dados: {e}")
        return None

# Função para inicializar o banco de dados
def initialize_database():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Criar tabelas se não existirem (simplificado)
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                contact TEXT,
                email TEXT,
                phone TEXT,
                created_at TEXT,
                updated_at TEXT
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                client_id TEXT,
                name TEXT NOT NULL,
                description TEXT,
                event_date TEXT,
                location TEXT,
                status TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id TEXT PRIMARY KEY,
                event_id TEXT,
                name TEXT NOT NULL,
                file_path TEXT,
                duration INTEGER,
                status TEXT,
                notes TEXT,
                created_at TEXT,
                updated_at TEXT,
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
            ''')
            
            conn.commit()
        except Exception as e:
            st.error(f"Erro ao inicializar o banco de dados: {e}")
        finally:
            conn.close()

# Estilo personalizado
def load_css():
    st.markdown("""
    <style>
        .main-header {color: #0066cc; font-size: 36px; font-weight: bold; margin-bottom: 20px;}
        .section-header {font-size: 24px; font-weight: bold; margin-top: 10px; margin-bottom: 10px;}
        .card {
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            background-color: #f8f9fa;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .metric-card {
            text-align: center;
            padding: 15px;
            border-radius: 5px;
            background-color: #ffffff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
        .sidebar .sidebar-content {
            background-color: #f1f3f4;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            background-color: #0066cc;
            color: white;
        }
        .status-pending {
            color: #ff9900;
            font-weight: bold;
        }
        .status-completed {
            color: #28a745;
            font-weight: bold;
        }
        .status-in-progress {
            color: #0066cc;
            font-weight: bold;
        }
        .streamlit-expanderHeader {
            font-weight: bold;
            color: #0066cc;
        }
        div[data-testid="stSidebarNav"] {
            background-image: url(data:image/png;base64,iVBORw0KGgo...);
            background-size: 200px;
            background-repeat: no-repeat;
            padding-top: 120px;
            background-position: 20px 20px;
        }
        div[data-testid="stSidebarNav"]::before {
            content: "GoNetwork AI";
            margin-left: 20px;
            font-size: 24px;
            font-weight: bold;
            color: #0066cc;
        }
    </style>
    """, unsafe_allow_html=True)

# Função de inicialização
def initialize_app():
    if not st.session_state.initialized:
        initialize_database()
        st.session_state.initialized = True

# Funções de utilidade
def format_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str

def get_status_class(status):
    status_map = {
        "Pendente": "status-pending",
        "Em Andamento": "status-in-progress",
        "Concluído": "status-completed"
    }
    return status_map.get(status, "")

# Funções CRUD para Clientes
def get_all_clients():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            st.error(f"Erro ao buscar clientes: {e}")
            return []
        finally:
            conn.close()
    return []

def get_client(client_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
            client = cursor.fetchone()
            return dict(client) if client else None
        except Exception as e:
            st.error(f"Erro ao buscar cliente: {e}")
            return None
        finally:
            conn.close()
    return None

def add_client(name, contact, email, phone):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            client_id = str(uuid.uuid4())
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO clients (id, name, contact, email, phone, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (client_id, name, contact, email, phone, now, now)
            )
            conn.commit()
            return client_id
        except Exception as e:
            st.error(f"Erro ao adicionar cliente: {e}")
            return None
        finally:
            conn.close()
    return None

def update_client(client_id, name, contact, email, phone):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "UPDATE clients SET name = ?, contact = ?, email = ?, phone = ?, updated_at = ? WHERE id = ?",
                (name, contact, email, phone, now, client_id)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar cliente: {e}")
            return False
        finally:
            conn.close()
    return False

def delete_client(client_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao excluir cliente: {e}")
            return False
        finally:
            conn.close()
    return False

# Funções CRUD para Eventos
def get_all_events():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.*, c.name as client_name 
                FROM events e 
                LEFT JOIN clients c ON e.client_id = c.id 
                ORDER BY e.event_date DESC
            """)
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            st.error(f"Erro ao buscar eventos: {e}")
            return []
        finally:
            conn.close()
    return []

def get_event(event_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.*, c.name as client_name 
                FROM events e 
                LEFT JOIN clients c ON e.client_id = c.id 
                WHERE e.id = ?
            """, (event_id,))
            event = cursor.fetchone()
            return dict(event) if event else None
        except Exception as e:
            st.error(f"Erro ao buscar evento: {e}")
            return None
        finally:
            conn.close()
    return None

def add_event(client_id, name, description, event_date, location, status="Pendente"):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            event_id = str(uuid.uuid4())
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO events (id, client_id, name, description, event_date, location, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (event_id, client_id, name, description, event_date, location, status, now, now)
            )
            conn.commit()
            return event_id
        except Exception as e:
            st.error(f"Erro ao adicionar evento: {e}")
            return None
        finally:
            conn.close()
    return None

def update_event(event_id, client_id, name, description, event_date, location, status):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "UPDATE events SET client_id = ?, name = ?, description = ?, event_date = ?, location = ?, status = ?, updated_at = ? WHERE id = ?",
                (client_id, name, description, event_date, location, status, now, event_id)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar evento: {e}")
            return False
        finally:
            conn.close()
    return False

def delete_event(event_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao excluir evento: {e}")
            return False
        finally:
            conn.close()
    return False

# Funções CRUD para Vídeos
def get_videos_by_event(event_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM videos WHERE event_id = ? ORDER BY created_at", (event_id,))
            return [dict(row) for row in cursor.fetchall()]
        except Exception as e:
            st.error(f"Erro ao buscar vídeos: {e}")
            return []
        finally:
            conn.close()
    return []

def add_video(event_id, name, file_path, duration, status="Pendente", notes=""):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            video_id = str(uuid.uuid4())
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO videos (id, event_id, name, file_path, duration, status, notes, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (video_id, event_id, name, file_path, duration, status, notes, now, now)
            )
            conn.commit()
            return video_id
        except Exception as e:
            st.error(f"Erro ao adicionar vídeo: {e}")
            return None
        finally:
            conn.close()
    return None

def update_video(video_id, name, status, notes):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "UPDATE videos SET name = ?, status = ?, notes = ?, updated_at = ? WHERE id = ?",
                (name, status, notes, now, video_id)
            )
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao atualizar vídeo: {e}")
            return False
        finally:
            conn.close()
    return False

def delete_video(video_id):
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM videos WHERE id = ?", (video_id,))
            conn.commit()
            return True
        except Exception as e:
            st.error(f"Erro ao excluir vídeo: {e}")
            return False
        finally:
            conn.close()
    return False

# Função para gerar estatísticas para o Dashboard
def get_dashboard_stats():
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Total de clientes
            cursor.execute("SELECT COUNT(*) as count FROM clients")
            total_clients = cursor.fetchone()['count']
            
            # Total de eventos
            cursor.execute("SELECT COUNT(*) as count FROM events")
            total_events = cursor.fetchone()['count']
            
            # Eventos por status
            cursor.execute("SELECT status, COUNT(*) as count FROM events GROUP BY status")
            events_by_status = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # Total de vídeos
            cursor.execute("SELECT COUNT(*) as count FROM videos")
            total_videos = cursor.fetchone()['count']
            
            # Vídeos por status
            cursor.execute("SELECT status, COUNT(*) as count FROM videos GROUP BY status")
            videos_by_status = {row['status']: row['count'] for row in cursor.fetchall()}
            
            # Eventos recentes
            cursor.execute("""
                SELECT e.*, c.name as client_name 
                FROM events e 
                LEFT JOIN clients c ON e.client_id = c.id 
                ORDER BY e.event_date DESC LIMIT 5
            """)
            recent_events = [dict(row) for row in cursor.fetchall()]
            
            return {
                "total_clients": total_clients,
                "total_events": total_events,
                "events_by_status": events_by_status,
                "total_videos": total_videos,
                "videos_by_status": videos_by_status,
                "recent_events": recent_events
            }
        except Exception as e:
            st.error(f"Erro ao buscar estatísticas: {e}")
            return {}
        finally:
            conn.close()
    return {}

# Componentes de UI para reutilização
def render_page_title(title):
    st.markdown(f"<h1 class='main-header'>{title}</h1>", unsafe_allow_html=True)

def render_section_title(title):
    st.markdown(f"<h2 class='section-header'>{title}</h2>", unsafe_allow_html=True)

def render_search_bar():
    search_query = st.text_input("🔍 Pesquisar", value=st.session_state.search_query)
    if search_query != st.session_state.search_query:
        st.session_state.search_query = search_query
        st.experimental_rerun()

# Páginas da aplicação
def dashboard_page():
    render_page_title("Dashboard")
    
    stats = get_dashboard_stats()
    if not stats:
        st.warning("Não foi possível carregar as estatísticas.")
        return
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(label="Total de Clientes", value=stats.get("total_clients", 0))
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(label="Total de Eventos", value=stats.get("total_events", 0))
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric(label="Total de Vídeos", value=stats.get("total_videos", 0))
        st.markdown("</div>", unsafe_allow_html=True)
    with col4:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        eventos_pendentes = stats.get("events_by_status", {}).get("Pendente", 0)
        st.metric(label="Eventos Pendentes", value=eventos_pendentes)
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos e status
    col1, col2 = st.columns(2)
    
    with col1:
        render_section_title("Status de Eventos")
        
        events_by_status = stats.get("events_by_status", {})
        
        # Preparar dados para o gráfico
        status_data = pd.DataFrame({
            'Status': list(events_by_status.keys()),
            'Quantidade': list(events_by_status.values())
        })
        
        if not status_data.empty:
            st.bar_chart(status_data.set_index('Status'))
        else:
            st.info("Sem dados de eventos para exibir.")
    
    with col2:
        render_section_title("Status de Vídeos")
        
        videos_by_status = stats.get("videos_by_status", {})
        
        # Preparar dados para o gráfico
        status_data = pd.DataFrame({
            'Status': list(videos_by_status.keys()),
            'Quantidade': list(videos_by_status.values())
        })
        
        if not status_data.empty:
            st.bar_chart(status_data.set_index('Status'))
        else:
            st.info("Sem dados de vídeos para exibir.")
    
    # Eventos recentes
    render_section_title("Eventos Recentes")
    
    recent_events = stats.get("recent_events", [])
    if recent_events:
        for event in recent_events:
            with st.expander(f"{event['name']} - {format_date(event['event_date'])}"):
                st.markdown(f"**Cliente:** {event.get('client_name', 'N/A')}")
                st.markdown(f"**Local:** {event.get('location', 'N/A')}")
                st.markdown(f"**Status:** <span class='{get_status_class(event.get('status', 'Pendente'))}'>{event.get('status', 'Pendente')}</span>", unsafe_allow_html=True)
                st.markdown(f"**Descrição:** {event.get('description', 'Sem descrição')}")
    else:
        st.info("Sem eventos recentes para exibir.")

def clients_page():
    render_page_title("Clientes")
    
    # Ações
    col1, col2 = st.columns([3, 1])
    with col1:
        render_search_bar()
    with col2:
        if st.button("➕ Novo Cliente"):
            st.session_state.show_add_client = True
    
    # Form para adicionar/editar cliente
    if st.session_state.get("show_add_client", False):
        with st.form("add_client_form"):
            st.subheader("Adicionar Novo Cliente")
            name = st.text_input("Nome do Cliente*")
            contact = st.text_input("Contato")
            email = st.text_input("Email")
            phone = st.text_input("Telefone")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Salvar")
            with col2:
                cancel = st.form_submit_button("Cancelar")
            
            if submit and name:
                add_client(name, contact, email, phone)
                st.session_state.show_add_client = False
                st.success(f"Cliente '{name}' adicionado com sucesso!")
                st.experimental_rerun()
            elif cancel:
                st.session_state.show_add_client = False
                st.experimental_rerun()
    
    # Form para editar cliente
    if st.session_state.get("edit_client_id", None):
        client_id = st.session_state.edit_client_id
        client = get_client(client_id)
        
        if client:
            with st.form("edit_client_form"):
                st.subheader(f"Editar Cliente: {client['name']}")
                name = st.text_input("Nome do Cliente*", value=client['name'])
                contact = st.text_input("Contato", value=client['contact'] or "")
                email = st.text_input("Email", value=client['email'] or "")
                phone = st.text_input("Telefone", value=client['phone'] or "")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Atualizar")
                with col2:
                    cancel = st.form_submit_button("Cancelar")
                
                if submit and name:
                    if update_client(client_id, name, contact, email, phone):
                        st.success(f"Cliente '{name}' atualizado com sucesso!")
                    st.session_state.edit_client_id = None
                    st.experimental_rerun()
                elif cancel:
                    st.session_state.edit_client_id = None
                    st.experimental_rerun()
    
    # Lista de clientes
    clients = get_all_clients()
    
    # Filtrar por pesquisa
    if st.session_state.search_query:
        query = st.session_state.search_query.lower()
        clients = [c for c in clients if query in c['name'].lower() or 
                  (c['contact'] and query in c['contact'].lower()) or 
                  (c['email'] and query in c['email'].lower())]
    
    if clients:
        for client in clients:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### {client['name']}")
                    if client['contact']:
                        st.markdown(f"**Contato:** {client['contact']}")
                    if client['email']:
                        st.markdown(f"**Email:** {client['email']}")
                    if client['phone']:
                        st.markdown(f"**Telefone:** {client['phone']}")
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{client['id']}"):
                        st.session_state.edit_client_id = client['id']
                        st.experimental_rerun()
                
                with col3:
                    if st.button("🗑️ Excluir", key=f"delete_{client['id']}"):
                        if delete_client(client['id']):
                            st.success(f"Cliente '{client['name']}' excluído com sucesso!")
                            st.experimental_rerun()
                
                st.markdown("---")
    else:
        st.info("Nenhum cliente encontrado.")

def events_page():
    render_page_title("Eventos")
    
    # Ações
    col1, col2 = st.columns([3, 1])
    with col1:
        render_search_bar()
    with col2:
        if st.button("➕ Novo Evento"):
            st.session_state.show_add_event = True
    
    # Form para adicionar evento
    if st.session_state.get("show_add_event", False):
        with st.form("add_event_form"):
            st.subheader("Adicionar Novo Evento")
            
            # Buscar lista de clientes para o select
            clients = get_all_clients()
            client_options = [("", "Selecione um cliente...")] + [(c['id'], c['name']) for c in clients]
            
            selected_client = st.selectbox(
                "Cliente*",
                options=[o[0] for o in client_options],
                format_func=lambda x: dict(client_options)[x] if x else "Selecione um cliente...",
            )
            
            name = st.text_input("Nome do Evento*")
            description = st.text_area("Descrição")
            
            col1, col2 = st.columns(2)
            with col1:
                event_date = st.date_input("Data do Evento")
            with col2:
                location = st.text_input("Local")
            
            status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"])
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Salvar")
            with col2:
                cancel = st.form_submit_button("Cancelar")
            
            if submit and name and selected_client:
                event_date_str = event_date.strftime("%Y-%m-%d %H:%M:%S")
                add_event(selected_client, name, description, event_date_str, location, status)
                st.session_state.show_add_event = False
                st.success(f"Evento '{name}' adicionado com sucesso!")
                st.experimental_rerun()
            elif cancel:
                st.session_state.show_add_event = False
                st.experimental_rerun()
    
    # Form para editar evento
    if st.session_state.get("edit_event_id", None):
        event_id = st.session_state.edit_event_id
        event = get_event(event_id)
        
        if event:
            with st.form("edit_event_form"):
                st.subheader(f"Editar Evento: {event['name']}")
                
                # Buscar lista de clientes para o select
                clients = get_all_clients()
                client_options = [("", "Selecione um cliente...")] + [(c['id'], c['name']) for c in clients]
                
                selected_client = st.selectbox(
                    "Cliente*",
                    options=[o[0] for o in client_options],
                    format_func=lambda x: dict(client_options)[x] if x else "Selecione um cliente...",
                    index=next((i for i, o in enumerate(client_options) if o[0] == event['client_id']), 0)
                )
                
                name = st.text_input("Nome do Evento*", value=event['name'])
                description = st.text_area("Descrição", value=event['description'] or "")
                
                col1, col2 = st.columns(2)
                with col1:
                    try:
                        event_date_obj = datetime.strptime(event['event_date'], "%Y-%m-%d %H:%M:%S").date()
                    except:
                        event_date_obj = datetime.now().date()
                    
                    event_date = st.date_input("Data do Evento", value=event_date_obj)
                with col2:
                    location = st.text_input("Local", value=event['location'] or "")
                
                status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"], index=["Pendente", "Em Andamento", "Concluído"].index(event['status']) if event['status'] in ["Pendente", "Em Andamento", "Concluído"] else 0)
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("Atualizar")
                with col2:
                    cancel = st.form_submit_button("Cancelar")
                
                if submit and name and selected_client:
                    event_date_str = event_date.strftime("%Y-%m-%d %H:%M:%S")
                    if update_event(event_id, selected_client, name, description, event_date_str, location, status):
                        st.success(f"Evento '{name}' atualizado com sucesso!")
                    st.session_state.edit_event_id = None
                    st.experimental_rerun()
                elif cancel:
                    st.session_state.edit_event_id = None
                    st.experimental_rerun()
    
    # Lista de eventos
    events = get_all_events()
    
    # Filtrar por pesquisa
    if st.session_state.search_query:
        query = st.session_state.search_query.lower()
        events = [e for e in events if query in e['name'].lower() or 
                 query in (e['client_name'] or "").lower() or 
                 query in (e['description'] or "").lower() or
                 query in (e['location'] or "").lower()]
    
    if events:
        for event in events:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.markdown(f"### {event['name']}")
                    st.markdown(f"**Cliente:** {event.get('client_name', 'N/A')}")
                    st.markdown(f"**Data:** {format_date(event['event_date'])}")
                    st.markdown(f"**Local:** {event.get('location', 'N/A')}")
                    st.markdown(f"**Status:** <span class='{get_status_class(event.get('status', 'Pendente'))}'>{event.get('status', 'Pendente')}</span>", unsafe_allow_html=True)
                
                with col2:
                    if st.button("📹 Vídeos", key=f"videos_{event['id']}"):
                        st.session_state.current_event_id = event['id']
                        st.session_state.current_page = "Videos"
                        st.experimental_rerun()
                
                with col3:
                    if st.button("✏️ Editar", key=f"edit_{event['id']}"):
                        st.session_state.edit_event_id = event['id']
                        st.experimental_rerun()
                
                with col4:
                    if st.button("🗑️ Excluir", key=f"delete_{event['id']}"):
                        if delete_event(event['id']):
                            st.success(f"Evento '{event['name']}' excluído com sucesso!")
                            st.experimental_rerun()
                
                st.markdown("---")
    else:
        st.info("Nenhum evento encontrado.")

def videos_page():
    # Se não houver um evento selecionado, redirecionar para a página de eventos
    if not st.session_state.current_event_id:
        st.session_state.current_page = "Events"
        st.experimental_rerun()
    
    event = get_event(st.session_state.current_event_id)
    if not event:
        st.error("Evento não encontrado.")
        st.session_state.current_page = "Events"
        st.experimental_rerun()
    
    render_page_title(f"Vídeos: {event['name']}")
    
    st.markdown(f"**Cliente:** {event.get('client_name', 'N/A')}")
    st.markdown(f"**Data:** {format_date(event['event_date'])}")
    st.markdown(f"**Status:** <span class='{get_status_class(event.get('status', 'Pendente'))}'>{event.get('status', 'Pendente')}</span>", unsafe_allow_html=True)
    
    # Botão para voltar
    if st.button("← Voltar para Eventos"):
        st.session_state.current_event_id = None
        st.session_state.current_page = "Events"
        st.experimental_rerun()
    
    st.markdown("---")
    
    # Ações
    col1, col2 = st.columns([3, 1])
    with col1:
        render_search_bar()
    with col2:
        if st.button("➕ Novo Vídeo"):
            st.session_state.show_add_video = True
    
    # Form para adicionar vídeo
    if st.session_state.get("show_add_video", False):
        with st.form("add_video_form"):
            st.subheader("Adicionar Novo Vídeo")
            
            name = st.text_input("Nome do Vídeo*")
            
            uploaded_file = st.file_uploader("Carregar Vídeo", type=['mp4', 'mov', 'avi'])
            
            duration = st.number_input("Duração (minutos)", min_value=0, value=0)
            status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"])
            notes = st.text_area("Anotações")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Salvar")
            with col2:
                cancel = st.form_submit_button("Cancelar")
            
            if submit and name:
                # Na versão web, podemos armazenar o arquivo em uma pasta temporária ou usar armazenamento em nuvem
                file_path = ""
                if uploaded_file:
                    # Na implementação real, seria necessário integrar com sistema de armazenamento
                    file_path = f"uploads/{uploaded_file.name}"
                    
                video_id = add_video(st.session_state.current_event_id, name, file_path, duration, status, notes)
                if video_id:
                    st.session_state.show_add_video = False
                    st.success(f"Vídeo '{name}' adicionado com sucesso!")
                    st.experimental_rerun()
            elif cancel:
                st.session_state.show_add_video = False
                st.experimental_rerun()
    
    # Form para editar vídeo
    if st.session_state.get("edit_video_id", None):
        video_id = st.session_state.edit_video_id
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM videos WHERE id = ?", (video_id,))
                video = cursor.fetchone()
                if video:
                    video = dict(video)
                else:
                    st.error("Vídeo não encontrado.")
                    st.session_state.edit_video_id = None
                    st.experimental_rerun()
            finally:
                conn.close()
        
        with st.form("edit_video_form"):
            st.subheader(f"Editar Vídeo: {video['name']}")
            
            name = st.text_input("Nome do Vídeo*", value=video['name'])
            status = st.selectbox("Status", ["Pendente", "Em Andamento", "Concluído"], index=["Pendente", "Em Andamento", "Concluído"].index(video['status']) if video['status'] in ["Pendente", "Em Andamento", "Concluído"] else 0)
            notes = st.text_area("Anotações", value=video['notes'] or "")
            
            col1, col2 = st.columns(2)
            with col1:
                submit = st.form_submit_button("Atualizar")
            with col2:
                cancel = st.form_submit_button("Cancelar")
            
            if submit and name:
                if update_video(video_id, name, status, notes):
                    st.success(f"Vídeo '{name}' atualizado com sucesso!")
                st.session_state.edit_video_id = None
                st.experimental_rerun()
            elif cancel:
                st.session_state.edit_video_id = None
                st.experimental_rerun()
    
    # Lista de vídeos
    videos = get_videos_by_event(st.session_state.current_event_id)
    
    # Filtrar por pesquisa
    if st.session_state.search_query:
        query = st.session_state.search_query.lower()
        videos = [v for v in videos if query in v['name'].lower() or 
                 query in (v['notes'] or "").lower()]
    
    if videos:
        for video in videos:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"### {video['name']}")
                    if video.get('duration'):
                        st.markdown(f"**Duração:** {video['duration']} minutos")
                    st.markdown(f"**Status:** <span class='{get_status_class(video.get('status', 'Pendente'))}'>{video.get('status', 'Pendente')}</span>", unsafe_allow_html=True)
                    if video.get('notes'):
                        with st.expander("Anotações"):
                            st.write(video['notes'])
                
                with col2:
                    if st.button("✏️ Editar", key=f"edit_{video['id']}"):
                        st.session_state.edit_video_id = video['id']
                        st.experimental_rerun()
                
                with col3:
                    if st.button("🗑️ Excluir", key=f"delete_{video['id']}"):
                        if delete_video(video['id']):
                            st.success(f"Vídeo '{video['name']}' excluído com sucesso!")
                            st.experimental_rerun()
                
                st.markdown("---")
    else:
        st.info("Nenhum vídeo encontrado para este evento.")

def reports_page():
    render_page_title("Relatórios")
    
    # Tipos de relatório
    report_type = st.selectbox(
        "Selecione o tipo de relatório",
        ["Status de Eventos", "Status de Vídeos", "Eventos por Cliente", "Produtividade"]
    )
    
    # Filtros comuns
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Data inicial", value=datetime.now().replace(day=1))
    with col2:
        end_date = st.date_input("Data final", value=datetime.now())
    
    if start_date > end_date:
        st.error("Data inicial deve ser anterior à data final!")
        return
    
    # Converter datas para string no formato do banco
    start_date_str = start_date.strftime("%Y-%m-%d 00:00:00")
    end_date_str = end_date.strftime("%Y-%m-%d 23:59:59")
    
    if report_type == "Status de Eventos":
        render_section_title("Relatório de Status de Eventos")
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT status, COUNT(*) as count 
                    FROM events 
                    WHERE event_date BETWEEN ? AND ?
                    GROUP BY status
                """, (start_date_str, end_date_str))
                
                status_data = {row["status"]: row["count"] for row in cursor.fetchall()}
                
                if status_data:
                    # Criar DataFrame para visualização
                    df = pd.DataFrame({
                        'Status': list(status_data.keys()),
                        'Quantidade': list(status_data.values())
                    })
                    
                    # Exibir gráfico
                    st.bar_chart(df.set_index('Status'))
                    
                    # Exibir tabela
                    st.dataframe(df)
                    
                    # Opção para baixar
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Baixar relatório CSV",
                        data=csv,
                        file_name=f"relatorio_eventos_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info(f"Nenhum evento encontrado no período de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")
            finally:
                conn.close()
    
    elif report_type == "Status de Vídeos":
        render_section_title("Relatório de Status de Vídeos")
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT v.status, COUNT(*) as count 
                    FROM videos v
                    INNER JOIN events e ON v.event_id = e.id
                    WHERE e.event_date BETWEEN ? AND ?
                    GROUP BY v.status
                """, (start_date_str, end_date_str))
                
                status_data = {row["status"]: row["count"] for row in cursor.fetchall()}
                
                if status_data:
                    # Criar DataFrame para visualização
                    df = pd.DataFrame({
                        'Status': list(status_data.keys()),
                        'Quantidade': list(status_data.values())
                    })
                    
                    # Exibir gráfico
                    st.bar_chart(df.set_index('Status'))
                    
                    # Exibir tabela
                    st.dataframe(df)
                    
                    # Opção para baixar
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Baixar relatório CSV",
                        data=csv,
                        file_name=f"relatorio_videos_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info(f"Nenhum vídeo encontrado no período de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")
            finally:
                conn.close()
    
    elif report_type == "Eventos por Cliente":
        render_section_title("Relatório de Eventos por Cliente")
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT c.name as client_name, COUNT(e.id) as event_count 
                    FROM events e
                    INNER JOIN clients c ON e.client_id = c.id
                    WHERE e.event_date BETWEEN ? AND ?
                    GROUP BY c.name
                    ORDER BY event_count DESC
                """, (start_date_str, end_date_str))
                
                results = [dict(row) for row in cursor.fetchall()]
                
                if results:
                    # Criar DataFrame para visualização
                    df = pd.DataFrame({
                        'Cliente': [row["client_name"] for row in results],
                        'Quantidade': [row["event_count"] for row in results]
                    })
                    
                    # Exibir gráfico
                    st.bar_chart(df.set_index('Cliente'))
                    
                    # Exibir tabela
                    st.dataframe(df)
                    
                    # Opção para baixar
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Baixar relatório CSV",
                        data=csv,
                        file_name=f"relatorio_clientes_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info(f"Nenhum evento encontrado no período de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")
            finally:
                conn.close()
    
    elif report_type == "Produtividade":
        render_section_title("Relatório de Produtividade")
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT 
                        strftime('%Y-%m', e.event_date) as month,
                        COUNT(DISTINCT e.id) as event_count,
                        COUNT(DISTINCT v.id) as video_count,
                        SUM(CASE WHEN v.status = 'Concluído' THEN 1 ELSE 0 END) as completed_videos
                    FROM events e
                    LEFT JOIN videos v ON e.id = v.event_id
                    WHERE e.event_date BETWEEN ? AND ?
                    GROUP BY month
                    ORDER BY month
                """, (start_date_str, end_date_str))
                
                results = [dict(row) for row in cursor.fetchall()]
                
                if results:
                    # Criar DataFrame para visualização
                    df = pd.DataFrame({
                        'Mês': [row["month"] for row in results],
                        'Eventos': [row["event_count"] for row in results],
                        'Vídeos': [row["video_count"] for row in results],
                        'Concluídos': [row["completed_videos"] for row in results]
                    })
                    
                    # Calcular taxa de conclusão
                    df['Taxa de Conclusão (%)'] = (df['Concluídos'] / df['Vídeos'] * 100).round(2).fillna(0)
                    
                    # Exibir gráfico
                    st.line_chart(df.set_index('Mês')[['Eventos', 'Vídeos', 'Concluídos']])
                    
                    # Exibir tabela
                    st.dataframe(df)
                    
                    # Opção para baixar
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="Baixar relatório CSV",
                        data=csv,
                        file_name=f"relatorio_produtividade_{start_date.strftime('%Y%m%d')}-{end_date.strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.info(f"Nenhum dado encontrado no período de {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")
            finally:
                conn.close()

def settings_page():
    render_page_title("Configurações")
    
    with st.form("settings_form"):
        st.subheader("Configurações do Sistema")
        
        current_config = load_config()
        
        db_path = st.text_input("Caminho do Banco de Dados", value=current_config.get("db_path", "database/gonetwork.db"))
        project_path = st.text_input("Pasta Padrão de Projetos", value=current_config.get("default_project_path", "data/projects/"))
        theme = st.selectbox("Tema", ["light", "dark"], index=0 if current_config.get("theme", "light") == "light" else 1)
        
        submit = st.form_submit_button("Salvar Configurações")
        
        if submit:
            new_config = {
                "db_path": db_path,
                "default_project_path": project_path,
                "theme": theme
            }
            
            try:
                with open("config.json", "w") as f:
                    json.dump(new_config, f, indent=4)
                st.success("Configurações salvas com sucesso! Algumas alterações podem requerer reiniciar o aplicativo.")
            except Exception as e:
                st.error(f"Erro ao salvar configurações: {e}")
    
    st.markdown("---")
    
    # Backup e Restauração
    st.subheader("Backup e Restauração")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Fazer Backup do Banco de Dados"):
            try:
                conn = get_db_connection()
                if conn:
                    backup_data = {}
                    
                    cursor = conn.cursor()
                    
                    # Backup de clientes
                    cursor.execute("SELECT * FROM clients")
                    backup_data["clients"] = [dict(row) for row in cursor.fetchall()]
                    
                    # Backup de eventos
                    cursor.execute("SELECT * FROM events")
                    backup_data["events"] = [dict(row) for row in cursor.fetchall()]
                    
                    # Backup de vídeos
                    cursor.execute("SELECT * FROM videos")
                    backup_data["videos"] = [dict(row) for row in cursor.fetchall()]
                    
                    # Criar arquivo JSON
                    backup_json = json.dumps(backup_data, indent=4)
                    
                    # Adicionar opção para download
                    now = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        label="Baixar Backup",
                        data=backup_json,
                        file_name=f"gonetwork_backup_{now}.json",
                        mime="application/json"
                    )
            except Exception as e:
                st.error(f"Erro ao criar backup: {e}")
    
    with col2:
        uploaded_file = st.file_uploader("Restaurar Backup", type=["json"])
        if uploaded_file is not None:
            try:
                backup_data = json.load(uploaded_file)
                
                # Verificar se o backup tem o formato esperado
                if not all(key in backup_data for key in ["clients", "events", "videos"]):
                    st.error("Arquivo de backup inválido!")
                else:
                    if st.button("Restaurar Dados (Atenção: isso substituirá dados existentes!)"):
                        conn = get_db_connection()
                        if conn:
                            try:
                                cursor = conn.cursor()
                                
                                # Limpar tabelas existentes
                                cursor.execute("DELETE FROM videos")
                                cursor.execute("DELETE FROM events")
                                cursor.execute("DELETE FROM clients")
                                
                                # Restaurar clientes
                                for client in backup_data["clients"]:
                                    cursor.execute(
                                        "INSERT INTO clients (id, name, contact, email, phone, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                        (client["id"], client["name"], client.get("contact"), client.get("email"), client.get("phone"), client.get("created_at"), client.get("updated_at"))
                                    )
                                
                                # Restaurar eventos
                                for event in backup_data["events"]:
                                    cursor.execute(
                                        "INSERT INTO events (id, client_id, name, description, event_date, location, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                        (event["id"], event["client_id"], event["name"], event.get("description"), 
                                         event.get("event_date"), event.get("location"), event.get("status"), 
                                         event.get("created_at"), event.get("updated_at"))
                                    )
                                
                                # Restaurar vídeos
                                for video in backup_data["videos"]:
                                    cursor.execute(
                                        "INSERT INTO videos (id, event_id, name, file_path, duration, status, notes, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                        (video["id"], video["event_id"], video["name"], video.get("file_path"), 
                                         video.get("duration"), video.get("status"), video.get("notes"), 
                                         video.get("created_at"), video.get("updated_at"))
                                    )
                                
                                conn.commit()
                                st.success("Restauração concluída com sucesso!")
                            except Exception as e:
                                st.error(f"Erro durante a restauração: {e}")
                                conn.rollback()
                            finally:
                                conn.close()
            except Exception as e:
                st.error(f"Erro ao processar arquivo de backup: {e}")

# Função principal da aplicação
def main():
    # Inicializar o aplicativo
    initialize_app()
    
    # Carregar estilos CSS
    load_css()
    
    # Sidebar de navegação
    st.sidebar.title("GoNetwork AI")
    st.sidebar.markdown("---")
    
    menu_options = {
        "Dashboard": "📊 Dashboard",
        "Clients": "👥 Clientes",
        "Events": "📅 Eventos",
        "Videos": "🎥 Vídeos",
        "Reports": "📈 Relatórios",
        "Settings": "⚙️ Configurações"
    }
    
    # Selecionar página
    selected_page = st.sidebar.radio("Menu", list(menu_options.values()))
    
    # Mapear seleção para chave da página
    selected_key = next(key for key, value in menu_options.items() if value == selected_page)
    
    # Atualizar estado da sessão
    if selected_key != "Videos" or selected_key == "Videos" and st.session_state.current_page == "Videos":
        st.session_state.current_page = selected_key
    
    # Exibir página correspondente
    if st.session_state.current_page == "Dashboard":
        dashboard_page()
    elif st.session_state.current_page == "Clients":
        clients_page()
    elif st.session_state.current_page == "Events":
        events_page()
    elif st.session_state.current_page == "Videos":
        videos_page()
    elif st.session_state.current_page == "Reports":
        reports_page()
    elif st.session_state.current_page == "Settings":
        settings_page()
    
    # Rodapé
    st.sidebar.markdown("---")
    st.sidebar.markdown("© 2025 GoNetwork")
    st.sidebar.markdown("Versão 1.0 Web")
    st.sidebar.markdown(f"Usuário: {st.session_state.user_id}")

# Executar aplicativo
if __name__ == "__main__":
    main()
