from PySide6.QtCore import QPoint, QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QScrollArea,
    QSlider,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class VideoPlayer(QFrame):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: #000000;
                border-radius: 8px;
            }}
        """
        )

        # Layout principal
        self.layout = QVBoxLayout(self)

        # Placeholder para o vídeo (no momento apenas uma imagem)
        self.video_placeholder = QLabel()
        self.video_placeholder.setAlignment(Qt.AlignCenter)
        self.video_placeholder.setText("PLAYER DE VÍDEO\n(Placeholder)")
        self.video_placeholder.setStyleSheet(
            f"""
            color: {style.foreground_color};
            background-color: #111111;
            font-size: 20px;
            border-radius: 8px;
        """
        )
        self.video_placeholder.setMinimumHeight(300)

        # Controles de vídeo
        self.controls_layout = QHBoxLayout()

        # Botão de play/pause
        self.play_button = QPushButton()
        self.play_button.setIcon(QIcon("./resources/icons/play.svg"))
        self.play_button.setIconSize(QSize(20, 20))
        self.play_button.setFixedSize(36, 36)
        self.play_button.setStyleSheet(style.secondary_button_style)

        # Timeline do vídeo
        self.timeline = QSlider(Qt.Horizontal)
        self.timeline.setStyleSheet(
            f"""
            QSlider::groove:horizontal {{
                border: none;
                height: 6px;
                background: {style.current_line_color};
                margin: 0px;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {style.purple_color};
                border: none;
                width: 12px;
                height: 12px;
                margin: -3px 0;
                border-radius: 6px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {style.pink_color};
            }}
        """
        )

        # Tempo atual / Duração
        self.time_label = QLabel("00:00 / 03:45")
        self.time_label.setStyleSheet(f"color: {style.foreground_color};")

        # Botão de tela cheia
        self.fullscreen_button = QPushButton()
        self.fullscreen_button.setIcon(
            QIcon("./resources/icons/fullscreen.svg")
        )
        self.fullscreen_button.setIconSize(QSize(16, 16))
        self.fullscreen_button.setFixedSize(36, 36)
        self.fullscreen_button.setStyleSheet(style.secondary_button_style)

        # Adicionar controles ao layout
        self.controls_layout.addWidget(self.play_button)
        self.controls_layout.addWidget(self.timeline)
        self.controls_layout.addWidget(self.time_label)
        self.controls_layout.addWidget(self.fullscreen_button)

        # Adicionar widgets ao layout principal
        self.layout.addWidget(self.video_placeholder)
        self.layout.addLayout(self.controls_layout)


class CommentItem(QFrame):
    def __init__(self, user, timestamp, text):
        super().__init__()

        self.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.current_line_color};
                border-radius: 8px;
                padding: 5px;
                margin: 5px 0px;
            }}
        """
        )

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # Cabeçalho (usuário e timestamp)
        self.header_layout = QHBoxLayout()

        # Usuário
        self.user_label = QLabel(user)
        self.user_label.setStyleSheet(
            f"""
            color: {style.cyan_color};
            font-weight: bold;
        """
        )

        # Timestamp
        self.timestamp_label = QLabel(timestamp)
        self.timestamp_label.setStyleSheet(
            f"""
            color: {style.comment_color};
            font-size: 11px;
        """
        )

        self.header_layout.addWidget(self.user_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.timestamp_label)

        # Texto do comentário
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet(
            f"""
            color: {style.foreground_color};
            font-size: 13px;
        """
        )
        self.text_label.setWordWrap(True)

        # Ações (responder, etc)
        self.actions_layout = QHBoxLayout()

        self.reply_button = QPushButton("Responder")
        self.reply_button.setFlat(True)
        self.reply_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.reply_button.setStyleSheet(
            f"""
            QPushButton {{
                color: {style.purple_color};
                background: transparent;
                border: none;
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: {style.pink_color};
                text-decoration: underline;
            }}
        """
        )

        self.actions_layout.addWidget(self.reply_button)
        self.actions_layout.addStretch()

        # Adicionar layouts ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.text_label)
        self.layout.addLayout(self.actions_layout)


class EditingWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Cabeçalho
        self.header_layout = QHBoxLayout()

        # Título
        self.title_label = QLabel("Edição e Aprovação")
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

        # Adicionar ao layout do cabeçalho
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(QLabel("Evento:"))
        self.header_layout.addWidget(self.event_selector)

        # Splitter principal (lista de vídeos e área do editor)
        self.main_splitter = QSplitter(Qt.Horizontal)

        # Lista de vídeos à esquerda
        self.videos_widget = QFrame()
        self.videos_widget.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
                padding: 5px;
            }}
        """
        )
        self.videos_widget.setMinimumWidth(250)
        self.videos_widget.setMaximumWidth(400)

        self.videos_layout = QVBoxLayout(self.videos_widget)

        # Título da lista
        self.videos_title = QLabel("Entregas")
        self.videos_title.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 16px; font-weight: bold;"
        )

        # Campo de pesquisa
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar entregas...")
        self.search_input.setStyleSheet(style.input_style)

        # Lista de vídeos
        self.videos_list = QListWidget()
        self.videos_list.setStyleSheet(
            f"""
            QListWidget {{
                background-color: {style.background_color};
                border-radius: 5px;
                border: 1px solid {style.current_line_color};
            }}
            QListWidget::item {{
                padding: 10px;
                border-bottom: 1px solid {style.current_line_color};
            }}
            QListWidget::item:selected {{
                background-color: {style.current_line_color};
            }}
        """
        )

        # Adicionar itens de exemplo
        items = [
            "Abertura - Festival de Música",
            "Entrevista - Artista Principal",
            "Patrocinador A - Ativação",
            "Teaser - Divulgação",
        ]

        for item in items:
            self.videos_list.addItem(item)

        # Adicionar widgets à lista
        self.videos_layout.addWidget(self.videos_title)
        self.videos_layout.addWidget(self.search_input)
        self.videos_layout.addWidget(self.videos_list)

        # Área do editor à direita
        self.editor_widget = QFrame()
        self.editor_widget.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
            }}
        """
        )

        self.editor_layout = QVBoxLayout(self.editor_widget)

        # Título do vídeo atual
        self.video_title = QLabel("Abertura - Festival de Música")
        self.video_title.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 18px; font-weight: bold;"
        )

        # Detalhes do vídeo
        self.details_layout = QHBoxLayout()

        self.status_label = QLabel("Status: Em Revisão")
        self.status_label.setStyleSheet(
            f"""
            color: {style.orange_color};
            background-color: {style.current_line_color};
            padding: 5px 10px;
            border-radius: 10px;
        """
        )

        self.editor_label = QLabel("Editor: Maria Souza")
        self.editor_label.setStyleSheet(
            f"""
            color: {style.foreground_color};
        """
        )

        self.version_label = QLabel("Versão: 2.1")
        self.version_label.setStyleSheet(
            f"""
            color: {style.foreground_color};
        """
        )

        self.details_layout.addWidget(self.status_label)
        self.details_layout.addWidget(self.editor_label)
        self.details_layout.addWidget(self.version_label)
        self.details_layout.addStretch()

        # Botões de ação
        self.actions_layout = QHBoxLayout()

        self.approve_button = QPushButton("Aprovar")
        self.approve_button.setIcon(QIcon("./resources/icons/check.svg"))
        self.approve_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: #50FA7B;
                color: #000000;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #70FF9B;
            }}
        """
        )

        self.reject_button = QPushButton("Solicitar Ajustes")
        self.reject_button.setIcon(QIcon("./resources/icons/edit.svg"))
        self.reject_button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {style.orange_color};
                color: #000000;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #FFD88C;
            }}
        """
        )

        self.download_button = QPushButton("Download")
        self.download_button.setIcon(QIcon("./resources/icons/download.svg"))
        self.download_button.setStyleSheet(style.secondary_button_style)

        self.actions_layout.addWidget(self.approve_button)
        self.actions_layout.addWidget(self.reject_button)
        self.actions_layout.addStretch()
        self.actions_layout.addWidget(self.download_button)

        # Player de vídeo
        self.player = VideoPlayer()

        # Comentários
        self.comments_title = QLabel("Comentários")
        self.comments_title.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 16px; font-weight: bold;"
        )

        # Lista de comentários
        self.comments_scroll = QScrollArea()
        self.comments_scroll.setWidgetResizable(True)
        self.comments_scroll.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """
        )

        self.comments_container = QWidget()
        self.comments_layout = QVBoxLayout(self.comments_container)
        self.comments_layout.setContentsMargins(0, 0, 0, 0)
        self.comments_layout.setSpacing(10)

        # Comentários de exemplo
        self.comments_layout.addWidget(
            CommentItem(
                "Ana Costa",
                "Hoje, 15:30",
                "O áudio está um pouco baixo na introdução. Pode aumentar o volume nos primeiros 15 segundos?",
            )
        )
        self.comments_layout.addWidget(
            CommentItem(
                "Carlos Lima",
                "Hoje, 16:05",
                "Gostei muito da transição aos 0:45, ficou muito suave!",
            )
        )
        self.comments_layout.addWidget(
            CommentItem(
                "Cliente XYZ",
                "Hoje, 16:20",
                "A logomarca do patrocinador precisa ficar mais tempo em tela, pelo menos 3 segundos.",
            )
        )

        self.comments_layout.addStretch()
        self.comments_scroll.setWidget(self.comments_container)

        # Campo para novo comentário
        self.new_comment = QTextEdit()
        self.new_comment.setStyleSheet(style.input_style)
        self.new_comment.setPlaceholderText("Escreva um comentário...")
        self.new_comment.setMaximumHeight(80)

        self.comment_button = QPushButton("Comentar")
        self.comment_button.setIcon(QIcon("./resources/icons/comment.svg"))
        self.comment_button.setStyleSheet(style.button_style)

        self.comment_layout = QHBoxLayout()
        self.comment_layout.addWidget(self.new_comment)
        self.comment_layout.addWidget(self.comment_button)

        # Adicionar widgets ao layout do editor
        self.editor_layout.addWidget(self.video_title)
        self.editor_layout.addLayout(self.details_layout)
        self.editor_layout.addLayout(self.actions_layout)
        self.editor_layout.addWidget(self.player)
        self.editor_layout.addWidget(self.comments_title)
        self.editor_layout.addWidget(self.comments_scroll)
        self.editor_layout.addLayout(self.comment_layout)

        # Adicionar widgets ao splitter
        self.main_splitter.addWidget(self.videos_widget)
        self.main_splitter.addWidget(self.editor_widget)
        self.main_splitter.setStretchFactor(
            1, 2
        )  # Dar mais espaço para o editor

        # Adicionar todos os layouts ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.main_splitter)
