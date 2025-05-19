import os

# Lista ampliada de ícones necessários
icons = [
    # Ícones de navegação e controle de janela
    "menu",
    "minimize",
    "maximize",
    "close",
    "dashboard",
    "calendar",
    "team",
    "document",
    "timeline",
    "video",
    "delivery",
    "folder",
    "settings",
    "logout",
    "restore",
    "arrow-down",
    # Ícones de status e indicadores
    "calendar-active",
    "delivery-today",
    "pending-edit",
    "approval",
    # Ícones de ações
    "plus",
    "edit",
    "view",
    "add-event",
    "user",
    "timeline-generate",
    "save",
    "trash",
    "refresh",
    "export",
    "check",
    "download",
    "play",
    "fullscreen",
    "comment",
    "upload",
    "info",
    "more",
    # Tipos de arquivos e assets
    "image",
    "video",
    "audio",
    "logo",
    "file",
]

# Garantir que o diretório de ícones exista
icons_dir = os.path.join("resources", "icons")
os.makedirs(icons_dir, exist_ok=True)

# Criar ícones SVG básicos
for icon_name in icons:
    icon_path = os.path.join(icons_dir, f"{icon_name}.svg")

    # Se o arquivo não existir, criar um SVG básico
    if not os.path.exists(icon_path):
        print(f"Criando ícone: {icon_name}.svg")

        # Criar um SVG básico para cada ícone
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="2" width="20" height="20" rx="5" fill="#BD93F9" opacity="0.5"/>
        <text x="50%" y="50%" font-family="Arial" font-size="8" text-anchor="middle" alignment-baseline="middle" fill="white">{icon_name}</text>
</svg>"""

        # Escrever o conteúdo no arquivo
        with open(icon_path, "w") as f:
            f.write(svg_content)
    else:
        print(f"Ícone já existe: {icon_name}.svg")

print("Ícones criados com sucesso!")

# Criar diretório de imagens e um avatar padrão
images_dir = os.path.join("resources", "images")
os.makedirs(images_dir, exist_ok=True)

# Criar um arquivo SVG para o avatar padrão
avatar_path = os.path.join(images_dir, "default_avatar.png")
if not os.path.exists(avatar_path):
    # Criando um SVG simples para o avatar
    avatar_svg_path = os.path.join(images_dir, "default_avatar.svg")
    with open(avatar_svg_path, "w") as f:
        f.write(
            """<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="50" fill="#3D4058"/>
    <text x="50%" y="50%" font-family="Arial" font-size="40" text-anchor="middle" alignment-baseline="middle" fill="#BD93F9">U</text>
</svg>"""
        )

    print("Avatar padrão criado como SVG. Convertendo para PNG é recomendado.")

    # Tentar converter para PNG se pillow estiver instalado
    try:
        from PIL import Image, ImageDraw

        # Criar uma imagem simples para o avatar
        img = Image.new("RGB", (100, 100), color="#3D4058")
        d = ImageDraw.Draw(img)

        # Adicionar um texto no centro
        d.text((50, 50), "U", fill="#BD93F9", anchor="mm")

        # Salvar a imagem
        img.save(avatar_path)
        print(f"Avatar PNG criado: {avatar_path}")
    except ImportError:
        print("Pillow não está instalado. O avatar permanecerá como SVG.")
else:
    print(f"Avatar já existe: {avatar_path}")
