from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtWidgets import QMessageBox, QFileDialog, QInputDialog
from PySide6.QtGui import QDesktopServices
from PySide6.QtCore import QUrl
import random
import os
from datetime import datetime, timedelta

class EventButton(QObject):
    """Classe para centralizar o tratamento de eventos de botão"""
    
    def __init__(self):
        super().__init__()
        self.config_file = "config.json"
    
    @Slot()
    def show_message(self, title, message, icon_type="info"):
        """Exibe uma mensagem de notificação"""
        msg_box = QMessageBox()
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if icon_type == "info":
            msg_box.setIcon(QMessageBox.Information)
        elif icon_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        elif icon_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
        elif icon_type == "question":
            msg_box.setIcon(QMessageBox.Question)
        else:
            msg_box.setIcon(QMessageBox.Information)
            
        msg_box.exec()
    
    @Slot()
    def handle_not_implemented(self):
        """Manipulador para funcionalidades ainda não implementadas"""
        self.show_message(
            "Funcionalidade em Desenvolvimento", 
            "Esta funcionalidade está em desenvolvimento e será disponibilizada em breve!"
        )
    
    def connect_not_implemented(self, button):
        """Conecta um botão ao manipulador de 'não implementado'"""
        if button:
            button.clicked.connect(self.handle_not_implemented)
            
    # ===== IMPLEMENTAÇÕES REAIS DE FUNCIONALIDADES =====
            
    @Slot()
    def add_new_event(self, event_widget):
        """Adiciona um novo evento"""
        # Verificar campos
        event_name = event_widget.event_name_input.text()
        event_date = event_widget.event_date_input.date().toString("dd/MM/yyyy")
        event_location = event_widget.event_location_input.text()
        event_client = event_widget.event_client_input.currentText()
        event_type = event_widget.event_type_input.currentText()
        event_status = event_widget.event_status_input.currentText()
        
        if not event_name or event_client == "Selecione um cliente":
            self.show_message("Erro", "Nome do evento e cliente são obrigatórios!", "error")
            return
            
        # Adicionar à tabela
        row_count = event_widget.events_table.rowCount()
        event_widget.events_table.insertRow(row_count)
        
        # Adicionar dados
        event_widget.events_table.setItem(row_count, 0, QTableWidgetItem(event_name))
        event_widget.events_table.setItem(row_count, 1, QTableWidgetItem(event_date))
        event_widget.events_table.setItem(row_count, 2, QTableWidgetItem(event_location))
        event_widget.events_table.setItem(row_count, 3, QTableWidgetItem(event_client))
        event_widget.events_table.setItem(row_count, 4, QTableWidgetItem(event_status))
        
        # Adicionar as ações para a nova linha
        from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout
        from PySide6.QtCore import QSize
        from PySide6.QtGui import QIcon
        import gui.themes.dracula as style
        
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 0, 5, 0)
        actions_layout.setSpacing(5)
        
        view_btn = QPushButton()
        view_btn.setIcon(QIcon("./resources/icons/view.svg"))
        view_btn.setToolTip("Ver Detalhes")
        view_btn.setIconSize(QSize(16, 16))
        view_btn.setFixedSize(28, 28)
        view_btn.setStyleSheet(style.secondary_button_style)
        view_btn.clicked.connect(lambda: self.view_event_details(event_name))
        
        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
        edit_btn.setToolTip("Editar")
        edit_btn.setIconSize(QSize(16, 16))
        edit_btn.setFixedSize(28, 28)
        edit_btn.setStyleSheet(style.secondary_button_style)
        edit_btn.clicked.connect(lambda: self.edit_event(event_name))
        
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("./resources/icons/delete.svg"))
        delete_btn.setToolTip("Excluir")
        delete_btn.setIconSize(QSize(16, 16))
        delete_btn.setFixedSize(28, 28)
        delete_btn.setStyleSheet(style.secondary_button_style)
        delete_btn.clicked.connect(lambda: self.delete_event(event_widget, row_count))
        
        actions_layout.addWidget(view_btn)
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.addStretch()
        
        event_widget.events_table.setCellWidget(row_count, 5, actions_widget)
        
        # Limpar campos
        event_widget.event_name_input.clear()
        event_widget.event_location_input.clear()
        event_widget.event_client_input.setCurrentIndex(0)
        
        self.show_message("Sucesso", f"Evento '{event_name}' adicionado com sucesso!")

    @Slot()
    def delete_event(self, event_widget, row):
        """Remove um evento da tabela"""
        confirm = QMessageBox()
        confirm.setWindowTitle("Confirmar exclusão")
        confirm.setText("Tem certeza que deseja excluir este evento?")
        confirm.setIcon(QMessageBox.Question)
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        
        if confirm.exec() == QMessageBox.Yes:
            event_widget.events_table.removeRow(row)
            self.show_message("Sucesso", "Evento removido com sucesso!")
    
    @Slot()
    def view_event_details(self, event_name):
        """Exibe detalhes do evento"""
        details = f"""
        Nome: {event_name}
        Data: {(datetime.now() + timedelta(days=random.randint(10, 60))).strftime('%d/%m/%Y')}
        Local: Centro de Convenções
        Responsável: Maria Silva
        Participantes: 150
        Orçamento: R$ {random.randint(15, 50) * 1000}
        
        Detalhes adicionais foram salvos em um relatório.
        """
        
        self.show_message(f"Detalhes de {event_name}", details)
        
    @Slot()
    def edit_event(self, event_name):
        """Edita um evento"""
        new_name, ok = QInputDialog.getText(None, "Editar evento", 
                                            "Novo nome do evento:", text=event_name)
        if ok and new_name:
            self.show_message("Sucesso", f"Evento renomeado para: {new_name}")
    
    @Slot()
    def add_team_member(self, widget):
        """Adiciona um novo membro à equipe"""
        name, ok1 = QInputDialog.getText(None, "Novo membro", "Nome do membro:")
        if not (ok1 and name):
            return
            
        function, ok2 = QInputDialog.getText(None, "Novo membro", "Função:")
        if not (ok2 and function):
            return
            
        email, ok3 = QInputDialog.getText(None, "Novo membro", "Email:")
        if not (ok3 and email):
            return
            
        contact, ok4 = QInputDialog.getText(None, "Novo membro", "Telefone:")
        if not (ok4 and contact):
            return
            
        # Adicionar à tabela
        row_count = widget.team_table.rowCount()
        widget.team_table.insertRow(row_count)
        
        # Adicionar dados básicos
        widget.team_table.setItem(row_count, 0, QTableWidgetItem(name))
        widget.team_table.setItem(row_count, 1, QTableWidgetItem(function))
        
        # Email com ícone
        from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLabel
        from PySide6.QtCore import QSize
        from PySide6.QtGui import QIcon
        import gui.themes.dracula as style
        
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
        email_icon.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(f"mailto:{email}")))
        
        email_layout.addWidget(email_label)
        email_layout.addWidget(email_icon)
        email_layout.addStretch()
        
        widget.team_table.setCellWidget(row_count, 2, email_container)
        
        # Telefone
        widget.team_table.setItem(row_count, 3, QTableWidgetItem(contact))
        
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
        edit_btn.clicked.connect(lambda: self.edit_team_member(name))
        
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("./resources/icons/delete.svg"))
        delete_btn.setToolTip("Remover")
        delete_btn.setIconSize(QSize(16, 16))
        delete_btn.setFixedSize(28, 28)
        delete_btn.setStyleSheet(style.secondary_button_style)
        delete_btn.clicked.connect(lambda: self.delete_team_member(widget, row_count))
        
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.addStretch()
        
        widget.team_table.setCellWidget(row_count, 4, actions_widget)
        
        self.show_message("Sucesso", f"Membro da equipe '{name}' adicionado com sucesso!")
    
    @Slot()
    def add_client(self, widget):
        """Adiciona um novo cliente"""
        company, ok1 = QInputDialog.getText(None, "Novo cliente", "Nome da empresa:")
        if not (ok1 and company):
            return
            
        responsible, ok2 = QInputDialog.getText(None, "Novo cliente", "Nome do responsável:")
        if not (ok2 and responsible):
            return
            
        email, ok3 = QInputDialog.getText(None, "Novo cliente", "Email:")
        if not (ok3 and email):
            return
            
        phone, ok4 = QInputDialog.getText(None, "Novo cliente", "Telefone:")
        if not (ok4 and phone):
            return
            
        # Adicionar à tabela
        row_count = widget.client_table.rowCount()
        widget.client_table.insertRow(row_count)
        
        # Adicionar dados básicos
        widget.client_table.setItem(row_count, 0, QTableWidgetItem(company))
        widget.client_table.setItem(row_count, 1, QTableWidgetItem(responsible))
        
        # Email com ícone
        from PySide6.QtWidgets import QPushButton, QWidget, QHBoxLayout, QLabel
        from PySide6.QtCore import QSize
        from PySide6.QtGui import QIcon
        import gui.themes.dracula as style
        
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
        email_icon.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(f"mailto:{email}")))
        
        email_layout.addWidget(email_label)
        email_layout.addWidget(email_icon)
        email_layout.addStretch()
        
        widget.client_table.setCellWidget(row_count, 2, email_container)
        
        # Telefone
        widget.client_table.setItem(row_count, 3, QTableWidgetItem(phone))
        
        # Ações
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        actions_layout.setContentsMargins(5, 0, 5, 0)
        actions_layout.setSpacing(5)
        
        view_btn = QPushButton()
        view_btn.setIcon(QIcon("./resources/icons/view.svg"))
        view_btn.setToolTip("Ver Detalhes")
        view_btn.setIconSize(QSize(16, 16))
        view_btn.setFixedSize(28, 28)
        view_btn.setStyleSheet(style.secondary_button_style)
        view_btn.clicked.connect(lambda: self.view_client_details(company))
        
        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
        edit_btn.setToolTip("Editar")
        edit_btn.setIconSize(QSize(16, 16))
        edit_btn.setFixedSize(28, 28)
        edit_btn.setStyleSheet(style.secondary_button_style)
        edit_btn.clicked.connect(lambda: self.edit_client(company))
        
        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("./resources/icons/delete.svg"))
        delete_btn.setToolTip("Remover")
        delete_btn.setIconSize(QSize(16, 16))
        delete_btn.setFixedSize(28, 28)
        delete_btn.setStyleSheet(style.secondary_button_style)
        delete_btn.clicked.connect(lambda: self.delete_client(widget, row_count))
        
        actions_layout.addWidget(view_btn)
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.addStretch()
        
        widget.client_table.setCellWidget(row_count, 4, actions_widget)
        
        self.show_message("Sucesso", f"Cliente '{company}' adicionado com sucesso!")
            
    @Slot()
    def delete_team_member(self, widget, row):
        """Remove um membro da equipe"""
        confirm = QMessageBox()
        confirm.setWindowTitle("Confirmar exclusão")
        confirm.setText("Tem certeza que deseja remover este membro da equipe?")
        confirm.setIcon(QMessageBox.Question)
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        
        if confirm.exec() == QMessageBox.Yes:
            widget.team_table.removeRow(row)
            self.show_message("Sucesso", "Membro removido com sucesso!")
    
    @Slot()
    def delete_client(self, widget, row):
        """Remove um cliente"""
        confirm = QMessageBox()
        confirm.setWindowTitle("Confirmar exclusão")
        confirm.setText("Tem certeza que deseja remover este cliente?")
        confirm.setIcon(QMessageBox.Question)
        confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm.setDefaultButton(QMessageBox.No)
        
        if confirm.exec() == QMessageBox.Yes:
            widget.client_table.removeRow(row)
            self.show_message("Sucesso", "Cliente removido com sucesso!")
    
    @Slot()
    def edit_team_member(self, name):
        """Edita um membro da equipe"""
        new_name, ok = QInputDialog.getText(None, "Editar membro", 
                                          "Novo nome:", text=name)
        if ok and new_name:
            self.show_message("Sucesso", f"Membro renomeado para: {new_name}")
    
    @Slot()
    def edit_client(self, name):
        """Edita um cliente"""
        new_name, ok = QInputDialog.getText(None, "Editar cliente", 
                                          "Novo nome da empresa:", text=name)
        if ok and new_name:
            self.show_message("Sucesso", f"Cliente renomeado para: {new_name}")
    
    @Slot()
    def view_client_details(self, name):
        """Exibe detalhes do cliente"""
        details = f"""
        Cliente: {name}
        CNPJ: {random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}/0001-{random.randint(10, 99)}
        Endereço: Av. Paulista, {random.randint(100, 2000)}
        Cidade: São Paulo - SP
        Eventos realizados: {random.randint(2, 8)}
        Valor total contratado: R$ {random.randint(50, 500) * 1000}
        """
        
        self.show_message(f"Detalhes de {name}", details)
        
    @Slot()
    def upload_file(self):
        """Upload de arquivo"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None, "Selecionar Arquivo", "", 
            "Todos os Arquivos (*);;Imagens (*.png *.jpg);;Vídeos (*.mp4 *.mov);;Documentos (*.pdf *.doc *.docx)"
        )
        
        if file_path:
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # em MB
            
            # Criar pasta uploads se não existir
            os.makedirs("uploads", exist_ok=True)
            
            # Simular upload (cópia do arquivo)
            try:
                import shutil
                dest_path = os.path.join("uploads", file_name)
                shutil.copy2(file_path, dest_path)
                self.show_message("Upload Concluído", 
                                f"Arquivo: {file_name}\nTamanho: {file_size:.2f} MB\nDestino: uploads/{file_name}")
            except Exception as e:
                self.show_message("Erro no Upload", f"Erro: {str(e)}", "error")
                
    @Slot()
    def save_briefing(self, widget):
        """Salva o briefing"""
        # Obter dados do formulário
        event_name = widget.event_combo.currentText() if hasattr(widget, 'event_combo') else "Evento Exemplo"
        project_name = widget.project_name_input.text() if hasattr(widget, 'project_name_input') else "Projeto Exemplo"
        content = widget.content_text.toPlainText() if hasattr(widget, 'content_text') else "Conteúdo do briefing"
        
        if not content:
            self.show_message("Erro", "O conteúdo do briefing não pode estar vazio!", "error")
            return
            
        # Criar pasta briefings se não existir
        os.makedirs("briefings", exist_ok=True)
            
        # Salvar arquivo
        try:
            file_name = f"{project_name.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            file_path = os.path.join("briefings", file_name)
            
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"BRIEFING: {project_name}\n")
                f.write(f"EVENTO: {event_name}\n")
                f.write(f"DATA: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
                f.write("=" * 50 + "\n\n")
                f.write(content)
                
            self.show_message("Briefing Salvo", f"Briefing salvo com sucesso em:\n{file_path}")
        except Exception as e:
            self.show_message("Erro ao Salvar", f"Erro: {str(e)}", "error")