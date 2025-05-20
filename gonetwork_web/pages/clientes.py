import pandas as pd
import streamlit as st

from utils.database import Database
from utils.formatters import truncar_texto
from components.client_form import show_client_form


def show():
    """Renderiza a página de clientes."""
    st.title("👥 Clientes")

    # Carregar dados dos clientes
    clients = Database.execute_query(
        """
        SELECT id, company, contact_name, email, phone, updated_at
        FROM clients
        ORDER BY company
        """
    )

    # Adicionar cliente
    if st.button("➕ Adicionar Cliente", use_container_width=True):
        st.session_state.show_client_form = True

    # Exibir formulário se necessário
    if "show_client_form" in st.session_state and st.session_state.show_client_form:
        show_client_form(client_id=st.session_state.get('edit_client_id'))
        # O formulário lida com o estado da sessão internamente
    
    # Filtros de busca
    st.subheader("Busca")
    search_term = st.text_input("Buscar por nome ou contato:", "")
    
    # Filtrar clientes se houver termo de busca
    if search_term:
        search_term = search_term.lower()
        filtered_clients = [
            c for c in clients 
            if search_term in c['company'].lower() 
            or search_term in c['contact_name'].lower()
            or search_term in (c['email'].lower() if c['email'] else '')
        ]
    else:
        filtered_clients = clients

    # Exibir clientes em formato de tabela
    if not filtered_clients:
        st.info("Nenhum cliente encontrado.")
    else:
        # Preparar dados para exibição
        display_data = []
        for client in filtered_clients:
            display_data.append({
                "ID": client['id'],
                "Empresa": client['company'],
                "Contato": client['contact_name'],
                "Email": client['email'] or "",
                "Telefone": client['phone'] or "",
            })
            
        # Criar DataFrame para exibição
        df = pd.DataFrame(display_data)
        
        # Usar DataEditor para mostrar os dados
        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "ID": st.column_config.TextColumn("ID", width="small"),
                "Empresa": st.column_config.TextColumn("Empresa"),
                "Contato": st.column_config.TextColumn("Contato"),
                "Email": st.column_config.TextColumn("Email"),
                "Telefone": st.column_config.TextColumn("Telefone", width="medium"),
            }
        )
        
        # Seleção de cliente para detalhar/editar/excluir
        selected_client_id = st.selectbox(
            "Selecione um cliente para gerenciar:",
            options=[c["id"] for c in filtered_clients],
            format_func=lambda id: next((c["company"] for c in filtered_clients if c["id"] == id), id),
        )
        
        if selected_client_id:
            # Obter cliente selecionado
            selected_client = next((c for c in clients if c["id"] == selected_client_id), None)
            
            if selected_client:
                # Exibir detalhes e opções
                with st.container():
                    st.subheader(f"Cliente: {selected_client['company']}")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button("✏️ Editar", use_container_width=True):
                            st.session_state.edit_client_id = selected_client_id
                            st.session_state.show_client_form = True
                            st.rerun()
                            
                    with col2:
                        if st.button("🔍 Ver Projetos", use_container_width=True):
                            # Aqui poderia navegar para a página de projetos desse cliente
                            st.info("Esta funcionalidade será implementada em breve.")
                    
                    with col3:
                        if st.button("🗑️ Excluir Cliente", type="primary", use_container_width=True):
                            st.session_state.confirm_delete_client = selected_client_id
                
                # Confirmar exclusão
                if "confirm_delete_client" in st.session_state and st.session_state.confirm_delete_client == selected_client_id:
                    st.warning("⚠️ Esta ação não pode ser desfeita. Todos os dados deste cliente serão excluídos permanentemente.")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Confirmar exclusão", key="confirm_delete", type="primary"):
                            # Primeiro verificar se há projetos vinculados
                            projects = Database.execute_query(
                                "SELECT COUNT(*) as count FROM events WHERE client_id = ?",
                                (selected_client_id,)
                            )
                            
                            if projects and projects[0]['count'] > 0:
                                st.error(f"Este cliente tem {projects[0]['count']} projetos associados. Exclua-os primeiro.")
                            else:
                                # Excluir cliente
                                success = Database.execute_write_query(
                                    "DELETE FROM clients WHERE id = ?",
                                    (selected_client_id,)
                                )
                                
                                if success:
                                    st.success(f"Cliente '{selected_client['company']}' excluído com sucesso!")
                                    del st.session_state.confirm_delete_client
                                    st.rerun()
                                else:
                                    st.error("Erro ao excluir cliente.")
                    
                    with col2:
                        if st.button("❌ Cancelar", key="cancel_delete"):
                            del st.session_state.confirm_delete_client
                            st.rerun()
