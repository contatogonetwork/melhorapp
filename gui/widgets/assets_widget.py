from PySide6.QtCore import QPoint, QSize, Qt
from PySide6.QtGui import QAction, QIcon, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMenu,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class AssetCard(QFrame):
    def __init__(self, name, asset_type, file_path=""):
        super().__init__()

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
                padding: 10px;
            }}
            QFrame:hover {{
                background-color: {style.current_line_color};
            }}
        """
        )

        self.setFixedHeight(200)
        self.setFixedWidth(180)

        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(5)

        # Thumbnail/preview
        self.preview = QLabel()
        self.preview.setAlignment(Qt.AlignCenter)

        import os

        if asset_type == "Imagem" and file_path:
            # Se for uma imagem real, carrega-la
            pixmap = QPixmap(file_path).scaled(
                120,
                120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.preview.setPixmap(pixmap)
        else:
            # Determinar extensão e escolher ícone adequado
            ext = os.path.splitext(name)[-1].lower() if name else ""

            # Mapeamento por extensão
            if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff"]:
                icon_path = "./resources/icons/image.svg"
            elif ext in [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv"]:
                icon_path = "./resources/icons/video.svg"
            elif ext in [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a"]:
                icon_path = "./resources/icons/audio.svg"
            elif ext in [".pdf", ".doc", ".docx", ".txt", ".rtf", ".xls", ".xlsx"]:
                icon_path = "./resources/icons/document.svg"
            elif ext in [".psd", ".ai", ".fig", ".xd", ".sketch"]:
                icon_path = "./resources/icons/edit.svg"
            elif ext in [".zip", ".rar", ".7z", ".tar", ".gz"]:
                icon_path = "./resources/icons/archive.svg"
            elif ext in [".svg", ".eps", ".cdr"]:
                icon_path = "./resources/icons/logo.svg"
            else:
                icon_path = "./resources/icons/file.svg"

            icon = QIcon(icon_path)
            self.preview.setPixmap(icon.pixmap(QSize(64, 64)))

        self.preview.setFixedHeight(120)

        # Nome do asset
        self.name_label = QLabel(name)
        self.name_label.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 12px;"
        )
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)

        # Tipo do asset
        self.type_label = QLabel(asset_type)
        self.type_label.setStyleSheet(f"color: {style.comment_color}; font-size: 11px;")
        self.type_label.setAlignment(Qt.AlignCenter)

        # Layout para botões
        self.buttons_layout = QHBoxLayout()

        # Botão de download
        self.download_btn = QPushButton()
        self.download_btn.setIcon(QIcon("./resources/icons/download.svg"))
        self.download_btn.setIconSize(QSize(16, 16))
        self.download_btn.setFixedSize(28, 28)
        self.download_btn.setStyleSheet(style.secondary_button_style)

        # Botão de menu
        self.menu_btn = QPushButton()
        self.menu_btn.setIcon(QIcon("./resources/icons/more.svg"))
        self.menu_btn.setIconSize(QSize(16, 16))
        self.menu_btn.setFixedSize(28, 28)
        self.menu_btn.setStyleSheet(style.secondary_button_style)

        # Configurar o menu de contexto
        self.menu = QMenu(self)
        self.menu.setStyleSheet(
            f"""
            QMenu {{
                background-color: {style.background_color};
                color: {style.foreground_color};
                border: 1px solid {style.comment_color};
                border-radius: 5px;
            }}
            QMenu::item {{
                padding: 5px 20px;
            }}
            QMenu::item:selected {{
                background-color: {style.current_line_color};
            }}
        """
        )

        rename_action = QAction("Renomear", self)
        rename_action.setIcon(QIcon("./resources/icons/edit.svg"))

        delete_action = QAction("Excluir", self)
        delete_action.setIcon(QIcon("./resources/icons/trash.svg"))

        info_action = QAction("Informações", self)
        info_action.setIcon(QIcon("./resources/icons/info.svg"))

        self.menu.addAction(rename_action)
        self.menu.addAction(delete_action)
        self.menu.addSeparator()
        self.menu.addAction(info_action)

        self.menu_btn.clicked.connect(self.show_menu)

        # Adicionar botões ao layout
        self.buttons_layout.addWidget(self.download_btn)
        self.buttons_layout.addWidget(self.menu_btn)

        # Adicionar widgets ao layout principal
        self.layout.addWidget(self.preview)
        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.type_label)
        self.layout.addLayout(self.buttons_layout)

    def show_menu(self):
        self.menu.exec(self.menu_btn.mapToGlobal(QPoint(0, self.menu_btn.height())))


class AssetsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Cabeçalho
        self.header_layout = QHBoxLayout()

        # Título
        self.title_label = QLabel("Biblioteca de Assets")
        self.title_label.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 24px; font-weight: bold;"
        )

        # Seletor de evento
        self.event_selector = QComboBox()
        self.event_selector.setStyleSheet(style.combobox_style)
        self.event_selector.setFixedWidth(250)
        self.event_selector.setFixedHeight(36)
        self.event_selector.addItems(
            [
                "Festival de Música - 18-20 Mai 2025",
                "Lançamento de Produto - 25 Mai 2025",
                "Conferência Tech - 01 Jun 2025",
            ]
        )

        # Botão de upload
        self.upload_button = QPushButton("Upload")
        self.upload_button.setIcon(QIcon("./resources/icons/upload.svg"))
        self.upload_button.setStyleSheet(style.button_style)
        self.upload_button.setFixedHeight(36)

        # Adicionar ao layout do cabeçalho
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(QLabel("Evento:"))
        self.header_layout.addWidget(self.event_selector)
        self.header_layout.addWidget(self.upload_button)

        # Filtros e pesquisa
        self.filter_layout = QHBoxLayout()

        # Campo de pesquisa
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar assets...")
        self.search_input.setStyleSheet(style.input_style)
        self.search_input.setFixedHeight(36)

        # Filtro por tipo
        self.type_filter = QComboBox()
        self.type_filter.setStyleSheet(style.combobox_style)
        self.type_filter.setFixedHeight(36)
        self.type_filter.addItems(
            ["Todos os Tipos", "Imagem", "Vídeo", "Áudio", "Logo", "Outro"]
        )

        # Filtro por categoria
        self.category_filter = QComboBox()
        self.category_filter.setStyleSheet(style.combobox_style)
        self.category_filter.setFixedHeight(36)
        self.category_filter.addItems(
            [
                "Todas as Categorias",
                "Patrocinadores",
                "Artistas",
                "Mídia",
                "Templates",
            ]
        )

        # Adicionar filtros
        self.filter_layout.addWidget(self.search_input)
        self.filter_layout.addWidget(QLabel("Tipo:"))
        self.filter_layout.addWidget(self.type_filter)
        self.filter_layout.addWidget(QLabel("Categoria:"))
        self.filter_layout.addWidget(self.category_filter)

        # Área de conteúdo
        self.assets_scroll = QScrollArea()
        self.assets_scroll.setWidgetResizable(True)
        self.assets_scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """
        )

        # Container para assets
        self.assets_container = QWidget()
        self.assets_grid = QGridLayout(self.assets_container)
        self.assets_grid.setContentsMargins(0, 0, 0, 0)
        self.assets_grid.setSpacing(15)

        # Adicionar alguns assets de exemplo
        assets = [
            {"name": "Logo_Patrocinador_A.png", "type": "Logo"},
            {"name": "Logo_Patrocinador_B.svg", "type": "Logo"},
            {"name": "Palco_Principal.jpg", "type": "Imagem"},
            {"name": "Intro_Music.mp3", "type": "Áudio"},
            {"name": "Entrevista_Raw.mp4", "type": "Vídeo"},
            {"name": "Transições_Pack.zip", "type": "Outro"},
            {"name": "Identidade_Visual.pdf", "type": "Outro"},
            {"name": "Fundo_Apresentação.png", "type": "Imagem"},
            {"name": "Efeitos_Sonoros.wav", "type": "Áudio"},
            {"name": "Drone_Shot_01.mp4", "type": "Vídeo"},
            {"name": "Template_Stories.psd", "type": "Outro"},
            {"name": "Logo_Festival.ai", "type": "Logo"},
        ]

        row, col = 0, 0
        max_cols = 5

        for asset in assets:
            card = AssetCard(asset["name"], asset["type"])
            self.assets_grid.addWidget(card, row, col)

            col += 1
            if col >= max_cols:
                col = 0
                row += 1

        self.assets_scroll.setWidget(self.assets_container)

        # Adicionar todos os layouts ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addLayout(self.filter_layout)
        self.layout.addWidget(self.assets_scroll)
