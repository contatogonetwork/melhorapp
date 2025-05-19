"""
Widget para exibir informações de versão de uma edição de vídeo
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class VersionInfoWidget(QFrame):
    """Widget para exibir informações sobre uma versão de vídeo"""

    def __init__(self, delivery_data=None, parent=None):
        super().__init__(parent)
        self.delivery_data = delivery_data
        self.setup_ui()

    def setup_ui(self):
        """Configura a interface do widget"""
        # Configurar o frame
        self.setFrameShape(QFrame.StyledPanel)
        self.setObjectName("versionInfoFrame")
        self.setStyleSheet(
            f"QFrame#versionInfoFrame {{background-color: {style.BG_THREE}; "
            f"border-radius: 6px; padding: 10px;}}"
        )

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(8)

        # Título e data
        header_layout = QHBoxLayout()

        self.title_label = QLabel("Informações da Versão")
        self.title_label.setStyleSheet(
            f"font-weight: bold; font-size: 14px; color: {style.foreground_color};"
        )

        self.date_label = QLabel("")
        self.date_label.setStyleSheet(f"color: {style.comment_color};")
        self.date_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        header_layout.addWidget(self.title_label)
        header_layout.addWidget(self.date_label, 1)

        # Status
        status_layout = QHBoxLayout()

        status_title = QLabel("Status:")
        status_title.setStyleSheet(
            f"font-weight: bold; color: {style.foreground_color};"
        )

        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"color: {style.cyan_color};")

        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status_label)
        status_layout.addStretch()

        # Referências de assets
        assets_layout = QHBoxLayout()

        assets_title = QLabel("Assets:")
        assets_title.setStyleSheet(
            f"font-weight: bold; color: {style.foreground_color};"
        )

        self.assets_label = QLabel("")
        self.assets_label.setStyleSheet(f"color: {style.foreground_color};")
        self.assets_label.setWordWrap(True)

        assets_layout.addWidget(assets_title, 0)
        assets_layout.addWidget(self.assets_label, 1)

        # Adicionar tudo ao layout principal
        main_layout.addLayout(header_layout)
        main_layout.addLayout(status_layout)
        main_layout.addLayout(assets_layout)

        # Se não houver dados, mostrar mensagem padrão
        if not self.delivery_data:
            self.show_default_info()
        else:
            self.update_info(self.delivery_data)

    def show_default_info(self):
        """Mostra informações padrão quando não há dados"""
        self.title_label.setText("Nenhuma versão selecionada")
        self.date_label.setText("")
        self.status_label.setText("N/A")
        self.assets_label.setText("Nenhum asset disponível")

    def update_info(self, delivery_data):
        """Atualiza as informações com os dados da entrega"""
        if not delivery_data:
            self.show_default_info()
            return

        # Atualizar título
        self.title_label.setText("Versão atual")

        # Atualizar data de envio
        submitted_at = delivery_data.get("submitted_at", "").split(" ")[0]
        if submitted_at:
            # Converter de YYYY-MM-DD para DD/MM/YYYY
            parts = submitted_at.split("-")
            if len(parts) == 3:
                submitted_at = f"{parts[2]}/{parts[1]}/{parts[0]}"
            self.date_label.setText(f"Enviado em: {submitted_at}")

        # Atualizar status
        status = delivery_data.get("approval_status", "Pendente")
        self.status_label.setText(status)

        # Definir cor do status
        if status == "Aprovado":
            self.status_label.setStyleSheet(
                f"color: {style.green_color}; font-weight: bold;"
            )
        elif status == "Rejeitado":
            self.status_label.setStyleSheet(
                f"color: {style.red_color}; font-weight: bold;"
            )
        elif status == "Aguardando aprovação":
            self.status_label.setStyleSheet(
                f"color: {style.orange_color}; font-weight: bold;"
            )
        else:
            self.status_label.setStyleSheet(f"color: {style.comment_color};")

        # Atualizar assets
        assets = delivery_data.get("asset_refs", "")
        if assets:
            if assets.startswith("http"):
                self.assets_label.setText(f"<a href='{assets}'>{assets}</a>")
                self.assets_label.setOpenExternalLinks(True)
            else:
                self.assets_label.setText(assets)
        else:
            self.assets_label.setText("Nenhum asset disponível")
