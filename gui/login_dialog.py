# login_dialog.py
# Implementação do diálogo de login

from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")

        # Layout principal
        layout = QVBoxLayout()

        # Campo de usuário
        self.username_label = QLabel("Usuário:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Campo de senha
        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Botão de login
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        # Simulação de validação de login
        if username == "admin" and password == "admin123":
            QMessageBox.information(self, "Sucesso", "Login bem-sucedido!")
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")

# Garantir que a classe possa ser importada corretamente
__all__ = ['LoginDialog']
