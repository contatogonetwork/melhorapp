"""
Testa importações do PySide6
"""


def test_imports():
    try:
        from PySide6.QtCore import QObject

        print("QtCore: OK")
    except Exception as e:
        print(f"QtCore: ERRO - {str(e)}")

    try:
        from PySide6.QtWidgets import QWidget

        print("QtWidgets: OK")
    except Exception as e:
        print(f"QtWidgets: ERRO - {str(e)}")

    try:
        from PySide6.QtGui import QIcon

        print("QtGui: OK")
    except Exception as e:
        print(f"QtGui: ERRO - {str(e)}")

    try:
        from PySide6.QtMultimedia import QMediaPlayer

        print("QtMultimedia: OK")
    except Exception as e:
        print(f"QtMultimedia: ERRO - {str(e)}")

    try:
        from PySide6.QtMultimediaWidgets import QVideoWidget

        print("QtMultimediaWidgets: OK")
    except Exception as e:
        print(f"QtMultimediaWidgets: ERRO - {str(e)}")


if __name__ == "__main__":
    print("Testando importações PySide6...")
    test_imports()
