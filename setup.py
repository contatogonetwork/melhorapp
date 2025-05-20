from cx_Freeze import Executable, setup

setup(
    name="GoNetwork AI",
    version="1.0",
    description="Sistema de Gerenciamento Audiovisual de Eventos",
    executables=[
        Executable(
            script="main.py",
            base="Win32GUI",
            target_name="gonetwork.exe",
            icon="resources/images/logo_gonetwork.ico",
        )
    ],
    options={
        "build_exe": {
            "packages": ["os", "sys", "sqlite3", "uuid", "datetime"],
            "includes": [
                "PySide6.QtCore",
                "PySide6.QtGui",
                "PySide6.QtWidgets",
                "PySide6.QtMultimedia",
            ],
            "excludes": ["tkinter", "PySide6.QtAsyncio"],
            "include_files": [
                "resources/",
                "database/",
                "gui/",
                "utils/",
                "config.json",
                "data/",
            ],
        }
    },
)
