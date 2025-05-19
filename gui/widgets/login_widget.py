from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QFrame, QCheckBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QPixmap, QFont

import gui.themes.dracula as style
from database.models import User

class LoginWidget(QWidget):
    # Sinal emitido quando o login é bem-sucedido
    login_success = Signal(dict)
    
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        
        # Container de login
        self.login_container = QFrame()
        self.login_container.setObjectName("login_container")
        self.login_container.setStyleSheet(f"""
            #login_container {{
                background-color: {style.background_color};
                border-radius: 10px;
            }}
        """)
        
        self.login_layout = QVBoxLayout(self.login_container)
        self.login_layout.setContentsMargins(0, 0, 0, 0)
        self.login_layout.setSpacing(0)
        
        # Barra superior para controles de janela
        self.top_bar = QFrame()
        self.top_bar.setFixedHeight(40)
        self.top_bar.setStyleSheet(f"""
            background-color: {style.background_color};
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
        """)
        
        self.top_bar_layout = QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(15, 0, 15, 0)
        self.top_bar_layout.setSpacing(8)
        
        # Logo ou nome na barra superior
        self.logo_label = QLabel("GoNetwork AI")
        self.logo_label.setStyleSheet(f"color: {style.purple_color}; font-size: 16px; font-weight: bold;")
        
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
        self.minimize_btn.clicked.connect(self.window().showMinimized)
        
        # Botão fechar
        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon("./resources/icons/close.svg"))
        self.close_btn.setFixedSize(24, 24)
        self.close_btn.setStyleSheet(style.close_button_style)
        self.close_btn.clicked.connect(self.window().close)
        
        # Adicionar botões ao layout dos controles
        self.controls_layout.addWidget(self.minimize_btn)
        self.controls_layout.addWidget(self.close_btn)
        
        # Adicionar widgets à barra superior
        self.top_bar_layout.addWidget(self.logo_label)
        self.top_bar_layout.addStretch()
        self.top_bar_layout.addWidget(self.window_controls)
        
        # Conteúdo do login
        self.content_frame = QFrame()
        self.content_frame.setStyleSheet(f"""
            background-color: {style.background_color};
            border-bottom-left-radius: 10px;
            border-bottom-right-radius: 10px;
        """)
        
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(40, 20, 40, 40)
        self.content_layout.setSpacing(20)
        self.content_layout.setAlignment(Qt.AlignCenter)
        
        # Logo ou imagem
        try:
            self.logo = QLabel()
            logo_pixmap = QPixmap("./resources/icons/logo.svg")
            if not logo_pixmap.isNull():
                self.logo.setPixmap(logo_pixmap.scaledToWidth(120, Qt.SmoothTransformation))
                self.logo.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(self.logo)
        except Exception:
            # Caso não encontre o logo, usar texto
            self.logo_text = QLabel("GoNetwork AI")
            self.logo_text.setAlignment(Qt.AlignCenter)
            self.logo_text.setStyleSheet(f"""
                color: {style.purple_color};
                font-size: 32px;
                font-weight: bold;
                margin-bottom: 20px;
            """)
            self.content_layout.addWidget(self.logo_text)
        
        # Título
        self.title = QLabel("Login")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(f"""
            color: {style.foreground_color};
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
        """)
        self.content_layout.addWidget(self.title)
        
        # Subtítulo
        self.subtitle = QLabel("Entre na sua conta para continuar")
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet(f"color: {style.comment_color}; font-size: 14px;")
        self.content_layout.addWidget(self.subtitle)
        
        # Formulário de login
        self.form_frame = QFrame()
        self.form_frame.setMaximumWidth(400)
        self.form_layout = QVBoxLayout(self.form_frame)
        self.form_layout.setContentsMargins(0, 20, 0, 0)
        self.form_layout.setSpacing(15)
        
        # Campo de usuário
        self.username_label = QLabel("Usuário")
        self.username_label.setStyleSheet(f"color: {style.foreground_color}; font-size: 14px;")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Digite seu nome de usuário")
        self.username_input.setStyleSheet(style.input_style)
        self.username_input.setMinimumHeight(36)
        
        # Campo de senha
        self.password_label = QLabel("Senha")
        self.password_label.setStyleSheet(f"color: {style.foreground_color}; font-size: 14px;")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(style.input_style)
        self.password_input.setMinimumHeight(36)
        
        # Remember me
        self.remember_layout = QHBoxLayout()
        self.remember_check = QCheckBox("Lembrar-me")
        self.remember_check.setStyleSheet(f"""
            QCheckBox {{
                color: {style.foreground_color};
                font-size: 14px;
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {style.comment_color};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {style.purple_color};
                border: 1px solid {style.purple_color};
            }}
        """)
        
        self.forgot_link = QPushButton("Esqueceu a senha?")
        self.forgot_link.setStyleSheet(f"""
            QPushButton {{
                color: {style.purple_color};
                background: transparent;
                border: none;
                text-decoration: none;
                text-align: right;
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: {style.pink_color};
                text-decoration: underline;
            }}
        """)
        
        self.remember_layout.addWidget(self.remember_check)
        self.remember_layout.addStretch()
        self.remember_layout.addWidget(self.forgot_link)
        
        # Botão de login
        self.login_btn = QPushButton("Entrar")
        self.login_btn.setStyleSheet(style.button_style)
        self.login_btn.setMinimumHeight(40)
        self.login_btn.clicked.connect(self.authenticate)
        
        # Adicionar campos ao formulário
        self.form_layout.addWidget(self.username_label)
        self.form_layout.addWidget(self.username_input)
        self.form_layout.addWidget(self.password_label)
        self.form_layout.addWidget(self.password_input)
        self.form_layout.addLayout(self.remember_layout)
        self.form_layout.addWidget(self.login_btn)
        
        # Registre-se
        self.register_layout = QHBoxLayout()
        self.register_label = QLabel("Não tem uma conta?")
        self.register_label.setStyleSheet(f"color: {style.comment_color}; font-size: 14px;")
        
        self.register_link = QPushButton("Registrar-se")
        self.register_link.setStyleSheet(f"""
            QPushButton {{
                color: {style.purple_color};
                background: transparent;
                border: none;
                text-decoration: none;
                font-size: 14px;
            }}
            QPushButton:hover {{
                color: {style.pink_color};
                text-decoration: underline;
            }}
        """)
        
        self.register_layout.addStretch()
        self.register_layout.addWidget(self.register_label)
        self.register_layout.addWidget(self.register_link)
        self.register_layout.addStretch()
        
        self.form_layout.addSpacing(10)
        self.form_layout.addLayout(self.register_layout)
        self.form_layout.addStretch()
        
        # Adicionar formulário ao conteúdo
        self.content_layout.addWidget(self.form_frame, 1, Qt.AlignCenter)
        
        # Adicionar versão na parte inferior
        self.version_label = QLabel("Versão 1.0.0")
        self.version_label.setAlignment(Qt.AlignCenter)
        self.version_label.setStyleSheet(f"color: {style.comment_color}; font-size: 12px;")
        self.content_layout.addWidget(self.version_label)
        
        # Adicionar à layout de login
        self.login_layout.addWidget(self.top_bar)
        self.login_layout.addWidget(self.content_frame, 1)
        
        # Adicionar container de login ao layout principal
        self.layout.addWidget(self.login_container, 1)
        
        # Focar no campo de usuário
        self.username_input.setFocus()
        
        # Permitir entrar pressionando Enter nos campos
        self.username_input.returnPressed.connect(self.password_input.setFocus)
        self.password_input.returnPressed.connect(self.authenticate)

        # Credenciais temporárias para desenvolvimento
        self.username_input.setText("admin")
        self.password_input.setText("admin123")
    
    def authenticate(self):
        """Autenticar o usuário e emitir sinal de login bem-sucedido"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_message("Erro", "Por favor, preencha todos os campos.")
            return
        
        # Credenciais fixas para desenvolvimento (prioridade mais alta)
        if username == "admin" and password == "admin123":
            # Dados fictícios para demonstração
            user_data = {
                'id': 1,
                'username': 'admin',
                'email': 'admin@gonetwork.ai',
                'full_name': 'Administrador',
                'role': 'admin',
                'profile_picture': None
            }
            self.login_success.emit(user_data)
            return
        
        # Se não for a credencial de desenvolvimento, tentar com o banco de dados
        try:
            user_model = User()
            success = user_model.authenticate(username, password)
            
            if success:
                # Obter dados do usuário autenticado
                user_data = {
                    'id': user_model.id,
                    'username': user_model.username,
                    'email': user_model.email,
                    'full_name': user_model.full_name,
                    'role': user_model.role,
                    'profile_picture': user_model.profile_picture
                }
                
                # Emitir sinal com os dados do usuário
                self.login_success.emit(user_data)
            else:
                self.show_message("Erro de Autenticação", "Usuário ou senha incorretos.")
        
        except Exception as e:
            self.show_message("Erro de Autenticação", f"Erro ao autenticar: {str(e)}")
    
    def show_message(self, title, message):
        """Exibe uma mensagem de erro"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Warning if "Erro" in title else QMessageBox.Information)
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {style.background_color};
                color: {style.foreground_color};
            }}
            QLabel {{
                color: {style.foreground_color};
            }}
            QPushButton {{
                background-color: {style.purple_color};
                color: {style.background_color};
                border-radius: 5px;
                padding: 5px 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {style.pink_color};
            }}
        """)
        msg_box.exec()