import json
import os
import sys

from PySide6.QtCore import QPoint, QSize, Qt, Signal, Slot
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style
from gui.widgets.assets_widget import AssetsWidget
from gui.widgets.briefing_widget import BriefingWidget
from gui.widgets.dashboard_widget import DashboardWidget
from gui.widgets.delivery_widget import DeliveryWidget
from gui.widgets.editing_widget import EditingWidget
from gui.widgets.event_widget import EventWidget
from gui.widgets.login_widget import LoginWidget
from gui.widgets.settings_widget import SettingsWidget
from gui.widgets.team_widget import TeamWidget
from gui.widgets.timeline_widget import TimelineWidget
from utils.helpers import load_config


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._drag_pos = None
        self.config = load_config()
        self.logged_in = False
        self.current_user = None

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("GoNetwork AI")
        self.setWindowIcon(QIcon("./resources/icons/logo.svg"))
        self.resize(1200, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.container = QWidget()
        self.container.setObjectName("container")
        self.container.setStyleSheet(
            f"""
            #container {{
                background-color: {style.background_color};
                border-radius: 10px;
                border: 1px solid {style.comment_color};
            }}
        """
        )

        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)

        self.main_layout.addWidget(self.container)

        self.setup_login_widget()

    def setup_app_widget(self):
        self.app_widget = QWidget()
        self.app_layout = QHBoxLayout(self.app_widget)
        self.app_layout.setContentsMargins(0, 0, 0, 0)
        self.app_layout.setSpacing(0)

        self.sidebar = QWidget()
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet(
            f"""
            #sidebar {{
                background-color: {style.background_color};
                border-right: 1px solid {style.current_line_color};
                border-top-left-radius: 10px;
                border-bottom-left-radius: 10px;
            }}
        """
        )
        self.sidebar.setFixedWidth(200)

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(10, 10, 10, 20)
        self.sidebar_layout.setSpacing(5)

        self.logo_label = QLabel("GoNetwork AI")
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setStyleSheet(
            f"""
            color: {style.purple_color};
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 20px;
            padding: 10px;
        """
        )

        self.menu_buttons = []

        def add_button(text, icon, index):
            btn = QPushButton(f"  {text}")
            btn.setIcon(QIcon(icon))
            btn.setIconSize(QSize(20, 20))
            btn.setStyleSheet(style.menu_button_style)
            btn.setFixedHeight(40)
            btn.clicked.connect(lambda: self.show_page(index))
            self.menu_buttons.append(btn)
            self.sidebar_layout.addWidget(btn)

        add_button("Dashboard", "./resources/icons/dashboard.svg", 0)
        add_button("Eventos", "./resources/icons/calendar.svg", 1)
        add_button("Equipe", "./resources/icons/team.svg", 2)
        add_button("Briefing", "./resources/icons/document.svg", 3)
        add_button("Timeline", "./resources/icons/timeline.svg", 4)
        add_button("Edição/Aprovação", "./resources/icons/video.svg", 5)
        add_button("Entregas", "./resources/icons/delivery.svg", 6)
        add_button("Assets", "./resources/icons/folder.svg", 7)
        add_button("Configurações", "./resources/icons/settings.svg", 8)

        self.sidebar_layout.addWidget(self.logo_label)
        self.sidebar_layout.addStretch()

        logout_btn = QPushButton("  Sair")
        logout_btn.setIcon(QIcon("./resources/icons/logout.svg"))
        logout_btn.setIconSize(QSize(20, 20))
        logout_btn.setStyleSheet(style.menu_button_style)
        logout_btn.setFixedHeight(40)
        logout_btn.clicked.connect(self.logout)
        self.sidebar_layout.addWidget(logout_btn)

        self.content_container = QWidget()
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)

        self.top_bar = QWidget()
        self.top_bar.setFixedHeight(50)
        self.top_bar.setStyleSheet(
            f"""
            background-color: {style.background_color};
            border-bottom: 1px solid {style.current_line_color};
            border-top-right-radius: 10px;
        """
        )

        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(10, 0, 10, 0)

        self.user_label = QLabel(f"Olá, {self.current_user['full_name']}")
        self.user_label.setStyleSheet(f"color: {style.foreground_color};")

        self.window_controls = QWidget()
        self.controls_layout = QHBoxLayout(self.window_controls)
        self.controls_layout.setContentsMargins(0, 0, 0, 0)
        self.controls_layout.setSpacing(8)

        self.minimize_btn = QPushButton()
        self.minimize_btn.setIcon(QIcon("./resources/icons/minimize.svg"))
        self.minimize_btn.setFixedSize(24, 24)
        self.minimize_btn.setStyleSheet(style.window_button_style)
        self.minimize_btn.clicked.connect(self.showMinimized)

        self.maximize_btn = QPushButton()
        self.maximize_btn.setIcon(QIcon("./resources/icons/maximize.svg"))
        self.maximize_btn.setFixedSize(24, 24)
        self.maximize_btn.setStyleSheet(style.window_button_style)
        self.maximize_btn.clicked.connect(self.toggle_maximize)

        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon("./resources/icons/close.svg"))
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setStyleSheet(style.close_button_style)
        self.close_btn.clicked.connect(self.close)

        self.controls_layout.addWidget(self.minimize_btn)
        self.controls_layout.addWidget(self.maximize_btn)
        self.controls_layout.addWidget(self.close_btn)

        self.top_bar_layout.addWidget(self.user_label)
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.window_controls)

        self.pages = QStackedWidget()

        self.dashboard_page = DashboardWidget()
        self.event_page = EventWidget()
        self.team_page = TeamWidget()
        self.briefing_page = BriefingWidget()
        self.timeline_page = TimelineWidget()
        self.editing_page = EditingWidget()
        self.delivery_page = DeliveryWidget()
        self.assets_page = AssetsWidget()
        self.settings_page = SettingsWidget()

        self.pages.addWidget(self.dashboard_page)
        self.pages.addWidget(self.event_page)
        self.pages.addWidget(self.team_page)
        self.pages.addWidget(self.briefing_page)
        self.pages.addWidget(self.timeline_page)
        self.pages.addWidget(self.editing_page)
        self.pages.addWidget(self.delivery_page)
        self.pages.addWidget(self.assets_page)
        self.pages.addWidget(self.settings_page)

        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.pages)

        self.app_layout.addWidget(self.sidebar)
        self.app_layout.addWidget(self.content_container)

        if hasattr(self, "login_widget"):
            self.container_layout.removeWidget(self.login_widget)
            self.login_widget.deleteLater()

        self.container_layout.addWidget(self.app_widget)

        self.show_page(0)

    def setup_login_widget(self):
        self.login_widget = LoginWidget()
        self.login_widget.login_success.connect(self.handle_login)
        self.container_layout.addWidget(self.login_widget)

    def handle_login(self, user):
        self.logged_in = True
        self.current_user = user

        self.setup_app_widget()

        # Após o setup do app, agora a edição está instanciada corretamente
        from database.EventRepository import EventRepository
        from database.TeamRepository import TeamRepository

        if hasattr(self, "editing_page"):
            self.editing_page.set_current_user(user)
            self.editing_page.load_initial_data(EventRepository(), TeamRepository())
            self.editing_page.setup_video_sync()

    def logout(self):
        if hasattr(self, "app_widget"):
            self.container_layout.removeWidget(self.app_widget)
            self.app_widget.deleteLater()

        self.logged_in = False
        self.current_user = None

        self.setup_login_widget()

    def show_page(self, index):
        for i, btn in enumerate(self.menu_buttons):
            if i == index:
                btn.setStyleSheet(style.menu_button_active_style)
            else:
                btn.setStyleSheet(style.menu_button_style)
        self.pages.setCurrentIndex(index)

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
            self.maximize_btn.setIcon(QIcon("./resources/icons/maximize.svg"))
        else:
            self.showMaximized()
            self.maximize_btn.setIcon(QIcon("./resources/icons/restore.svg"))

    def mousePressEvent(self, event):
        if event.position().y() < 50:
            self._drag_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        super().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self._drag_pos is not None:
            diff = event.position().toPoint() - self._drag_pos
            self.move(self.pos() + diff)
        super().mouseMoveEvent(event)
