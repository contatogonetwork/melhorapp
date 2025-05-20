import streamlit as st
from utils.database import Database
from datetime import datetime


def show_client_form(client_id=None, on_save=None):
    """
    Exibe um formulário para adicionar ou editar cliente
    
    Args:
        client_id: ID do cliente para edição, ou None para criar novo
        on_save: Função de callback ao salvar
        
    Returns:
        dict: Dados do cliente ou None
    """
    edit_mode = client_id is not None
    
    # Carregar dados do cliente se estivermos editando
    client_data = {}
    if edit_mode:
        result = Database.execute_query(
            "SELECT * FROM clients WHERE id = ?", 
            (client_id,)
        )
        if result:
            client_data = result[0]
    
    with st.form("client_form"):
        st.subheader("Informações do Cliente")
        
        # Campos do formulário
        company = st.text_input("Nome da Empresa*", value=client_data.get('company', ''))
        contact_name = st.text_input("Nome do Contato*", value=client_data.get('contact_name', ''))
        
        col1, col2 = st.columns(2)
        with col1:
            email = st.text_input("Email", value=client_data.get('email', ''))
        with col2:
            phone = st.text_input("Telefone", value=client_data.get('phone', ''))
        
        address = st.text_area("Endereço", value=client_data.get('address', ''))
        notes = st.text_area("Observações", value=client_data.get('notes', ''))
        
        # Seção de segurança para clientes que acessam o sistema
        st.subheader("Acesso ao Sistema")
        has_access = st.checkbox("Cliente tem acesso ao sistema", value=bool(client_data.get('has_access', False)))
        
        if has_access:
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Nome de usuário", value=client_data.get('username', ''))
            with col2:
                password = st.text_input("Senha", type="password", value="")
            
            access_level = st.selectbox(
                "Nível de Acesso",
                options=["Visualização", "Comentários", "Aprovações"],
                index=max(0, ["Visualização", "Comentários", "Aprovações"].index(client_data.get('access_level', 'Visualização')) if 'access_level' in client_data else 0)
            )
        
        # Botões de controle
        col1, col2 = st.columns(2)
        with col1:
            submit = st.form_submit_button("Salvar Cliente")
        with col2:
            cancel = st.form_submit_button("Cancelar")
        
        if cancel:
            if 'show_client_form' in st.session_state:
                del st.session_state.show_client_form
            if 'edit_client_id' in st.session_state:
                del st.session_state.edit_client_id
            return None
        
        if submit:
            # Validar campos
            if not company or not contact_name:
                st.error("Os campos marcados com * são obrigatórios.")
                return None
                
            # Preparar dados para salvar
            now = datetime.now().isoformat()
            
            if not has_access:
                username = None
                password_hash = None
                access_level = None
            elif password:
                # Aqui poderia ter uma função para gerar hash da senha
                import hashlib
                password_hash = hashlib.sha256(password.encode()).hexdigest()
            else:
                password_hash = client_data.get('password_hash') if edit_mode else None
            
            client_data = {
                'company': company,
                'contact_name': contact_name,
                'email': email,
                'phone': phone,
                'address': address,
                'notes': notes,
                'has_access': has_access,
                'username': username,
                'password_hash': password_hash,
                'access_level': access_level,
            }
            
            # Salvar no banco de dados
            if edit_mode:
                # Atualizar cliente existente
                query = """
                UPDATE clients
                SET company = ?, contact_name = ?, email = ?, phone = ?,
                    address = ?, notes = ?, has_access = ?, username = ?,
                    password_hash = ?, access_level = ?, updated_at = ?
                WHERE id = ?
                """
                params = (*client_data.values(), now, client_id)
                success = Database.execute_write_query(query, params)
            else:
                # Inserir novo cliente
                query = """
                INSERT INTO clients (company, contact_name, email, phone,
                                    address, notes, has_access, username,
                                    password_hash, access_level, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (*client_data.values(), now, now)
                success = Database.execute_write_query(query, params)
            
            if success:
                if edit_mode:
                    st.success(f"Cliente '{company}' atualizado com sucesso!")
                else:
                    st.success(f"Cliente '{company}' adicionado com sucesso!")
                
                # Limpar estado
                if 'show_client_form' in st.session_state:
                    del st.session_state.show_client_form
                if 'edit_client_id' in st.session_state:
                    del st.session_state.edit_client_id
                
                # Executar callback se fornecido
                if on_save and callable(on_save):
                    on_save()
                
                return client_data
            else:
                st.error("Erro ao salvar cliente no banco de dados.")
                return None
            
    return None
