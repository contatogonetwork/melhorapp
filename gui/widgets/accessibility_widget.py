#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Widget de configurações de acessibilidade.

Este módulo fornece um widget para permitir que os usuários configurem
as opções de acessibilidade do aplicativo.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from utils.accessibility import AccessibilityManager, ColorScheme, FontSize
from utils.logger import get_logger

# Configurar logger
logger = get_logger("gui.widgets.accessibility")


class AccessibilitySettingsWidget(QWidget):
    """Widget para configurações de acessibilidade."""

    def __init__(self, parent=None):
        """
        Inicializa o widget de configurações de acessibilidade.

        Args:
            parent: Widget pai
        """
        super().__init__(parent)

        self.accessibility_manager = AccessibilityManager()

        self.setup_ui()
        self.load_current_settings()
        self.setup_connections()

        # Configurar este widget para ser acessível
        self.setAccessibleName("Configurações de Acessibilidade")
        self.setAccessibleDescription(
            "Widget para configurar opções de acessibilidade do aplicativo"
        )

    def setup_ui(self):
        """Configura a interface do widget."""
        # Layout principal
        main_layout = QVBoxLayout(self)

        # Grupo de tamanho de fonte
        font_group = QGroupBox("Tamanho da Fonte")
        font_layout = QGridLayout(font_group)

        font_layout.addWidget(QLabel("Pequena"), 0, 0)

        self.font_slider = QSlider(Qt.Horizontal)
        self.font_slider.setMinimum(0)  # FontSize.SMALL
        self.font_slider.setMaximum(3)  # FontSize.X_LARGE
        self.font_slider.setPageStep(1)
        self.font_slider.setTickPosition(QSlider.TicksBelow)
        self.font_slider.setTickInterval(1)

        font_layout.addWidget(self.font_slider, 0, 1)
        font_layout.addWidget(QLabel("Extra Grande"), 0, 2)

        # Botões de exemplo
        example_label = QLabel("Texto de exemplo")
        example_label.setFont(QFont("Arial", 12))
        font_layout.addWidget(example_label, 1, 0, 1, 3)

        main_layout.addWidget(font_group)

        # Grupo de esquema de cores
        color_group = QGroupBox("Esquema de Cores")
        color_layout = QVBoxLayout(color_group)

        self.color_combo = QComboBox()
        self.color_combo.addItem("Normal", ColorScheme.NORMAL.value)
        self.color_combo.addItem("Alto Contraste", ColorScheme.HIGH_CONTRAST.value)
        self.color_combo.addItem("Escuro", ColorScheme.DARK.value)
        self.color_combo.addItem("Claro", ColorScheme.LIGHT.value)

        color_layout.addWidget(self.color_combo)
        main_layout.addWidget(color_group)

        # Grupo de opções adicionais
        options_group = QGroupBox("Opções Adicionais")
        options_layout = QVBoxLayout(options_group)

        self.screen_reader_cb = QCheckBox("Modo para leitores de tela")
        self.screen_reader_cb.setToolTip(
            "Ativa recursos para melhor compatibilidade com leitores de tela"
        )

        self.keyboard_cb = QCheckBox("Atalhos de teclado")
        self.keyboard_cb.setToolTip("Ativa navegação completa por teclado")

        options_layout.addWidget(self.screen_reader_cb)
        options_layout.addWidget(self.keyboard_cb)

        main_layout.addWidget(options_group)

        # Botões de ação
        self.apply_btn = QPushButton("Aplicar")
        self.apply_btn.setIcon(QIcon(":/icons/apply"))

        self.reset_btn = QPushButton("Restaurar Padrões")
        self.reset_btn.setIcon(QIcon(":/icons/reset"))

        buttons_layout = QGridLayout()
        buttons_layout.addWidget(self.apply_btn, 0, 0)
        buttons_layout.addWidget(self.reset_btn, 0, 1)

        main_layout.addLayout(buttons_layout)
        main_layout.addStretch()

    def load_current_settings(self):
        """Carrega as configurações atuais nos controles."""
        # Tamanho da fonte
        current_font_size = self.accessibility_manager.get_font_size()
        self.font_slider.setValue(current_font_size.value)

        # Esquema de cores
        current_color_scheme = self.accessibility_manager.get_color_scheme()
        index = self.color_combo.findData(current_color_scheme.value)
        if index >= 0:
            self.color_combo.setCurrentIndex(index)

        # Modo para leitores de tela
        self.screen_reader_cb.setChecked(
            self.accessibility_manager.is_screen_reader_mode_enabled()
        )

    def setup_connections(self):
        """Configura as conexões de sinais e slots."""
        self.apply_btn.clicked.connect(self.apply_settings)
        self.reset_btn.clicked.connect(self.reset_settings)

        # Atualizar texto de exemplo quando o tamanho da fonte muda
        self.font_slider.valueChanged.connect(self.update_example_text)

    def apply_settings(self):
        """Aplica as configurações selecionadas."""
        # Tamanho da fonte
        font_size = FontSize(self.font_slider.value())
        self.accessibility_manager.set_font_size(font_size)

        # Esquema de cores
        color_scheme_value = self.color_combo.currentData()
        color_scheme = ColorScheme(color_scheme_value)
        self.accessibility_manager.set_color_scheme(color_scheme)

        # Modo para leitores de tela
        screen_reader_mode = self.screen_reader_cb.isChecked()
        self.accessibility_manager.set_screen_reader_mode(screen_reader_mode)

        logger.info("Configurações de acessibilidade aplicadas")

    def reset_settings(self):
        """Restaura as configurações padrão."""
        self.font_slider.setValue(FontSize.NORMAL.value)

        index = self.color_combo.findData(ColorScheme.NORMAL.value)
        if index >= 0:
            self.color_combo.setCurrentIndex(index)

        self.screen_reader_cb.setChecked(False)
        self.keyboard_cb.setChecked(True)

        self.apply_settings()
        logger.info("Configurações de acessibilidade restauradas para os padrões")

    def update_example_text(self, value):
        """
        Atualiza o texto de exemplo com o tamanho de fonte selecionado.

        Args:
            value: Valor do slider
        """
        # Encontrar o QLabel de exemplo
        for i in range(self.layout().count()):
            item = self.layout().itemAt(i)
            if item.widget() and isinstance(item.widget(), QGroupBox):
                group_box = item.widget()
                if group_box.title() == "Tamanho da Fonte":
                    # Procurar o QLabel no layout do grupo
                    for j in range(group_box.layout().count()):
                        inner_item = group_box.layout().itemAt(j)
                        if (
                            inner_item.widget()
                            and isinstance(inner_item.widget(), QLabel)
                            and inner_item.widget().text() == "Texto de exemplo"
                        ):
                            label = inner_item.widget()

                            # Ajustar tamanho da fonte
                            font_sizes = [
                                9,
                                12,
                                15,
                                18,
                            ]  # tamanhos para SMALL, NORMAL, LARGE, X_LARGE
                            font = label.font()
                            font.setPointSize(font_sizes[value])
                            label.setFont(font)
                            break
