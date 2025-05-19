import os
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from gui.splash_screen import SplashScreen

# Garantir que o diretório atual esteja no path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Criar aplicação
    app = QApplication(sys.argv)
    app.setApplicationName("GoNetwork AI")

    # Exibir tela de splash
    splash = SplashScreen()
    splash.show()

    # Criar e iniciar janela principal após o splash
    window = MainWindow()

    # Temporizador para fechar o splash e mostrar janela principal
    def show_main_window():
        splash.close()
        window.show()

    QTimer.singleShot(3000, show_main_window)  # 3 segundos de splash

    # Executar aplicação
    sys.exit(app.exec())
