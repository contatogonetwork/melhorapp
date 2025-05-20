"""
Widget para exibir marcadores de comentários na timeline de um vídeo
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor, QPainter
from PySide6.QtWidgets import QWidget


class CommentMarkerWidget(QWidget):
    """Widget para representar marcadores de comentários na timeline do vídeo"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.comments = []
        self.video_duration = 0
        self.setFixedHeight(10)

    def set_comments(self, comments):
        """Define os comentários a serem exibidos"""
        self.comments = comments
        self.update()

    def set_duration(self, duration):
        """Define a duração total do vídeo em ms"""
        self.video_duration = max(1, duration)  # Evitar divisão por zero
        self.update()

    def paintEvent(self, event):
        """Desenha os marcadores na timeline"""
        if not self.comments or self.video_duration <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dimensões do widget
        width = self.width()
        height = self.height()

        # Cor para comentários normais (azul)
        normal_color = QColor(51, 153, 255)

        # Cor para comentários resolvidos (verde)
        resolved_color = QColor(102, 204, 102)

        # Desenhar marcadores para cada comentário
        for comment in self.comments:
            # Calcular posição relativa
            position = comment.video_timestamp / self.video_duration
            x_pos = int(position * width)

            # Selecionar cor com base no status
            if comment.is_resolved:
                color = resolved_color
            else:
                color = normal_color

            # Desenhar marcador
            painter.setBrush(QBrush(color))
            painter.setPen(Qt.NoPen)

            # Desenhar um pequeno retângulo
            marker_width = 2
            painter.drawRect(x_pos - marker_width // 2, 0, marker_width, height)
