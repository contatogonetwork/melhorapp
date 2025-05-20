import streamlit as st
import importlib
import sys

@st.cache_resource
def load_module(module_name):
    """
    Carrega módulos dinamicamente e com cache para melhorar o desempenho.
    
    Args:
        module_name: Nome do módulo para carregar (ex: 'pages.dashboard')
        
    Returns:
        O módulo carregado ou None se falhar
    """
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        st.error(f"Erro ao carregar módulo {module_name}: {str(e)}")
        return None

def load_page(page_name):
    """
    Carrega uma página específica com tratamento de erro.
    
    Args:
        page_name: Nome da página (ex: 'dashboard')
        
    Returns:
        O módulo da página ou um módulo substituto em caso de falha
    """
    module = load_module(f"pages.{page_name}")
    
    if module is None:
        # Criar um módulo substituto simples
        class EmergencyPage:
            @staticmethod
            def show():
                st.title(f"{page_name.capitalize()}")
                st.write("Esta página está temporariamente indisponível.")
                
        return EmergencyPage
    
    return module