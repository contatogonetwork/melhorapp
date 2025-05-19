import os
import sys
from pathlib import Path

def create_icon(name, content=None):
    """Cria um ícone SVG com o nome especificado se não existir."""
    icon_path = Path("resources/icons") / f"{name}.svg"
    
    # Criar diretório se não existir
    os.makedirs(icon_path.parent, exist_ok=True)
    
    # Se o ícone já existir, não sobrescreva
    if icon_path.exists():
        return
    
    # Se não foi especificado conteúdo, use um template padrão
    if content is None:
        content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2" fill="none">
    <rect x="2" y="2" width="20" height="20" rx="4" fill="#6272a4" opacity="0.7"/>
    <text x="50%" y="50%" font-family="Arial" font-size="7" fill="white" text-anchor="middle" dominant-baseline="middle">{name}</text>
</svg>"""
    
    # Escrever o conteúdo no arquivo
    with open(icon_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"Ícone criado: {name}")

# Criar ícones específicos para controle de janela
create_icon("minimize", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2">
    <line x1="5" y1="12" x2="19" y2="12" stroke="#fff" stroke-width="2"/>
</svg>""")

create_icon("maximize", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2">
    <rect x="5" y="5" width="14" height="14" rx="1" fill="none"/>
</svg>""")

create_icon("restore", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2">
    <rect x="7" y="9" width="10" height="10" rx="1" fill="none"/>
    <path d="M7 9V8C7 7.44772 7.44772 7 8 7H16C16.5523 7 17 7.44772 17 8V16C17 16.5523 16.5523 17 16 17H15" />
</svg>""")

create_icon("close", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2">
    <line x1="6" y1="6" x2="18" y2="18" stroke="#fff" stroke-width="2"/>
    <line x1="6" y1="18" x2="18" y2="6" stroke="#fff" stroke-width="2"/>
</svg>""")

create_icon("edit", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2">
    <path d="M17 3a2.85 2.85 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
</svg>""")

create_icon("view", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
    <circle cx="12" cy="12" r="3"/>
</svg>""")

create_icon("delete", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2">
    <path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M10 11v6M14 11v6"/>
</svg>""")

create_icon("add", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2">
    <line x1="12" y1="5" x2="12" y2="19" stroke="#fff" stroke-width="2"/>
    <line x1="5" y1="12" x2="19" y2="12" stroke="#fff" stroke-width="2"/>
</svg>""")

create_icon("arrow-down", """<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" stroke="#fff" stroke-width="2">
    <path d="M6 9l6 6 6-6"/>
</svg>""")

# Lista de todos os ícones necessários para o sistema
required_icons = [
    # Controle de janela (já criados acima)
    
    # Menu principal
    "menu", "dashboard", "calendar", "team", "document", "timeline", "video", 
    "delivery", "folder", "settings", "logout", "logo",
    
    # Dashboard
    "plus", "notification", "calendar-active", "delivery-today", "pending-edit", "approval",
    
    # Eventos
    "add-event", "event-details", "event-active", "date", "location", "client",
    
    # Equipe
    "user", "user-add", "client-add", "email", "phone", "role",
    
    # Outros ícones
    "save", "trash", "refresh", "export", "check", "download", "play",
    "fullscreen", "comment", "upload", "info", "more", "search", "filter",
    "image", "audio", "file", "video-file", "document-file", "cloud", 
]

# Criar todos os ícones necessários
for icon_name in required_icons:
    create_icon(icon_name)

print("Todos os ícones foram verificados/criados!")