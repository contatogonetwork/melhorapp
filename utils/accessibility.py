#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários para melhorar a acessibilidade da aplicação.

Este módulo fornece classes e funções para melhorar a acessibilidade
da interface gráfica, garantindo que o aplicativo seja utilizável
por pessoas com necessidades especiais.
"""

from enum import Enum
from typing import Dict, Optional, Union

from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QAction, QFont, QKeySequence
from PySide6.QtWidgets import QApplication, QWidget

from utils.logger import get_logger

# Configurar logger
logger = get_logger("accessibility")


class FontSize(Enum):
    """Tamanhos de fonte para acessibilidade."""

    SMALL = 0
    NORMAL = 1
    LARGE = 2
    X_LARGE = 3


class ColorScheme(Enum):
    """Esquemas de cores para acessibilidade."""

    NORMAL = "normal"
    HIGH_CONTRAST = "high_contrast"
    DARK = "dark"
    LIGHT = "light"


class AccessibilityManager(QObject):
    """
    Gerencia configurações de acessibilidade para toda a aplicação.

    Esta classe fornece funcionalidades para ajustar tamanho de fonte,
    esquema de cores, atalhos de teclado e outras configurações de
    acessibilidade para toda a aplicação.
    """

    # Sinais emitidos quando as configurações mudam
    font_size_changed = Signal(FontSize)
    color_scheme_changed = Signal(ColorScheme)
    screen_reader_mode_changed = Signal(bool)

    # Instância singleton
    _instance = None

    def __new__(cls):
        """Implementa o padrão Singleton."""
        if cls._instance is None:
            cls._instance = super(AccessibilityManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Inicializa o gerenciador de acessibilidade."""
        if self._initialized:
            return

        super().__init__()
        self._initialized = True

        # Configurações padrão
        self._font_size = FontSize.NORMAL
        self._color_scheme = ColorScheme.NORMAL
        self._screen_reader_mode = False
        self._keyboard_shortcuts_enabled = True

        # Fatores de escala para tamanhos de fonte
        self._font_scale_factors = {
            FontSize.SMALL: 0.85,
            FontSize.NORMAL: 1.0,
            FontSize.LARGE: 1.25,
            FontSize.X_LARGE: 1.5,
        }

        # Dicionário de fontes em cache
        self._font_cache: Dict[str, QFont] = {}

        # Registrar para eventos de aplicação
        app = QApplication.instance()
        if app:
            app.installEventFilter(self)

        logger.info("Gerenciador de acessibilidade inicializado")

    def set_font_size(self, size: FontSize) -> None:
        """
        Define o tamanho da fonte para toda a aplicação.

        Args:
            size: Tamanho da fonte a ser definido
        """
        if self._font_size == size:
            return

        self._font_size = size
        self._update_application_fonts()
        self.font_size_changed.emit(size)
        logger.info(f"Tamanho de fonte alterado para {size.name}")

    def get_font_size(self) -> FontSize:
        """
        Obtém o tamanho de fonte atual.

        Returns:
            FontSize: Tamanho de fonte atual
        """
        return self._font_size

    def set_color_scheme(self, scheme: ColorScheme) -> None:
        """
        Define o esquema de cores para toda a aplicação.

        Args:
            scheme: Esquema de cores a ser definido
        """
        if self._color_scheme == scheme:
            return

        self._color_scheme = scheme
        self._update_application_style()
        self.color_scheme_changed.emit(scheme)
        logger.info(f"Esquema de cores alterado para {scheme.value}")

    def get_color_scheme(self) -> ColorScheme:
        """
        Obtém o esquema de cores atual.

        Returns:
            ColorScheme: Esquema de cores atual
        """
        return self._color_scheme

    def set_screen_reader_mode(self, enabled: bool) -> None:
        """
        Ativa ou desativa o modo para leitores de tela.

        Args:
            enabled: True para ativar, False para desativar
        """
        if self._screen_reader_mode == enabled:
            return

        self._screen_reader_mode = enabled
        self._update_accessibility_properties()
        self.screen_reader_mode_changed.emit(enabled)
        logger.info(
            f"Modo para leitores de tela {'ativado' if enabled else 'desativado'}"
        )

    def is_screen_reader_mode_enabled(self) -> bool:
        """
        Verifica se o modo para leitores de tela está ativado.

        Returns:
            bool: True se ativado, False caso contrário
        """
        return self._screen_reader_mode

    def get_scaled_font(self, base_font: Optional[QFont] = None) -> QFont:
        """
        Obtém uma fonte escalada de acordo com as configurações de acessibilidade.

        Args:
            base_font: Fonte base a ser escalada. Se None, usa a fonte padrão da aplicação.

        Returns:
            QFont: Fonte escalada de acordo com as configurações
        """
        if base_font is None:
            base_font = QApplication.font()

        # Calcular tamanho da fonte escalado
        scale_factor = self._font_scale_factors[self._font_size]
        point_size = base_font.pointSizeF() * scale_factor

        # Verificar se a fonte já está em cache
        cache_key = f"{base_font.family()}_{point_size}_{base_font.weight()}_{base_font.italic()}"

        if cache_key in self._font_cache:
            return self._font_cache[cache_key]

        # Criar nova fonte escalada
        scaled_font = QFont(base_font)
        scaled_font.setPointSizeF(point_size)

        # Adicionar ao cache
        self._font_cache[cache_key] = scaled_font

        return scaled_font

    def _update_application_fonts(self) -> None:
        """Atualiza as fontes em toda a aplicação."""
        app = QApplication.instance()
        if not app:
            return

        # Obter fonte atual
        current_font = app.font()

        # Aplicar fator de escala
        scale_factor = self._font_scale_factors[self._font_size]
        new_size = (
            current_font.pointSizeF()
            * scale_factor
            / self._font_scale_factors[FontSize.NORMAL]
        )

        # Criar nova fonte
        new_font = QFont(current_font)
        new_font.setPointSizeF(new_size)

        # Aplicar a nova fonte à aplicação
        app.setFont(new_font)

        # Limpar cache de fontes
        self._font_cache.clear()

        # Forçar atualização de todos os widgets
        for widget in app.allWidgets():
            widget.update()

    def _update_application_style(self) -> None:
        """Atualiza o estilo da aplicação com base no esquema de cores."""
        app = QApplication.instance()
        if not app:
            return

        # Configurações específicas por esquema de cores
        if self._color_scheme == ColorScheme.HIGH_CONTRAST:
            app.setStyleSheet(
                """
                QWidget {
                    background-color: black;
                    color: white;
                    border: 1px solid white;
                }
                QLabel {
                    border: none;
                }
                QPushButton {
                    background-color: black;
                    color: white;
                    border: 2px solid white;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #333;
                }
                QPushButton:pressed {
                    background-color: #555;
                }
                QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
                    background-color: black;
                    color: white;
                    border: 2px solid white;
                    padding: 3px;
                }
                QTableView, QListView, QTreeView {
                    background-color: black;
                    color: white;
                    border: 1px solid white;
                    alternate-background-color: #222;
                }
                QHeaderView::section {
                    background-color: black;
                    color: white;
                    border: 1px solid white;
                    padding: 4px;
                }
            """
            )
        elif self._color_scheme == ColorScheme.DARK:
            app.setStyleSheet(
                """
                QWidget {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                }
                QPushButton {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555;
                    border-radius: 3px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #4d4d4d;
                }
                QPushButton:pressed {
                    background-color: #5d5d5d;
                }
                QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {
                    background-color: #3d3d3d;
                    color: #e0e0e0;
                    border: 1px solid #555;
                    border-radius: 3px;
                    padding: 3px;
                }
                QTableView, QListView, QTreeView {
                    background-color: #2d2d2d;
                    color: #e0e0e0;
                    alternate-background-color: #3a3a3a;
                }
            """
            )
        else:
            # Restaurar estilo normal
            app.setStyleSheet("")

    def _update_accessibility_properties(self) -> None:
        """Atualiza propriedades de acessibilidade nos widgets."""
        app = QApplication.instance()
        if not app:
            return

        # Configurar propriedades para leitores de tela
        for widget in app.allWidgets():
            if self._screen_reader_mode:
                # Melhorar suporte para leitores de tela
                widget.setProperty("screenReaderMode", True)

                # Garantir que todos os widgets focáveis tenham acessibilidade adequada
                widget.setFocusPolicy(Qt.StrongFocus)
            else:
                widget.setProperty("screenReaderMode", False)

            # Forçar atualização de estilo
            widget.style().unpolish(widget)
            widget.style().polish(widget)
            widget.update()

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        """
        Filtro de eventos da aplicação para tratamento de acessibilidade.

        Args:
            obj: Objeto que gerou o evento
            event: Evento gerado

        Returns:
            bool: True se o evento foi tratado, False caso contrário
        """
        # Manipular eventos específicos de acessibilidade
        return super().eventFilter(obj, event)


def make_widget_accessible(widget: QWidget, label: str, description: str = "") -> None:
    """
    Configura um widget para ser mais acessível para pessoas com deficiência.

    Args:
        widget: Widget a ser configurado
        label: Texto curto para identificar o widget
        description: Descrição detalhada do propósito do widget
    """
    # Configurar nome de acessibilidade
    widget.setAccessibleName(label)

    # Configurar descrição de acessibilidade
    if description:
        widget.setAccessibleDescription(description)

    # Garantir que o widget seja focável pelo teclado
    widget.setFocusPolicy(Qt.StrongFocus)

    logger.debug(
        f"Widget {widget.__class__.__name__} configurado para acessibilidade: {label}"
    )


def add_keyboard_shortcut(
    widget: QWidget,
    key_sequence: Union[QKeySequence, str],
    callback,
    context=Qt.WidgetShortcut,
) -> QAction:
    """
    Adiciona um atalho de teclado a um widget.

    Args:
        widget: Widget que receberá o atalho
        key_sequence: Sequência de teclas para o atalho
        callback: Função a ser chamada quando o atalho for ativado
        context: Contexto do atalho

    Returns:
        QAction: Ação criada para o atalho
    """
    action = QAction(widget)
    action.setShortcut(key_sequence)
    action.setShortcutContext(context)
    action.triggered.connect(callback)
    widget.addAction(action)

    logger.debug(
        f"Atalho de teclado {key_sequence} adicionado a {widget.__class__.__name__}"
    )

    return action
