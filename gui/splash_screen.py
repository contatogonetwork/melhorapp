from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QFont, QLinearGradient, QPainter, QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QSplashScreen,
    QVBoxLayout,
    QWidget,
)


class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # Configuração do tamanho
        self.setFixedSize(600, 400)

        # Widget central com layout
        self.central_widget = QWidget(self)
        self.central_widget.setFixedSize(self.size())

        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        self.layout.setAlignment(Qt.AlignCenter)

        # Logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setText(
            "GoNetwork AI"
        )  # Placeholder até termos um logo real
        self.logo_label.setStyleSheet(
            """
            color: #FFFFFF;
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
        """
        )

        # Descrição
        self.description_label = QLabel(
            "Sistema Integrado de Gerenciamento Audiovisual"
        )
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setStyleSheet(
            """
            color: #CCCCCC;
            font-size: 16px;
            margin-bottom: 30px;
        """
        )

        # Barra de progresso
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #303030;
                border-radius: 2px;
            }
            
            QProgressBar::chunk {
                background-color: #BD93F9;
                border-radius: 2px;
            }
        """
        )

        # Adicionar widgets ao layout
        self.layout.addStretch()
        self.layout.addWidget(self.logo_label)
        self.layout.addWidget(self.description_label)
        self.layout.addStretch()
        self.layout.addWidget(self.progress_bar)

        # Iniciar animação de progresso
        self._progress_counter = 0
        self._progress_timer = self.startTimer(30)

    def timerEvent(self, event):
        self._progress_counter += 1
        self.progress_bar.setValue(self._progress_counter)

        if self._progress_counter >= 100:
            self.killTimer(self._progress_timer)

    def paintEvent(self, event):
        # Criar o painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Desenhar o gradiente de fundo
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#021E33"))
        gradient.setColorAt(1, QColor("#000000"))

        painter.fillRect(self.rect(), gradient)

        # Desenhar partículas (simulando fluxo de trabalho visual)
        painter.setPen(QColor(255, 255, 255, 50))
        for i in range(20):
            x = (self._progress_counter * 3 + i * 30) % self.width()
            y = (self._progress_counter * 2 + i * 25) % self.height()
            size = (i % 5) + 1
            painter.drawEllipse(x, y, size, size)
