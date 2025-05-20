import streamlit as st
import pandas as pd
from datetime import datetime
from utils.database import Database
from utils.formatters import formatar_data_hora


def show_comments_section(item_id, item_type, can_edit=True, is_admin=False):
    """
    Exibe uma seção de comentários para um item específico
    
    Args:
        item_id: ID do item (evento, briefing, edição, etc.)
        item_type: Tipo de item ('event', 'briefing', 'edit', etc.)
        can_edit: Se o usuário atual pode adicionar/editar comentários
        is_admin: Se o usuário é administrador (pode excluir qualquer comentário)
    
    Returns:
        None
    """
    st.subheader("Comentários")
    
    # Carregar comentários existentes
    comments = Database.execute_query(
        """
        SELECT c.id, c.content, c.timestamp, c.user_id, tm.name as user_name
        FROM comments c
        LEFT JOIN team_members tm ON c.user_id = tm.id
        WHERE c.item_id = ? AND c.item_type = ?
        ORDER BY c.timestamp DESC
        """,
        (item_id, item_type)
    )
    
    # Exibir formulário para adicionar novo comentário
    if can_edit:
        with st.form("add_comment_form"):
            comment_text = st.text_area("Adicionar comentário", height=100)
            col1, col2 = st.columns([3, 1])
            with col1:
                pass
            with col2:
                submit = st.form_submit_button("Enviar", use_container_width=True)
            
            if submit and comment_text.strip():
                user_id = st.session_state.get('user_id', 'unknown')
                timestamp = datetime.now().isoformat()
                
                # Inserir o comentário no banco de dados
                success = Database.execute_write_query(
                    """
                    INSERT INTO comments (item_id, item_type, content, user_id, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (item_id, item_type, comment_text, user_id, timestamp)
                )
                
                if success:
                    st.success("Comentário adicionado com sucesso!")
                    st.rerun()
                else:
                    st.error("Erro ao adicionar comentário")
    
    # Exibir comentários existentes
    if not comments:
        st.info("Nenhum comentário ainda.")
    else:
        st.write(f"Total: {len(comments)} comentários")
        
        for comment in comments:
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**{comment['user_name'] or 'Usuário'}**")
                with col2:
                    st.caption(formatar_data_hora(comment['timestamp']))
                
                st.markdown(comment['content'])
                
                # Opções de gerenciamento do comentário
                if is_admin or comment['user_id'] == st.session_state.get('user_id', None):
                    if st.button("🗑️ Excluir", key=f"del_comment_{comment['id']}", help="Excluir este comentário"):
                        success = Database.execute_write_query(
                            "DELETE FROM comments WHERE id = ?",
                            (comment['id'],)
                        )
                        
                        if success:
                            st.success("Comentário excluído com sucesso!")
                            st.rerun()
                        else:
                            st.error("Erro ao excluir comentário")
                
                st.divider()
                
    return None


def delete_all_comments(item_id, item_type, require_confirmation=True):
    """
    Exclui todos os comentários relacionados a um item
    
    Args:
        item_id: ID do item
        item_type: Tipo de item
        require_confirmation: Se deve exigir confirmação
        
    Returns:
        bool: True se os comentários foram excluídos
    """
    if require_confirmation:
        confirmation = st.checkbox(f"Confirmar exclusão de todos os comentários para este {item_type}")
        if not confirmation:
            return False
    
    success = Database.execute_write_query(
        "DELETE FROM comments WHERE item_id = ? AND item_type = ?",
        (item_id, item_type)
    )
    
    return success
