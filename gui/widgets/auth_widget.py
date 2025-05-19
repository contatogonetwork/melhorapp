from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class AuthWidget(QWidget):
    login_successful = Signal()

    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Widget de conteúdo
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setAlignment(Qt.AlignCenter)

        # Painel de login
        self.auth_panel = QFrame()
        self.auth_panel.setFixedSize(400, 500)
        self.auth_panel.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 10px;
                border: 1px solid {style.current_line_color};
            }}
        """
        )

        # Layout do painel
        self.panel_layout = QVBoxLayout(self.auth_panel)
        self.panel_layout.setContentsMargins(25, 25, 25, 25)
        self.panel_layout.setSpacing(15)

        # Logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignCenter)
        self.logo_label.setText(
            "GoNetwork AI"
        )  # Placeholder até termos um logo real
        self.logo_label.setStyleSheet(
            f"""
            color: {style.purple_color};
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 10px;
        """
        )

        # Abas (login/cadastro)
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet(style.tab_style)

        # Aba de login
        self.login_tab = QWidget()
        self.login_layout = QVBoxLayout(self.login_tab)
        self.login_layout.setContentsMargins(10, 20, 10, 10)
        self.login_layout.setSpacing(15)

        # Formulário de login
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        # Campo de email
        self.email_label = QLabel("Email:")
        self.email_label.setStyleSheet(f"color: {style.foreground_color};")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Seu email")
        self.email_input.setStyleSheet(style.input_style)

        # Campo de senha
        self.password_label = QLabel("Senha:")
        self.password_label.setStyleSheet(f"color: {style.foreground_color};")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Sua senha")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(style.input_style)

        # Adicionar campos ao formulário
        self.form_layout.addRow(self.email_label, self.email_input)
        self.form_layout.addRow(self.password_label, self.password_input)

        # Opção "Lembrar-me"
        self.remember_me = QCheckBox("Lembrar-me")
        self.remember_me.setStyleSheet(style.toggle_style)

        # Link "Esqueceu a senha"
        self.forgot_password = QPushButton("Esqueceu a senha?")
        self.forgot_password.setCursor(Qt.CursorShape.PointingHandCursor)
        self.forgot_password.setStyleSheet(
            f"""
            QPushButton {{
                background-color: transparent;
                color: {style.cyan_color};
                text-align: right;
                border: none;
            }}
            QPushButton:hover {{
                color: {style.purple_color};
            }}
        """
        )

        # Layout para "Lembrar-me" e "Esqueceu a senha"
        self.options_layout = QHBoxLayout()
        self.options_layout.addWidget(self.remember_me)
        self.options_layout.addStretch()
        self.options_layout.addWidget(self.forgot_password)

        # Botão de login
        self.login_button = QPushButton("Entrar")
        self.login_button.setStyleSheet(style.button_style)
        self.login_button.setFixedHeight(40)

        # Adicionar elementos ao layout de login
        self.login_layout.addLayout(self.form_layout)
        self.login_layout.addLayout(self.options_layout)
        self.login_layout.addWidget(self.login_button)
        self.login_layout.addStretch()

        # Aba de cadastro (simplificada para exemplo)
        self.register_tab = QWidget()
        self.register_layout = QVBoxLayout(self.register_tab)
        self.register_layout.setContentsMargins(10, 20, 10, 10)

        self.register_label = QLabel("Função de cadastro em desenvolvimento")
        self.register_label.setStyleSheet(
            f"color: {style.foreground_color}; text-align: center;"
        )
        self.register_label.setAlignment(Qt.AlignCenter)

        self.register_layout.addWidget(self.register_label)
        self.register_layout.addStretch()

        # Adicionar abas ao widget de abas
        self.tab_widget.addTab(self.login_tab, "Login")
        self.tab_widget.addTab(self.register_tab, "Cadastro")

        # Adicionar elementos ao painel
        self.panel_layout.addWidget(self.logo_label)
        self.panel_layout.addWidget(self.tab_widget)

        # Adicionar painel ao layout de conteúdo
        self.content_layout.addWidget(self.auth_panel)

        # Adicionar conteúdo ao layout principal
        self.layout.addWidget(self.content)

        # Conectar sinais
        self.login_button.clicked.connect(self.on_login)

    def on_login(self):
        # Placeholder - em produção, verificaria as credenciais
        self.login_successful.emit()

    def paintEvent(self, event):
        # Criar o painter
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Desenhar o gradiente de fundo
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor("#021E33"))
        gradient.setColorAt(1, QColor("#000000"))

        painter.fillRect(self.rect(), gradient)

        # Desenhar partículas (decorativas)
        painter.setPen(QColor(255, 255, 255, 30))
        for i in range(50):
            x = (i * 30) % self.width()
            y = (i * 25) % self.height()
            size = (i % 5) + 1
            painter.drawEllipse(x, y, size, size)
