import sys
import os
import json
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QStackedWidget, QApplication
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Qt, QSize, QPoint, Signal, Slot

# Importar widgets
from gui.widgets.dashboard_widget import DashboardWidget
from gui.widgets.event_widget import EventWidget
from gui.widgets.team_widget import TeamWidget
from gui.widgets.briefing_widget import BriefingWidget
from gui.widgets.timeline_widget import TimelineWidget
from gui.widgets.editing_widget import EditingWidget
from gui.widgets.delivery_widget import DeliveryWidget
from gui.widgets.assets_widget import AssetsWidget
from gui.widgets.settings_widget import SettingsWidget
from gui.widgets.login_widget import LoginWidget

import gui.themes.dracula as style
from utils.helpers import load_config

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Adicionando a inicialização do _drag_pos aqui
        self._drag_pos = None
        
        # Configuração inicial
        self.config = load_config()
        self.logged_in = False
        self.current_user = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Configurar janela principal
        self.setWindowTitle("GoNetwork AI")
        self.setWindowIcon(QIcon("./resources/icons/logo.svg"))
        self.resize(1200, 800)
        
        # Remover barra de título padrão
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Widget central
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout principal
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # Container principal com borda arredondada
        self.container = QWidget()
        self.container.setObjectName("container")
        self.container.setStyleSheet(f"""
            #container {{
                background-color: {style.background_color};
                border-radius: 10px;
                border: 1px solid {style.comment_color};
            }}
        """)
        
        # Layout do container
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        
        # Adicionar container ao layout principal
        self.main_layout.addWidget(self.container)
        
        # Mostrar tela de login inicialmente
        self.setup_login_widget()
        
    def setup_app_widget(self):
        # Layout para o conteúdo do aplicativo
        self.app_widget = QWidget()
        self.app_layout = QHBoxLayout(self.app_widget)
        self.app_layout.setContentsMargins(0, 0, 0, 0)
        self.app_layout.setSpacing(0)
        
        # Barra lateral/menu
        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet(f"""
            #sidebar {{
                background-color: {style.background_color};
                border-right: 1px solid {style.current_line_color};
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
            }}
        """)
        self.sidebar.setFixedWidth(200)
        
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 20)
        self.sidebar_layout.setSpacing(5)
        
        # Logo
        self.logo_label = QLabel("GoNetwork AI")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet(f"""
            color: {style.purple_color};
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            padding: 10px;
        """)
        
        # Botões do menu
        self.menu_buttons = []
        
        # Dashboard
        dashboard_btn = QPushButton("  Dashboard")
        dashboard_btn.setIcon(QIcon("./resources/icons/dashboard.svg"))
        dashboard_btn.setIconSize(QSize(20, 20))
        dashboard_btn.setStyleSheet(style.menu_button_style)
        dashboard_btn.setFixedHeight(40)
        dashboard_btn.clicked.connect(lambda: self.show_page(0))
        self.menu_buttons.append(dashboard_btn)
        
        # Eventos
        events_btn = QPushButton("  Eventos")
        events_btn.setIcon(QIcon("./resources/icons/calendar.svg"))
        events_btn.setIconSize(QSize(20, 20))
        events_btn.setStyleSheet(style.menu_button_style)
        events_btn.setFixedHeight(40)
        events_btn.clicked.connect(lambda: self.show_page(1))
        self.menu_buttons.append(events_btn)
        
        # Equipe
        team_btn = QPushButton("  Equipe")
        team_btn.setIcon(QIcon("./resources/icons/team.svg"))
        team_btn.setIconSize(QSize(20, 20))
        team_btn.setStyleSheet(style.menu_button_style)
        team_btn.setFixedHeight(40)
        team_btn.clicked.connect(lambda: self.show_page(2))
        self.menu_buttons.append(team_btn)
        
        # Briefing
        briefing_btn = QPushButton("  Briefing")
        briefing_btn.setIcon(QIcon("./resources/icons/document.svg"))
        briefing_btn.setIconSize(QSize(20, 20))
        briefing_btn.setStyleSheet(style.menu_button_style)
        briefing_btn.setFixedHeight(40)
        briefing_btn.clicked.connect(lambda: self.show_page(3))
        self.menu_buttons.append(briefing_btn)
        
        # Timeline
        timeline_btn = QPushButton("  Timeline")
        timeline_btn.setIcon(QIcon("./resources/icons/timeline.svg"))
        timeline_btn.setIconSize(QSize(20, 20))
        timeline_btn.setStyleSheet(style.menu_button_style)
        timeline_btn.setFixedHeight(40)
        timeline_btn.clicked.connect(lambda: self.show_page(4))
        self.menu_buttons.append(timeline_btn)
        
        # Edição e Aprovação
        editing_btn = QPushButton("  Edição/Aprovação")
        editing_btn.setIcon(QIcon("./resources/icons/video.svg"))
        editing_btn.setIconSize(QSize(20, 20))
        editing_btn.setStyleSheet(style.menu_button_style)
        editing_btn.setFixedHeight(40)
        editing_btn.clicked.connect(lambda: self.show_page(5))
        self.menu_buttons.append(editing_btn)
        
        # Entregas
        delivery_btn = QPushButton("  Entregas")
        delivery_btn.setIcon(QIcon("./resources/icons/delivery.svg"))
        delivery_btn.setIconSize(QSize(20, 20))
        delivery_btn.setStyleSheet(style.menu_button_style)
        delivery_btn.setFixedHeight(40)
        delivery_btn.clicked.connect(lambda: self.show_page(6))
        self.menu_buttons.append(delivery_btn)
        
        # Assets
        assets_btn = QPushButton("  Assets")
        assets_btn.setIcon(QIcon("./resources/icons/folder.svg"))
        assets_btn.setIconSize(QSize(20, 20))
        assets_btn.setStyleSheet(style.menu_button_style)
        assets_btn.setFixedHeight(40)
        assets_btn.clicked.connect(lambda: self.show_page(7))
        self.menu_buttons.append(assets_btn)
        
        # Configurações
        settings_btn = QPushButton("  Configurações")
        settings_btn.setIcon(QIcon("./resources/icons/settings.svg"))
        settings_btn.setIconSize(QSize(20, 20))
        settings_btn.setStyleSheet(style.menu_button_style)
        settings_btn.setFixedHeight(40)
        settings_btn.clicked.connect(lambda: self.show_page(8))
        self.menu_buttons.append(settings_btn)
        
        # Adicionar logo e botões ao sidebar
        self.sidebar_layout.addWidget(self.logo_label)
        for btn in self.menu_buttons:
            self.sidebar_layout.addWidget(btn)
        
        # Espaço flexível
        self.sidebar_layout.addStretch()
        
        # Botão de logout
        logout_btn = QPushButton("  Sair")
        logout_btn.setIcon(QIcon("./resources/icons/logout.svg"))
        logout_btn.setIconSize(QSize(20, 20))
        logout_btn.setStyleSheet(style.menu_button_style)
        logout_btn.setFixedHeight(40)
        
        # Conectar diretamente ao logout, sem tentar desconectar antes
        logout_btn.clicked.connect(self.logout)
        self.sidebar_layout.addWidget(logout_btn)
        
        # Conteúdo principal com barra superior
        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Barra superior
        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(50)
        self.top_bar.setStyleSheet(f"""
            background-color: {style.background_color};
            border-bottom: 1px solid {style.current_line_color};
            border-top-right-radius: 10px;
        """)
        
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(10, 0, 10, 0)
        
        # Usuário logado
        self.user_label = QLabel(f"Olá, {self.current_user['full_name']}")
        self.user_label.setStyleSheet(f"color: {style.foreground_color};")
        
        # Botões de controle da janela
        self.window_controls = QWidget()
        self.controls_layout = QHBoxLayout(self.window_controls)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_layout.setSpacing(8)
        
        # Botão minimizar
        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(QIcon("./resources/icons/minimize.svg"))
        self.minimize_btn.setFixedSize(24, 24)
        self.minimize_btn.setStyleSheet(style.window_button_style)
        self.minimize_btn.clicked.connect(self.showMinimized)
        
        # Botão maximizar/restaurar
        self.maximize_btn = QPushButton()
        self.maximize_btn.setIcon(QIcon("./resources/icons/maximize.svg"))
        self.maximize_btn.setFixedSize(24, 24)
        self.maximize_btn.setStyleSheet(style.window_button_style)
        self.maximize_btn.clicked.connect(self.toggle_maximize)
        
        # Botão fechar
        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon("./resources/icons/close.svg"))
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setStyleSheet(style.close_button_style)
        self.close_btn.clicked.connect(self.close)
        
        # Adicionar botões ao layout dos controles
        self.controls_layout.addWidget(self.minimize_btn)
        self.controls_layout.addWidget(self.maximize_btn)
        self.controls_layout.addWidget(self.close_btn)
        
        # Adicionar widgets à barra superior
        self.top_bar_layout.addWidget(self.user_label)
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.window_controls)
        
        # Área de conteúdo (Stacked Widget para múltiplas páginas)
        self.pages = QStackedWidget()
        
        # Inicializar páginas
        self.dashboard_page = DashboardWidget()
        self.event_page = EventWidget()
        self.team_page = TeamWidget()
        self.briefing_page = BriefingWidget()
        self.timeline_page = TimelineWidget()
        self.editing_page = EditingWidget()
        self.delivery_page = DeliveryWidget()
        self.assets_page = AssetsWidget()
        self.settings_page = SettingsWidget()
        
        # Adicionar páginas ao stack
        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.event_page)
        self.pages.addWidget(self.team_page)
        self.pages.addWidget(self.briefing_page)
        self.pages.addWidget(self.timeline_page)
        self.pages.addWidget(self.editing_page)
        self.pages.addWidget(self.delivery_page)
        self.pages.addWidget(self.assets_page)
        self.pages.addWidget(self.settings_page)
        
        # Adicionar widgets ao container de conteúdo
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.pages)
        
        # Adicionar sidebar e conteúdo ao layout principal do app
        self.app_layout.addWidget(self.sidebar)
        self.app_layout.addWidget(self.content_container)
        
        # Substituir o widget atual pelo app completo
        if hasattr(self, 'login_widget'):
            self.container_layout.removeWidget(self.login_widget)
            self.login_widget.deleteLater()
        
        self.container_layout.addWidget(self.app_widget)
        
        # Selecionar a página inicial (dashboard)
        self.show_page(0)
        
    def setup_login_widget(self):
        # Criar e configurar o widget de login
        self.login_widget = LoginWidget()
        self.login_widget.login_success.connect(self.handle_login)
        
        # Adicionar widget de login ao container
        self.container_layout.addWidget(self.login_widget)
    
    def handle_login(self, user):
        # Armazenar informações do usuário
        self.logged_in = True
        self.current_user = user
        
        # Carregar interface principal do app
        self.setup_app_widget()
    
    def logout(self):
        # Remover o widget do app
        if hasattr(self, 'app_widget'):
            self.container_layout.removeWidget(self.app_widget)
            self.app_widget.deleteLater()
        
        # Resetar estado
        self.logged_in = False
        self.current_user = None
        
        # Mostrar login novamente
        self.setup_login_widget()
    
    def show_page(self, index):
        # Destacar botão selecionado
        for i, btn in enumerate(self.menu_buttons):
            if i == index:
                btn.setStyleSheet(style.menu_button_active_style)
            else:
                btn.setStyleSheet(style.menu_button_style)
        
        # Mostrar página correspondente
        self.pages.setCurrentIndex(index)
    
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_btn.setIcon(QIcon("./resources/icons/maximize.svg"))
        else:
            self.showMaximized()
            self.maximize_btn.setIcon(QIcon("./resources/icons/restore.svg"))
    
    def mousePressEvent(self, event):
        # Verificar se o clique foi na barra superior
        if event.position().y() < 50:
            self._drag_pos = event.position().toPoint()
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        # Verificar se está em modo de arrastar
        if self._drag_pos is not None:
            # Calcular a diferença entre a posição atual e a posição inicial
            diff = event.position().toPoint() - self._drag_pos
            # Mover a janela pela diferença calculada
            self.move(self.pos() + diff)
        
        super().mouseMoveEvent(event)