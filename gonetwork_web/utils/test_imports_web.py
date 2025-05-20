"""
Script para testar a importação de módulos essenciais na versão web
"""
import sys
import os
import importlib

def test_import(module_name, show_success=True):
    """Testa se um módulo pode ser importado corretamente."""
    try:
        module = importlib.import_module(module_name)
        if show_success:
            print(f"✅ {module_name}: Importado com sucesso")
        return True
    except Exception as e:
        print(f"❌ {module_name}: {str(e)}")
        return False

def test_all_imports():
    """Testa todos os imports críticos para a aplicação web."""
    print("\n=== Testando Imports Necessários para GoNetwork Web ===\n")
    
    # Dependências Streamlit
    test_import("streamlit")
    test_import("streamlit_option_menu")
    test_import("streamlit_authenticator")
    
    # Processamento de dados
    test_import("pandas")
    test_import("numpy")
    
    # Visualização
    test_import("plotly.express")
    test_import("matplotlib.pyplot")
    
    # Utilitários
    test_import("yaml")
    test_import("requests")
    test_import("PIL")
    
    # Módulos PySide6 (opcional para compatibilidade)
    print("\n--- Dependências PySide6 (Opcionais) ---")
    try:
        test_import("PySide6.QtCore")
        test_import("PySide6.QtWidgets")
        test_import("PySide6.QtGui")
        
        # Testar módulos multimídia especificamente
        test_import("PySide6.QtMultimedia")
        test_import("PySide6.QtMultimediaWidgets")
    except Exception:
        print("PySide6 não está disponível, mas não é crítico para a versão web")
    
    # Módulos personalizados da aplicação web
    print("\n--- Módulos Internos ---")
    test_import("utils.database")
    test_import("utils.state_management")
    test_import("utils.notifications")
    
    print("\n=== Teste de Imports Concluído ===\n")

if __name__ == "__main__":
    # Adicionar diretório raiz ao PYTHONPATH
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)
    
    test_all_imports()
