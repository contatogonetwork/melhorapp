from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog, QMessageBox
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPixmap

import gui.themes.dracula as style

class TeamWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Cabeçalho
        self.header_layout = QHBoxLayout()
        
        # Título
        self.title_label = QLabel("Gerenciamento de Equipe")
        self.title_label.setStyleSheet(f"color: {style.foreground_color}; font-size: 24px; font-weight: bold;")
        
        # Botões
        self.button_layout = QHBoxLayout()
        self.button_layout.setSpacing(10)
        
        self.add_member_button = QPushButton("Adicionar Membro")
        self.add_member_button.setIcon(QIcon("./resources/icons/user-add.svg"))
        self.add_member_button.setFixedHeight(36)
        self.add_member_button.setStyleSheet(style.button_style)
        self.add_member_button.clicked.connect(self.adicionar_membro)
        
        self.add_client_button = QPushButton("Adicionar Cliente")
        self.add_client_button.setIcon(QIcon("./resources/icons/client-add.svg"))
        self.add_client_button.setFixedHeight(36)
        self.add_client_button.setStyleSheet(style.secondary_button_style)
        self.add_client_button.clicked.connect(self.adicionar_cliente)
        
        self.button_layout.addWidget(self.add_member_button)
        self.button_layout.addWidget(self.add_client_button)
        
        # Adicionar ao layout do cabeçalho
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addLayout(self.button_layout)
        
        # Tabela de membros da equipe
        self.team_frame = QFrame()
        self.team_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
                border: 1px solid {style.current_line_color};
            }}
        """)
        
        self.team_layout = QVBoxLayout(self.team_frame)
        self.team_layout.setContentsMargins(15, 15, 15, 15)
        self.team_layout.setSpacing(10)
        
        # Título da seção
        self.team_section_title = QLabel("Membros da Equipe")
        self.team_section_title.setStyleSheet(f"color: {style.foreground_color}; font-size: 16px; font-weight: bold;")
        self.team_layout.addWidget(self.team_section_title)
        
        # Tabela de membros
        self.team_table = QTableWidget()
        self.team_table.setColumnCount(5)
        self.team_table.setHorizontalHeaderLabels(["Nome", "Função", "Email", "Contato", "Ações"])
        self.team_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.team_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.team_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.team_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.team_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.team_table.setStyleSheet(style.table_style)
        
        # Adicionar dados de exemplo
        self.add_sample_team()
        
        self.team_layout.addWidget(self.team_table)
        
        # Tabela de clientes
        self.client_frame = QFrame()
        self.client_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
                border: 1px solid {style.current_line_color};
            }}
        """)
        
        self.client_layout = QVBoxLayout(self.client_frame)
        self.client_layout.setContentsMargins(15, 15, 15, 15)
        self.client_layout.setSpacing(10)
        
        # Título da seção
        self.client_section_title = QLabel("Clientes")
        self.client_section_title.setStyleSheet(f"color: {style.foreground_color}; font-size: 16px; font-weight: bold;")
        self.client_layout.addWidget(self.client_section_title)
        
        # Tabela de clientes
        self.client_table = QTableWidget()
        self.client_table.setColumnCount(5)
        self.client_table.setHorizontalHeaderLabels(["Empresa/Cliente", "Responsável", "Email", "Telefone", "Ações"])
        self.client_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.client_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.client_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.client_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.client_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.client_table.setStyleSheet(style.table_style)
        
        # Adicionar dados de exemplo
        self.add_sample_clients()
        
        self.client_layout.addWidget(self.client_table)
        
        # Adicionar todos os layouts ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.team_frame)
        self.layout.addWidget(self.client_frame)
    
    def add_sample_team(self):
        # Dados de exemplo
        team = [
            ["Maria Souza", "Editora de Vídeo", "maria@gonetwork.ai", "(11) 98765-4321"],
            ["Pedro Alves", "Diretor de Fotografia", "pedro@gonetwork.ai", "(11) 97654-3210"],
            ["Ana Silva", "Produtora", "ana@gonetwork.ai", "(11) 96543-2109"],
            ["Carlos Mendes", "Editor de Áudio", "carlos@gonetwork.ai", "(11) 95432-1098"],
            ["Luciana Santos", "Motion Designer", "luciana@gonetwork.ai", "(11) 94321-0987"],
        ]
        
        self.team_table.setRowCount(len(team))
        
        for row, member in enumerate(team):
            # Nome
            self.team_table.setItem(row, 0, QTableWidgetItem(member[0]))
            
            # Função
            self.team_table.setItem(row, 1, QTableWidgetItem(member[1]))
            
            # Email
            email_container = QWidget()
            email_layout = QHBoxLayout(email_container)
            email_layout.setContentsMargins(5, 0, 5, 0)
            email_layout.setSpacing(5)
            
            email_label = QLabel(member[2])
            email_label.setStyleSheet(f"color: {style.foreground_color};")
            
            email_icon = QPushButton()
            email_icon.setIcon(QIcon("./resources/icons/email.svg"))
            email_icon.setToolTip("Enviar Email")
            email_icon.setIconSize(QSize(16, 16))
            email_icon.setFixedSize(24, 24)
            email_icon.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: {style.current_line_color};
                    border-radius: 12px;
                }}
            """)
            
            email_layout.addWidget(email_label)
            email_layout.addWidget(email_icon)
            email_layout.addStretch()
            
            self.team_table.setCellWidget(row, 2, email_container)
            
            # Contato
            self.team_table.setItem(row, 3, QTableWidgetItem(member[3]))
            
            # Ações
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)
            actions_layout.setSpacing(5)
            
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
            edit_btn.setToolTip("Editar")
            edit_btn.setIconSize(QSize(16, 16))
            edit_btn.setFixedSize(28, 28)
            edit_btn.setStyleSheet(style.secondary_button_style)
            
            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("./resources/icons/delete.svg"))
            delete_btn.setToolTip("Remover")
            delete_btn.setIconSize(QSize(16, 16))
            delete_btn.setFixedSize(28, 28)
            delete_btn.setStyleSheet(style.secondary_button_style)
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            self.team_table.setCellWidget(row, 4, actions_widget)
    
    def add_sample_clients(self):
        # Dados de exemplo
        clients = [
            ["Empresa ABC", "João Oliveira", "joao@empresaabc.com", "(11) 3456-7890"],
            ["XYZ Corp", "Fernanda Gomes", "fernanda@xyzcorp.com", "(11) 2345-6789"],
            ["Tech Solutions", "Ricardo Dias", "ricardo@techsolutions.com", "(11) 4567-8901"],
            ["Consultoria DEF", "Amanda Cruz", "amanda@def.com.br", "(11) 5678-9012"],
            ["Associação GHI", "Roberto Lima", "roberto@ghi.org.br", "(11) 6789-0123"],
        ]
        
        self.client_table.setRowCount(len(clients))
        
        for row, client in enumerate(clients):
            # Empresa/Cliente
            self.client_table.setItem(row, 0, QTableWidgetItem(client[0]))
            
            # Responsável
            self.client_table.setItem(row, 1, QTableWidgetItem(client[1]))
            
            # Email
            email_container = QWidget()
            email_layout = QHBoxLayout(email_container)
            email_layout.setContentsMargins(5, 0, 5, 0)
            email_layout.setSpacing(5)
            
            email_label = QLabel(client[2])
            email_label.setStyleSheet(f"color: {style.foreground_color};")
            
            email_icon = QPushButton()
            email_icon.setIcon(QIcon("./resources/icons/email.svg"))
            email_icon.setToolTip("Enviar Email")
            email_icon.setIconSize(QSize(16, 16))
            email_icon.setFixedSize(24, 24)
            email_icon.setStyleSheet(f"""
                QPushButton {{
                    background-color: transparent;
                    border: none;
                }}
                QPushButton:hover {{
                    background-color: {style.current_line_color};
                    border-radius: 12px;
                }}
            """)
            
            email_layout.addWidget(email_label)
            email_layout.addWidget(email_icon)
            email_layout.addStretch()
            
            self.client_table.setCellWidget(row, 2, email_container)
            
            # Telefone
            self.client_table.setItem(row, 3, QTableWidgetItem(client[3]))
            
            # Ações
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)
            actions_layout.setSpacing(5)
            
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
            edit_btn.setToolTip("Editar")
            edit_btn.setIconSize(QSize(16, 16))
            edit_btn.setFixedSize(28, 28)
            edit_btn.setStyleSheet(style.secondary_button_style)
            
            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("./resources/icons/delete.svg"))
            delete_btn.setToolTip("Remover")
            delete_btn.setIconSize(QSize(16, 16))
            delete_btn.setFixedSize(28, 28)
            delete_btn.setStyleSheet(style.secondary_button_style)
            
            view_btn = QPushButton()
            view_btn.setIcon(QIcon("./resources/icons/view.svg"))
            view_btn.setToolTip("Ver Detalhes")
            view_btn.setIconSize(QSize(16, 16))
            view_btn.setFixedSize(28, 28)
            view_btn.setStyleSheet(style.secondary_button_style)
            
            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()
            
            self.client_table.setCellWidget(row, 4, actions_widget)
    
    def adicionar_membro(self):
        """Adiciona um novo membro à equipe"""
        nome, ok1 = QInputDialog.getText(self, "Novo Membro", "Nome:")
        if not ok1 or not nome:
            return
            
        funcao, ok2 = QInputDialog.getText(self, "Novo Membro", "Função:")
        if not ok2 or not funcao:
            return
            
        email, ok3 = QInputDialog.getText(self, "Novo Membro", "Email:")
        if not ok3 or not email:
            return
            
        contato, ok4 = QInputDialog.getText(self, "Novo Membro", "Contato:")
        if not ok4 or not contato:
            return
        
        # Adicionar à tabela
        row = self.team_table.rowCount()
        self.team_table.insertRow(row)
        
        # Nome
        self.team_table.setItem(row, 0, QTableWidgetItem(nome))
        
        # Função
        self.team_table.setItem(row, 1, QTableWidgetItem(funcao))
        
        # Email com ícone
        email_container = QWidget()
        email_layout = QHBoxLayout(email_container)
        email_layout.setContentsMargins(5, 0, 5, 0)
        email_layout.setSpacing(5)
        
        email_label = QLabel(email)
        email_label.setStyleSheet(f"color: {style.foreground_color};")
        
        email_icon = QPushButton()
        email_icon.setIcon(QIcon("./resources/icons/email.svg"))
        email_icon.setToolTip("Enviar Email")
        email_icon.setIconSize(QSize(16, 16))
        email_icon.setFixedSize(24, 24)
        email_icon.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {style.current_line_color};
                border-radius: 12px;
            }}
        """)
        
        email_layout.addWidget(email_label)
        email_layout.addWidget(email_icon)
        email_layout.addStretch()
        
        self.team_table.setCellWidget(row, 2, email_container)
        
        # Contato
        self.team_table.setItem(row, 3, QTableWidgetItem(contato))
        
        # Ações
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 0, 5, 0)
        actions_layout.setSpacing(5)
        
        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
        edit_btn.setToolTip("Editar")
        edit_btn.setIconSize(QSize(16, 16))
        edit_btn.setFixedSize(28, 28)
        edit_btn.setStyleSheet(style.secondary_button_style)
        
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("./resources/icons/delete.svg"))
        delete_btn.setToolTip("Remover")
        delete_btn.setIconSize(QSize(16, 16))
        delete_btn.setFixedSize(28, 28)
        delete_btn.setStyleSheet(style.secondary_button_style)
        
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.addStretch()
        
        self.team_table.setCellWidget(row, 4, actions_widget)
        
        QMessageBox.information(self, "Sucesso", f"Membro '{nome}' adicionado com sucesso!")
    
    def adicionar_cliente(self):
        """Adiciona um novo cliente"""
        empresa, ok1 = QInputDialog.getText(self, "Novo Cliente", "Empresa:")
        if not ok1 or not empresa:
            return
            
        responsavel, ok2 = QInputDialog.getText(self, "Novo Cliente", "Responsável:")
        if not ok2 or not responsavel:
            return
            
        email, ok3 = QInputDialog.getText(self, "Novo Cliente", "Email:")
        if not ok3 or not email:
            return
            
        telefone, ok4 = QInputDialog.getText(self, "Novo Cliente", "Telefone:")
        if not ok4 or not telefone:
            return
        
        # Adicionar à tabela
        row = self.client_table.rowCount()
        self.client_table.insertRow(row)
        
        # Empresa
        self.client_table.setItem(row, 0, QTableWidgetItem(empresa))
        
        # Responsável
        self.client_table.setItem(row, 1, QTableWidgetItem(responsavel))
        
        # Email com ícone
        email_container = QWidget()
        email_layout = QHBoxLayout(email_container)
        email_layout.setContentsMargins(5, 0, 5, 0)
        email_layout.setSpacing(5)
        
        email_label = QLabel(email)
        email_label.setStyleSheet(f"color: {style.foreground_color};")
        
        email_icon = QPushButton()
        email_icon.setIcon(QIcon("./resources/icons/email.svg"))
        email_icon.setToolTip("Enviar Email")
        email_icon.setIconSize(QSize(16, 16))
        email_icon.setFixedSize(24, 24)
        email_icon.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {style.current_line_color};
                border-radius: 12px;
            }}
        """)
        
        email_layout.addWidget(email_label)
        email_layout.addWidget(email_icon)
        email_layout.addStretch()
        
        self.client_table.setCellWidget(row, 2, email_container)
        
        # Telefone
        self.client_table.setItem(row, 3, QTableWidgetItem(telefone))
        
        # Ações
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 0, 5, 0)
        actions_layout.setSpacing(5)
        
        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
        edit_btn.setToolTip("Editar")
        edit_btn.setIconSize(QSize(16, 16))
        edit_btn.setFixedSize(28, 28)
        edit_btn.setStyleSheet(style.secondary_button_style)
        
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("./resources/icons/delete.svg"))
        delete_btn.setToolTip("Remover")
        delete_btn.setIconSize(QSize(16, 16))
        delete_btn.setFixedSize(28, 28)
        delete_btn.setStyleSheet(style.secondary_button_style)
        
        view_btn = QPushButton()
        view_btn.setIcon(QIcon("./resources/icons/view.svg"))
        view_btn.setToolTip("Ver Detalhes")
        view_btn.setIconSize(QSize(16, 16))
        view_btn.setFixedSize(28, 28)
        view_btn.setStyleSheet(style.secondary_button_style)
        
        actions_layout.addWidget(view_btn)
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.addStretch()
        
        self.client_table.setCellWidget(row, 4, actions_widget)
        
        QMessageBox.information(self, "Sucesso", f"Cliente '{empresa}' adicionado com sucesso!")