import os

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style
import utils.helpers as helpers


class SettingsWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Cabeçalho
        self.header_layout = QHBoxLayout()

        # Título
        self.title_label = QLabel("Configurações")
        self.title_label.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 24px; font-weight: bold;"
        )

        # Botão de salvar
        self.save_button = QPushButton("Salvar Configurações")
        self.save_button.setIcon(QIcon("./resources/icons/save.svg"))
        self.save_button.setStyleSheet(style.button_style)
        self.save_button.setFixedHeight(36)

        # Adicionar ao layout do cabeçalho
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.save_button)

        # Tabs para diferentes categorias de configurações
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            f"""
            QTabWidget::pane {{
                border: 1px solid {style.current_line_color};
                border-radius: 5px;
                padding: 10px;
            }}
            QTabBar::tab {{
                background-color: {style.background_color};
                color: {style.comment_color};
                border: 1px solid {style.current_line_color};
                padding: 8px 20px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                margin-right: 2px;
            }}
            QTabBar::tab:selected {{
                background-color: {style.current_line_color};
                color: {style.pink_color};
                border-bottom-color: {style.pink_color};
            }}
        """
        )

        # Tab de configurações gerais
        self.general_tab = QWidget()
        self.general_layout = QVBoxLayout(self.general_tab)

        # Grupo de configurações do aplicativo
        self.app_group = QGroupBox("Configurações do Aplicativo")
        self.app_group.setStyleSheet(
            f"""
            QGroupBox {{
                font-weight: bold;
                color: {style.purple_color};
                border: 1px solid {style.purple_color};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """
        )

        self.app_form = QFormLayout(self.app_group)
        self.app_form.setLabelAlignment(Qt.AlignRight)

        # Tema
        self.theme_combo = QComboBox()
        self.theme_combo.setStyleSheet(style.combobox_style)
        self.theme_combo.setFixedWidth(200)
        self.theme_combo.addItems(["Dracula (Padrão)", "Claro", "Escuro"])
        self.app_form.addRow("Tema:", self.theme_combo)

        # Idioma
        self.language_combo = QComboBox()
        self.language_combo.setStyleSheet(style.combobox_style)
        self.language_combo.setFixedWidth(200)
        self.language_combo.addItems(
            ["Português (Brasil)", "English", "Español"]
        )
        self.app_form.addRow("Idioma:", self.language_combo)

        # Notificações
        self.notifications_check = QCheckBox("Ativar notificações")
        self.notifications_check.setStyleSheet(
            f"""
            QCheckBox {{
                color: {style.foreground_color};
            }}
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 1px solid {style.comment_color};
                border-radius: 3px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {style.green_color};
                border: 1px solid {style.green_color};
            }}
        """
        )
        self.notifications_check.setChecked(True)
        self.app_form.addRow("Notificações:", self.notifications_check)

        # Intervalo de verificação
        self.check_interval = QSpinBox()
        self.check_interval.setStyleSheet(style.input_style)
        self.check_interval.setMinimum(1)
        self.check_interval.setMaximum(120)
        self.check_interval.setValue(60)
        self.check_interval.setSuffix(" min")
        self.check_interval.setFixedWidth(100)
        self.app_form.addRow("Intervalo de verificação:", self.check_interval)

        # Adicionar grupo de app ao tab geral
        self.general_layout.addWidget(self.app_group)

        # Grupo de diretórios
        self.dirs_group = QGroupBox("Diretórios")
        self.dirs_group.setStyleSheet(
            f"""
            QGroupBox {{
                font-weight: bold;
                color: {style.purple_color};
                border: 1px solid {style.purple_color};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """
        )

        self.dirs_form = QFormLayout(self.dirs_group)
        self.dirs_form.setLabelAlignment(Qt.AlignRight)

        # Diretório de uploads
        self.upload_dir_layout = QHBoxLayout()
        self.upload_dir_input = QLineEdit("./uploads")
        self.upload_dir_input.setStyleSheet(style.input_style)
        self.upload_dir_input.setReadOnly(True)

        self.upload_dir_button = QPushButton("Escolher")
        self.upload_dir_button.setIcon(QIcon("./resources/icons/folder.svg"))
        self.upload_dir_button.setStyleSheet(style.secondary_button_style)
        self.upload_dir_button.clicked.connect(
            lambda: self.choose_directory(self.upload_dir_input)
        )

        self.upload_dir_layout.addWidget(self.upload_dir_input)
        self.upload_dir_layout.addWidget(self.upload_dir_button)

        self.dirs_form.addRow("Diretório de uploads:", self.upload_dir_layout)

        # Diretório de exportação
        self.export_dir_layout = QHBoxLayout()
        self.export_dir_input = QLineEdit("./exports")
        self.export_dir_input.setStyleSheet(style.input_style)
        self.export_dir_input.setReadOnly(True)

        self.export_dir_button = QPushButton("Escolher")
        self.export_dir_button.setIcon(QIcon("./resources/icons/folder.svg"))
        self.export_dir_button.setStyleSheet(style.secondary_button_style)
        self.export_dir_button.clicked.connect(
            lambda: self.choose_directory(self.export_dir_input)
        )

        self.export_dir_layout.addWidget(self.export_dir_input)
        self.export_dir_layout.addWidget(self.export_dir_button)

        self.dirs_form.addRow(
            "Diretório de exportação:", self.export_dir_layout
        )

        # Adicionar grupo de diretórios ao tab geral
        self.general_layout.addWidget(self.dirs_group)

        # Espaçador
        self.general_layout.addStretch()

        # Tab de configurações de vídeo
        self.video_tab = QWidget()
        self.video_layout = QVBoxLayout(self.video_tab)

        # Grupo de configurações de vídeo
        self.video_group = QGroupBox("Configurações de Vídeo")
        self.video_group.setStyleSheet(
            f"""
            QGroupBox {{
                font-weight: bold;
                color: {style.purple_color};
                border: 1px solid {style.purple_color};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """
        )

        self.video_form = QFormLayout(self.video_group)
        self.video_form.setLabelAlignment(Qt.AlignRight)

        # Qualidade padrão
        self.quality_combo = QComboBox()
        self.quality_combo.setStyleSheet(style.combobox_style)
        self.quality_combo.setFixedWidth(200)
        self.quality_combo.addItems(["4K", "1080p", "720p", "480p"])
        self.quality_combo.setCurrentText("720p")
        self.video_form.addRow("Qualidade padrão:", self.quality_combo)

        # Formatos suportados
        self.format_layout = QHBoxLayout()
        self.mp4_check = QCheckBox("MP4")
        self.mp4_check.setChecked(True)
        self.mp4_check.setStyleSheet(f"color: {style.foreground_color};")

        self.mov_check = QCheckBox("MOV")
        self.mov_check.setChecked(True)
        self.mov_check.setStyleSheet(f"color: {style.foreground_color};")

        self.avi_check = QCheckBox("AVI")
        self.avi_check.setChecked(True)
        self.avi_check.setStyleSheet(f"color: {style.foreground_color};")

        self.format_layout.addWidget(self.mp4_check)
        self.format_layout.addWidget(self.mov_check)
        self.format_layout.addWidget(self.avi_check)
        self.format_layout.addStretch()

        self.video_form.addRow("Formatos suportados:", self.format_layout)

        # Adicionar grupo de vídeo ao tab de vídeo
        self.video_layout.addWidget(self.video_group)

        # Grupo de configurações de uploads
        self.upload_group = QGroupBox("Configurações de Upload")
        self.upload_group.setStyleSheet(
            f"""
            QGroupBox {{
                font-weight: bold;
                color: {style.purple_color};
                border: 1px solid {style.purple_color};
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 15px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }}
        """
        )

        self.upload_form = QFormLayout(self.upload_group)
        self.upload_form.setLabelAlignment(Qt.AlignRight)

        # Tamanho máximo
        self.max_size = QSpinBox()
        self.max_size.setStyleSheet(style.input_style)
        self.max_size.setMinimum(1)
        self.max_size.setMaximum(10240)
        self.max_size.setValue(2048)
        self.max_size.setSuffix(" MB")
        self.max_size.setFixedWidth(100)
        self.upload_form.addRow("Tamanho máximo:", self.max_size)

        # Tipos permitidos
        self.types_layout = QVBoxLayout()

        self.image_check = QCheckBox("Imagens (JPEG, PNG, GIF)")
        self.image_check.setChecked(True)
        self.image_check.setStyleSheet(f"color: {style.foreground_color};")

        self.video_check = QCheckBox("Vídeos (MP4, MOV, AVI)")
        self.video_check.setChecked(True)
        self.video_check.setStyleSheet(f"color: {style.foreground_color};")

        self.audio_check = QCheckBox("Áudios (MP3, WAV)")
        self.audio_check.setChecked(True)
        self.audio_check.setStyleSheet(f"color: {style.foreground_color};")

        self.doc_check = QCheckBox("Documentos (PDF, DOC)")
        self.doc_check.setChecked(True)
        self.doc_check.setStyleSheet(f"color: {style.foreground_color};")

        self.zip_check = QCheckBox("Arquivos compactados (ZIP, RAR)")
        self.zip_check.setChecked(True)
        self.zip_check.setStyleSheet(f"color: {style.foreground_color};")

        self.types_layout.addWidget(self.image_check)
        self.types_layout.addWidget(self.video_check)
        self.types_layout.addWidget(self.audio_check)
        self.types_layout.addWidget(self.doc_check)
        self.types_layout.addWidget(self.zip_check)

        self.upload_form.addRow("Tipos permitidos:", self.types_layout)

        # Adicionar grupo de uploads ao tab de vídeo
        self.video_layout.addWidget(self.upload_group)

        # Espaçador
        self.video_layout.addStretch()

        # Adicionar tabs ao widget de tabs
        self.tabs.addTab(self.general_tab, "Geral")
        self.tabs.addTab(self.video_tab, "Vídeo e Uploads")

        # Adicionar todos os layouts ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.tabs)

        # Carregar configurações existentes
        self.load_settings()

        # Conectar sinais
        self.save_button.clicked.connect(self.save_settings)

    def choose_directory(self, input_field):
        """Abre um diálogo para escolher um diretório"""
        current_dir = input_field.text() or "./"
        directory = QFileDialog.getExistingDirectory(
            self, "Selecionar Diretório", current_dir, QFileDialog.ShowDirsOnly
        )
        if directory:
            input_field.setText(directory)

    def load_settings(self):
        """Carrega configurações do arquivo config.json"""
        try:
            config = helpers.load_config()

            # Configurações do aplicativo
            if "app" in config:
                if "theme" in config["app"]:
                    theme = config["app"]["theme"]
                    if theme == "dracula":
                        self.theme_combo.setCurrentText("Dracula (Padrão)")
                    elif theme == "light":
                        self.theme_combo.setCurrentText("Claro")
                    elif theme == "dark":
                        self.theme_combo.setCurrentText("Escuro")

            # Configurações de notificações
            if "notifications" in config:
                self.notifications_check.setChecked(
                    config["notifications"].get("enabled", True)
                )
                self.check_interval.setValue(
                    config["notifications"].get("check_interval", 60)
                )

            # Diretórios
            if "uploads" in config and "path" in config["uploads"]:
                self.upload_dir_input.setText(config["uploads"]["path"])

            # Configurações de vídeo
            if "video" in config:
                if "default_quality" in config["video"]:
                    self.quality_combo.setCurrentText(
                        config["video"]["default_quality"]
                    )

                if "formats" in config["video"]:
                    formats = config["video"]["formats"]
                    self.mp4_check.setChecked("mp4" in formats)
                    self.mov_check.setChecked("mov" in formats)
                    self.avi_check.setChecked("avi" in formats)

            # Configurações de upload
            if "uploads" in config:
                if "max_size" in config["uploads"]:
                    self.max_size.setValue(config["uploads"]["max_size"])

                if "allowed_types" in config["uploads"]:
                    types = config["uploads"]["allowed_types"]
                    self.image_check.setChecked(
                        "image/jpeg" in types or "image/png" in types
                    )
                    self.video_check.setChecked("video/mp4" in types)
                    self.audio_check.setChecked("audio/mpeg" in types)
                    self.doc_check.setChecked("application/pdf" in types)
                    self.zip_check.setChecked("application/zip" in types)

        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")

    def save_settings(self):
        """Salva as configurações no arquivo config.json"""
        try:
            config = helpers.load_config() or {}

            # Configurações do aplicativo
            if "app" not in config:
                config["app"] = {}

            theme_text = self.theme_combo.currentText()
            if theme_text == "Dracula (Padrão)":
                config["app"]["theme"] = "dracula"
            elif theme_text == "Claro":
                config["app"]["theme"] = "light"
            elif theme_text == "Escuro":
                config["app"]["theme"] = "dark"

            # Configurações de notificações
            if "notifications" not in config:
                config["notifications"] = {}

            config["notifications"][
                "enabled"
            ] = self.notifications_check.isChecked()
            config["notifications"][
                "check_interval"
            ] = self.check_interval.value()

            # Diretórios
            if "uploads" not in config:
                config["uploads"] = {}

            config["uploads"]["path"] = self.upload_dir_input.text()

            # Configurações de vídeo
            if "video" not in config:
                config["video"] = {}

            config["video"][
                "default_quality"
            ] = self.quality_combo.currentText()

            formats = []
            if self.mp4_check.isChecked():
                formats.append("mp4")
            if self.mov_check.isChecked():
                formats.append("mov")
            if self.avi_check.isChecked():
                formats.append("avi")

            config["video"]["formats"] = formats

            # Configurações de upload
            config["uploads"]["max_size"] = self.max_size.value()

            allowed_types = []
            if self.image_check.isChecked():
                allowed_types.extend(["image/jpeg", "image/png"])
            if self.video_check.isChecked():
                allowed_types.extend(["video/mp4", "video/quicktime"])
            if self.audio_check.isChecked():
                allowed_types.extend(["audio/mpeg", "audio/wav"])
            if self.doc_check.isChecked():
                allowed_types.extend(["application/pdf", "application/msword"])
            if self.zip_check.isChecked():
                allowed_types.extend(
                    ["application/zip", "application/x-rar-compressed"]
                )

            config["uploads"]["allowed_types"] = allowed_types

            # Salvar configurações
            config_path = "./config.json"
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)

            # Criar diretório de uploads se não existir
            uploads_path = config["uploads"]["path"]
            os.makedirs(uploads_path, exist_ok=True)

            # Mostrar mensagem de sucesso
            helpers.show_message(
                "Sucesso", "Configurações salvas com sucesso!"
            )

        except Exception as e:
            helpers.show_message("Erro", f"Erro ao salvar configurações: {e}")
