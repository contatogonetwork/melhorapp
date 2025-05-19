import os

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class VideoPlayerComponent(QWidget):
    """Componente de player de vídeo com controles"""

    positionUpdated = Signal(
        int
    )  # Sinal para notificar a posição atual do vídeo
    fullscreenToggled = Signal(
        bool
    )  # Sinal para notificar mudanças no estado de tela cheia

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.setupConnections()
        self.currentPosition = 0
        self.is_fullscreen = False

    def setupUi(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Widget de vídeo
        self.videoWidget = QVideoWidget()
        self.layout.addWidget(self.videoWidget)

        # Player e audio
        self.mediaPlayer = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.mediaPlayer.setAudioOutput(self.audioOutput)
        self.mediaPlayer.setVideoOutput(self.videoWidget)

        # Controles
        self.controlLayout = QHBoxLayout()

        # Botão Play/Pause
        self.playButton = QPushButton()
        self.playButton.setIcon(
            QIcon(os.path.join("resources", "icons", "play.svg"))
        )
        self.playButton.setFixedSize(32, 32)
        self.playButton.setObjectName("playButton")
        self.playButton.setStyleSheet(style.btn_secondary)
        self.playButton.setCursor(Qt.CursorShape.PointingHandCursor)

        # Slider de tempo
        self.timeSlider = QSlider(Qt.Horizontal)
        self.timeSlider.setRange(0, 0)
        self.timeSlider.setObjectName("timeSlider")

        # Label de tempo
        self.timeLabel = QLabel("00:00 / 00:00")
        self.timeLabel.setObjectName("timeLabel")

        # Adiciona controles ao layout
        self.controlLayout.addWidget(self.playButton)
        self.controlLayout.addWidget(self.timeSlider)
        self.controlLayout.addWidget(self.timeLabel)

        self.layout.addLayout(self.controlLayout)

    def setupConnections(self):
        self.playButton.clicked.connect(self.togglePlayPause)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.timeSlider.sliderMoved.connect(self.setPosition)

    @Slot()
    def togglePlayPause(self):
        if (
            self.mediaPlayer.playbackState()
            == QMediaPlayer.PlaybackState.PlayingState
        ):
            self.mediaPlayer.pause()
            self.playButton.setIcon(
                QIcon(os.path.join("resources", "icons", "play.svg"))
            )
        else:
            self.mediaPlayer.play()
            self.playButton.setIcon(
                QIcon(os.path.join("resources", "icons", "pause.svg"))
            )

    @Slot(int)
    def positionChanged(self, position):
        self.timeSlider.setValue(position)
        current = self.formatTime(position)
        total = self.formatTime(self.mediaPlayer.duration())
        self.timeLabel.setText(f"{current} / {total}")
        self.currentPosition = position
        self.positionUpdated.emit(
            position
        )  # Emite o sinal com a posição atual

    @Slot(int)
    def durationChanged(self, duration):
        self.timeSlider.setRange(0, duration)
        total = self.formatTime(duration)
        current = self.formatTime(0)
        self.timeLabel.setText(f"{current} / {total}")

    @Slot(int)
    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def setSource(self, url):
        """Define a fonte do vídeo para reprodução"""
        self.mediaPlayer.setSource(url)

    def getCurrentTime(self):
        """Retorna a posição atual em milissegundos"""
        return self.mediaPlayer.position()

    def formatTime(self, ms):
        """Formata milissegundos para MM:SS"""
        s = ms // 1000
        m = s // 60
        s = s % 60
        return f"{m:02d}:{s:02d}"

    def setPlaybackRate(self, rate):
        """Define a velocidade de reprodução do vídeo"""
        self.mediaPlayer.setPlaybackRate(rate)

    def jumpToPosition(self, position):
        """Salta para uma posição específica no vídeo em milissegundos"""
        self.mediaPlayer.setPosition(position)
        # Atualiza o slider e a etiqueta de tempo
        self.timeSlider.setValue(position)
        current = self.formatTime(position)
        total = self.formatTime(self.mediaPlayer.duration())
        self.timeLabel.setText(f"{current} / {total}")

    @Slot()
    def toggle_fullscreen(self):
        """Alterna entre os modos de tela cheia e janela"""
        if self.is_fullscreen:
            self.setWindowState(self.windowState() & ~Qt.WindowFullScreen)
            self.is_fullscreen = False
            self.fullscreenToggled.emit(False)
        else:
            self.setWindowState(self.windowState() | Qt.WindowFullScreen)
            self.is_fullscreen = True
            self.fullscreenToggled.emit(True)
