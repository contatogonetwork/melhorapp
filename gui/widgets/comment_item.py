from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class CommentItem(QWidget):
    """Widget para exibir um comentário de vídeo com controles de interação"""

    goToTimestampRequested = Signal(int)
    resolveRequested = Signal(str)  # ID do comentário

    def __init__(self, comment, is_editor=False, parent=None):
        super().__init__(parent)
        self.comment = comment
        self.is_editor = is_editor
        self.is_active = False  # Estado para controlar se o comentário está ativo (baseado no tempo do vídeo)
        self.setupUi()

    def setupUi(self):
        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 5)

        # Info do comentário (autor, timestamp)
        self.infoLayout = QHBoxLayout()

        self.authorLabel = QLabel(self.comment.author)
        self.authorLabel.setObjectName("authorLabel")
        self.authorLabel.setStyleSheet("font-weight: bold;")

        # Formata o timestamp do vídeo como MM:SS
        video_seconds = self.comment.video_timestamp // 1000
        video_mins = video_seconds // 60
        video_secs = video_seconds % 60
        timestamp_str = f"{video_mins:02d}:{video_secs:02d}"

        self.timestampLabel = QLabel(f"em {timestamp_str}")
        self.timestampLabel.setObjectName("timestampLabel")

        self.infoLayout.addWidget(self.authorLabel)
        self.infoLayout.addWidget(self.timestampLabel)
        self.infoLayout.addStretch()

        # Botões de ação
        self.goToButton = QPushButton("Ir para momento")
        self.goToButton.setObjectName("goToButton")
        self.goToButton.setStyleSheet(style.btn_secondary)
        self.goToButton.setCursor(Qt.PointingHandCursor)
        self.goToButton.clicked.connect(self.onGoToTimestamp)

        self.infoLayout.addWidget(self.goToButton)

        # Conteúdo do comentário
        self.contentLabel = QLabel(self.comment.text)
        self.contentLabel.setWordWrap(True)
        self.contentLabel.setObjectName("contentLabel")
        self.contentLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)

        # Layout para marcar como resolvido (apenas para editores)
        self.resolveLayout = QHBoxLayout()
        if self.is_editor and not self.comment.is_resolved:
            self.resolveButton = QPushButton("Marcar como resolvido")
            self.resolveButton.setObjectName("resolveButton")
            self.resolveButton.setStyleSheet(style.btn_primary)
            self.resolveButton.setCursor(Qt.PointingHandCursor)
            self.resolveButton.clicked.connect(self.onResolveRequested)
            self.resolveLayout.addStretch()
            self.resolveLayout.addWidget(self.resolveButton)
        elif self.comment.is_resolved:
            self.resolvedLabel = QLabel("✓ Resolvido")
            self.resolvedLabel.setObjectName("resolvedLabel")
            self.resolvedLabel.setStyleSheet(f"color: {style.SUCCESS};")
            self.resolveLayout.addStretch()
            self.resolveLayout.addWidget(self.resolvedLabel)

        # Adiciona tudo ao layout principal
        main_layout.addLayout(self.infoLayout)
        main_layout.addWidget(self.contentLabel)
        main_layout.addLayout(self.resolveLayout)

        # Estilo inicial
        self.updateAppearance()

    def onGoToTimestamp(self):
        """Emite sinal para ir para o timestamp do vídeo"""
        self.goToTimestampRequested.emit(self.comment.video_timestamp)
        # Destaca automaticamente o comentário quando clicado
        self.setActive(True)

    def onResolveRequested(self):
        """Emite sinal para marcar o comentário como resolvido"""
        self.resolveRequested.emit(self.comment.id)

    def setActive(self, active=True):
        """Define se o comentário está ativo (atual no vídeo)"""
        if active != self.is_active:
            self.is_active = active
            self.updateAppearance()

    def updateAppearance(self):
        """Atualiza a aparência do comentário com base em seu estado"""
        if self.is_active:
            # Comentário ativo - destaque especial
            self.setStyleSheet(
                f"background-color: {style.PRIMARY_LIGHT}; "
                f"border-left: 3px solid {style.PRIMARY}; "
                f"border-radius: 5px; padding: 10px; margin-bottom: 5px;"
            )
        elif self.comment.is_resolved:
            # Comentário resolvido - estilo mais suave
            self.setStyleSheet(
                f"background-color: {style.BG_THREE}; "
                f"border-left: 3px solid {style.SUCCESS}; "
                f"border-radius: 5px; padding: 10px; margin-bottom: 5px; "
                f"color: {style.FONT_COLOR};"
            )
        else:
            # Comentário normal
            self.setStyleSheet(
                f"background-color: {style.BG_THREE}; "
                f"border-radius: 5px; padding: 10px; margin-bottom: 5px;"
            )
