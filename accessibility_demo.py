#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de demonstração das funcionalidades de acessibilidade.

Este script mostra como usar os recursos de acessibilidade implementados
no aplicativo GoNetwork AI.
"""

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.resolve()))

from gui.widgets.accessibility_widget import AccessibilitySettingsWidget
from utils.accessibility import (
    AccessibilityManager,
    ColorScheme,
    FontSize,
    add_keyboard_shortcut,
    make_widget_accessible,
)
from utils.logger import get_logger

# Configurar logger
logger = get_logger("accessibility_demo")


class AccessibilityDemoWindow(QMainWindow):
    """Janela de demonstração das funcionalidades de acessibilidade."""

    def __init__(self):
        """Inicializa a janela de demonstração."""
        super().__init__()

        self.accessibility_manager = AccessibilityManager()

        self.setup_ui()
        self.setup_keyboard_shortcuts()
        self.setup_accessibility()

        logger.info("Janela de demonstração de acessibilidade inicializada")

    def setup_ui(self):
        """Configura a interface do usuário."""
        self.setWindowTitle("Demonstração de Acessibilidade")
        self.resize(800, 600)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout(central_widget)

        # Título
        title_label = QLabel("Demonstração de Recursos de Acessibilidade")
        title_font = title_label.font()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title_label)

        # Tabs
        self.tab_widget = QTabWidget()
        self.setup_demo_tab()
        self.setup_settings_tab()

        main_layout.addWidget(self.tab_widget)

    def setup_demo_tab(self):
        """Configura a aba de demonstração."""
        demo_tab = QWidget()
        demo_layout = QVBoxLayout(demo_tab)

        # Instruções
        instructions = QLabel(
            "Esta é uma demonstração dos recursos de acessibilidade do GoNetwork AI.\n"
            "Experimente alterar as configurações na aba 'Configurações' para ver as mudanças.\n"
            "Atalhos de teclado:\n"
            "  • Ctrl+1: Selecionar aba de Demonstração\n"
            "  • Ctrl+2: Selecionar aba de Configurações\n"
            "  • Ctrl+F: Aumentar tamanho da fonte\n"
            "  • Ctrl+Shift+F: Diminuir tamanho da fonte\n"
            "  • Ctrl+H: Alternar modo de alto contraste\n"
        )
        instructions.setWordWrap(True)
        demo_layout.addWidget(instructions)

        # Botões de exemplo
        primary_button = QPushButton("Botão Primário")
        secondary_button = QPushButton("Botão Secundário")
        tertiary_button = QPushButton("Botão Terciário")

        demo_layout.addWidget(primary_button)
        demo_layout.addWidget(secondary_button)
        demo_layout.addWidget(tertiary_button)

        # Adicionar a aba
        self.tab_widget.addTab(demo_tab, "Demonstração")

    def setup_settings_tab(self):
        """Configura a aba de configurações."""
        settings_tab = QWidget()
        settings_layout = QVBoxLayout(settings_tab)

        # Widget de configurações de acessibilidade
        accessibility_widget = AccessibilitySettingsWidget()
        settings_layout.addWidget(accessibility_widget)

        # Adicionar a aba
        self.tab_widget.addTab(settings_tab, "Configurações")

    def setup_keyboard_shortcuts(self):
        """Configura atalhos de teclado."""
        # Atalhos para navegação entre abas
        add_keyboard_shortcut(
            self,
            "Ctrl+1",
            lambda: self.tab_widget.setCurrentIndex(0),
            Qt.WindowShortcut,
        )
        add_keyboard_shortcut(
            self,
            "Ctrl+2",
            lambda: self.tab_widget.setCurrentIndex(1),
            Qt.WindowShortcut,
        )

        # Atalhos para ajustar tamanho da fonte
        add_keyboard_shortcut(
            self, "Ctrl+F", self.increase_font_size, Qt.WindowShortcut
        )
        add_keyboard_shortcut(
            self, "Ctrl+Shift+F", self.decrease_font_size, Qt.WindowShortcut
        )

        # Atalho para alternar modo de alto contraste
        add_keyboard_shortcut(
            self, "Ctrl+H", self.toggle_high_contrast, Qt.WindowShortcut
        )

    def setup_accessibility(self):
        """Configura recursos de acessibilidade."""
        # Configurar widgets para acessibilidade
        make_widget_accessible(
            self.tab_widget,
            "Abas de demonstração",
            "Contém abas para demonstrar recursos e configurar acessibilidade",
        )

        # Configurar a janela principal para acessibilidade
        self.setAccessibleName("Demonstração de Acessibilidade")
        self.setAccessibleDescription(
            "Janela para demonstrar os recursos de acessibilidade do GoNetwork AI"
        )

    def increase_font_size(self):
        """Aumenta o tamanho da fonte."""
        current_size = self.accessibility_manager.get_font_size()
        new_size_value = min(current_size.value + 1, FontSize.X_LARGE.value)
        new_size = FontSize(new_size_value)

        self.accessibility_manager.set_font_size(new_size)
        logger.info(f"Tamanho da fonte aumentado para {new_size.name}")

    def decrease_font_size(self):
        """Diminui o tamanho da fonte."""
        current_size = self.accessibility_manager.get_font_size()
        new_size_value = max(current_size.value - 1, FontSize.SMALL.value)
        new_size = FontSize(new_size_value)

        self.accessibility_manager.set_font_size(new_size)
        logger.info(f"Tamanho da fonte diminuído para {new_size.name}")

    def toggle_high_contrast(self):
        """Alterna entre modo normal e alto contraste."""
        current_scheme = self.accessibility_manager.get_color_scheme()

        if current_scheme == ColorScheme.HIGH_CONTRAST:
            self.accessibility_manager.set_color_scheme(ColorScheme.NORMAL)
            logger.info("Modo de alto contraste desativado")
        else:
            self.accessibility_manager.set_color_scheme(ColorScheme.HIGH_CONTRAST)
            logger.info("Modo de alto contraste ativado")


def main():
    """Função principal."""
    app = QApplication(sys.argv)

    # Configurar a aplicação para acessibilidade
    app.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # Criar e exibir a janela
    window = AccessibilityDemoWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
