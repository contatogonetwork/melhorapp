# login_dialog.py
# Implementação do diálogo de login

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from utils.logger import get_logger


class LoginDialog(QDialog):
    """
    Diálogo de login para autenticação de usuários.

    Esta classe apresenta uma interface de login com campos para
    nome de usuário e senha, além de validação de credenciais.
    """

    def __init__(self):
        """Inicializa o diálogo de login com todos os componentes visuais."""
        super().__init__()
        self.logger = get_logger("login_dialog")
        self.setWindowTitle("Login")
        self.resize(300, 150)

        # Configurações visuais
        self.setWindowFlags(
            Qt.Dialog
            | Qt.CustomizeWindowHint
            | Qt.WindowTitleHint
            | Qt.WindowCloseButtonHint
        )

        # Layout principal
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        # Campo de usuário
        self.username_label = QLabel("Usuário:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Digite seu usuário")
        self.username_input.textChanged.connect(self.validate_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Campo de senha
        self.password_label = QLabel("Senha:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Digite sua senha")
        self.password_input.textChanged.connect(self.validate_input)
        # Permite pressionar Enter para fazer login
        self.password_input.returnPressed.connect(self.handle_login)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Botão de login
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setEnabled(False)  # Inicialmente desabilitado
        layout.addWidget(self.login_button)

        self.setLayout(layout)

        # Focar no campo de usuário inicialmente
        self.username_input.setFocus()

    def validate_input(self):
        """
        Valida os campos de entrada para habilitar/desabilitar o botão de login.

        O botão de login só é habilitado quando ambos os campos contêm texto.
        """
        has_username = bool(self.username_input.text().strip())
        has_password = bool(self.password_input.text().strip())
        self.login_button.setEnabled(has_username and has_password)

    def handle_login(self):
        """
        Processa a tentativa de login quando o botão é clicado.

        Verifica as credenciais e apresenta mensagem apropriada ao usuário.
        """
        if not self.login_button.isEnabled():
            return

        # Mostra indicador de carregamento
        QApplication.setOverrideCursor(Qt.WaitCursor)

        try:
            username = self.username_input.text().strip()
            password = self.password_input.text()

            # Simulação de validação de login
            if username == "admin" and password == "admin123":
                self.logger.info(f"Login bem-sucedido: {username}")
                QApplication.restoreOverrideCursor()
                QMessageBox.information(self, "Sucesso", "Login bem-sucedido!")
                self.accept()
            else:
                self.logger.warning(f"Tentativa de login falhou: {username}")
                QApplication.restoreOverrideCursor()
                QMessageBox.warning(
                    self,
                    "Erro de Login",
                    "Usuário ou senha incorretos. Tente novamente.",
                )
                self.password_input.clear()
                self.password_input.setFocus()
        except Exception as e:
            self.logger.error(f"Erro durante login: {str(e)}")
            QApplication.restoreOverrideCursor()
            QMessageBox.critical(
                self, "Erro", f"Ocorreu um erro durante o login: {str(e)}"
            )
        finally:
            # Garante que o cursor seja restaurado mesmo em caso de erro
            if QApplication.overrideCursor():
                QApplication.restoreOverrideCursor()


# Garantir que a classe possa ser importada corretamente
__all__ = ["LoginDialog"]
