import os
from pathlib import Path

def create_window_control_icons():
    """Cria os ícones necessários para os controles da janela (minimizar, maximizar, fechar)"""
    
    icons_path = Path("resources/icons")
    # Criar diretório se não existir
    icons_path.mkdir(parents=True, exist_ok=True)
    
    # Ícone minimizar
    minimize_icon = icons_path / "minimize.svg"
    if not minimize_icon.exists():
        with open(minimize_icon, "w", encoding="utf-8") as f:
            f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <line x1="5" y1="12" x2="19" y2="12" stroke="#FFFFFF" stroke-width="2"/>
            </svg>""")
    
    # Ícone maximizar
    maximize_icon = icons_path / "maximize.svg"
    if not maximize_icon.exists():
        with open(maximize_icon, "w", encoding="utf-8") as f:
            f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <rect x="5" y="5" width="14" height="14" stroke="#FFFFFF" stroke-width="2" fill="none"/>
            </svg>""")
    
    # Ícone restaurar
    restore_icon = icons_path / "restore.svg"
    if not restore_icon.exists():
        with open(restore_icon, "w", encoding="utf-8") as f:
            f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <rect x="7" y="9" width="10" height="10" stroke="#FFFFFF" stroke-width="2" fill="none"/>
                <path d="M7 9V8C7 7.44772 7.44772 7 8 7H16C16.5523 7 17 7.44772 17 8V16C17 16.5523 16.5523 17 16 17H15" stroke="#FFFFFF" stroke-width="2" fill="none"/>
            </svg>""")
    
    # Ícone fechar
    close_icon = icons_path / "close.svg"
    if not close_icon.exists():
        with open(close_icon, "w", encoding="utf-8") as f:
            f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24">
                <line x1="6" y1="6" x2="18" y2="18" stroke="#FFFFFF" stroke-width="2"/>
                <line x1="6" y1="18" x2="18" y2="6" stroke="#FFFFFF" stroke-width="2"/>
            </svg>""")
    
    print("Ícones de controle da janela criados com sucesso!")

# Executar a função para criar os ícones necessários
if __name__ == "__main__":
    create_window_control_icons()