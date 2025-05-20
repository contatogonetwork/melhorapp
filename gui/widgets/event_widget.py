from PySide6.QtCore import QDate, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class EventWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Cabeçalho
        self.header_layout = QHBoxLayout()

        # Título
        self.title_label = QLabel("Gerenciamento de Eventos")
        self.title_label.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 24px; font-weight: bold;"
        )

        # Botão Novo Evento
        self.new_event_button = QPushButton("Novo Evento")
        self.new_event_button.setIcon(QIcon("./resources/icons/add-event.svg"))
        self.new_event_button.setStyleSheet(style.button_style)
        self.new_event_button.setFixedHeight(36)
        self.new_event_button.clicked.connect(self.criar_novo_evento)

        # Adicionar ao layout do cabeçalho
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.new_event_button)

        # Filtros
        self.filter_layout = QHBoxLayout()
        self.filter_layout.setSpacing(10)

        # Filtro por data
        self.date_filter = QDateEdit()
        self.date_filter.setCalendarPopup(True)
        self.date_filter.setFixedWidth(150)
        self.date_filter.setFixedHeight(36)
        self.date_filter.setStyleSheet(style.input_style)
        self.date_filter.setDate(QDate.currentDate())

        # Filtro por tipo
        self.type_filter = QComboBox()
        self.type_filter.setFixedWidth(180)
        self.type_filter.setFixedHeight(36)
        self.type_filter.setStyleSheet(style.combobox_style)
        self.type_filter.addItems(
            [
                "Todos os Tipos",
                "Corporativo",
                "Festival",
                "Conferência",
                "Lançamento",
                "Outro",
            ]
        )

        # Filtro por status
        self.status_filter = QComboBox()
        self.status_filter.setFixedWidth(180)
        self.status_filter.setFixedHeight(36)
        self.status_filter.setStyleSheet(style.combobox_style)
        self.status_filter.addItems(
            [
                "Todos os Status",
                "Em planejamento",
                "Confirmado",
                "Em andamento",
                "Concluído",
                "Cancelado",
            ]
        )

        # Campo de busca
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar eventos...")
        self.search_input.setStyleSheet(style.input_style)
        self.search_input.setFixedHeight(36)

        # Botão de busca
        self.search_button = QPushButton()
        self.search_button.setIcon(QIcon("./resources/icons/search.svg"))
        self.search_button.setFixedSize(36, 36)
        self.search_button.setStyleSheet(style.secondary_button_style)

        # Adicionar filtros ao layout
        self.filter_layout.addWidget(QLabel("Data:"))
        self.filter_layout.addWidget(self.date_filter)
        self.filter_layout.addWidget(QLabel("Tipo:"))
        self.filter_layout.addWidget(self.type_filter)
        self.filter_layout.addWidget(QLabel("Status:"))
        self.filter_layout.addWidget(self.status_filter)
        self.filter_layout.addStretch()
        self.filter_layout.addWidget(self.search_input)
        self.filter_layout.addWidget(self.search_button)

        # Tabela de eventos
        self.events_table = QTableWidget()
        self.events_table.setColumnCount(6)
        self.events_table.setHorizontalHeaderLabels(
            ["Nome do Evento", "Data", "Local", "Cliente", "Status", "Ações"]
        )
        self.events_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.events_table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.ResizeToContents
        )
        self.events_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.ResizeToContents
        )
        self.events_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        self.events_table.horizontalHeader().setSectionResizeMode(
            4, QHeaderView.ResizeMode.ResizeToContents
        )
        self.events_table.horizontalHeader().setSectionResizeMode(
            5, QHeaderView.ResizeMode.ResizeToContents
        )
        self.events_table.setStyleSheet(style.table_style)

        # Adicionar dados de exemplo
        self.add_sample_events()

        # Novo evento frame
        self.add_event_frame = QFrame()
        self.add_event_frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border: 1px solid {style.current_line_color};
                border-radius: 5px;
            }}
        """
        )

        self.add_event_layout = QVBoxLayout(self.add_event_frame)
        self.add_event_layout.setContentsMargins(20, 20, 20, 20)
        self.add_event_layout.setSpacing(15)

        # Título do frame
        self.add_event_title = QLabel("Criar Novo Evento")
        self.add_event_title.setStyleSheet(
            f"color: {style.purple_color}; font-size: 18px; font-weight: bold;"
        )
        self.add_event_layout.addWidget(self.add_event_title)

        # Form layout para campos
        self.form_layout = QHBoxLayout()
        self.form_layout.setSpacing(20)

        # Coluna esquerda
        self.left_form = QVBoxLayout()
        self.left_form.setSpacing(15)

        # Nome do evento
        self.left_form.addWidget(QLabel("Nome do Evento"))
        self.event_name_input = QLineEdit()
        self.event_name_input.setPlaceholderText("Digite o nome do evento")
        self.event_name_input.setStyleSheet(style.input_style)
        self.event_name_input.setFixedHeight(36)
        self.left_form.addWidget(self.event_name_input)

        # Data do evento
        self.left_form.addWidget(QLabel("Data do Evento"))
        self.event_date_input = QDateEdit()
        self.event_date_input.setCalendarPopup(True)
        self.event_date_input.setStyleSheet(style.input_style)
        self.event_date_input.setFixedHeight(36)
        self.event_date_input.setDate(QDate.currentDate().addDays(30))
        self.left_form.addWidget(self.event_date_input)

        # Local do evento
        self.left_form.addWidget(QLabel("Local"))
        self.event_location_input = QLineEdit()
        self.event_location_input.setPlaceholderText("Digite o local do evento")
        self.event_location_input.setStyleSheet(style.input_style)
        self.event_location_input.setFixedHeight(36)
        self.left_form.addWidget(self.event_location_input)

        self.left_form.addStretch()

        # Coluna direita
        self.right_form = QVBoxLayout()
        self.right_form.setSpacing(15)

        # Cliente
        self.right_form.addWidget(QLabel("Cliente"))
        self.event_client_input = QComboBox()
        self.event_client_input.setStyleSheet(style.combobox_style)
        self.event_client_input.setFixedHeight(36)
        self.event_client_input.addItems(
            [
                "Selecione um cliente",
                "Empresa ABC",
                "XYZ Corp",
                "Tech Solutions",
                "Novo Cliente...",
            ]
        )
        self.right_form.addWidget(self.event_client_input)

        # Tipo
        self.right_form.addWidget(QLabel("Tipo de Evento"))
        self.event_type_input = QComboBox()
        self.event_type_input.setStyleSheet(style.combobox_style)
        self.event_type_input.setFixedHeight(36)
        self.event_type_input.addItems(
            ["Corporativo", "Festival", "Conferência", "Lançamento", "Outro"]
        )
        self.right_form.addWidget(self.event_type_input)

        # Status
        self.right_form.addWidget(QLabel("Status"))
        self.event_status_input = QComboBox()
        self.event_status_input.setStyleSheet(style.combobox_style)
        self.event_status_input.setFixedHeight(36)
        self.event_status_input.addItems(
            [
                "Em planejamento",
                "Confirmado",
                "Em andamento",
                "Concluído",
                "Cancelado",
            ]
        )
        self.right_form.addWidget(self.event_status_input)

        self.right_form.addStretch()

        # Adicionar colunas ao form layout
        self.form_layout.addLayout(self.left_form, 1)
        self.form_layout.addLayout(self.right_form, 1)
        self.add_event_layout.addLayout(self.form_layout)

        # Botões de ação
        self.actions_layout = QHBoxLayout()
        self.actions_layout.setSpacing(10)
        self.actions_layout.addStretch()

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.setStyleSheet(style.secondary_button_style)
        self.cancel_button.setFixedHeight(36)

        self.create_button = QPushButton("Criar Evento")
        self.create_button.setIcon(QIcon("./resources/icons/save.svg"))
        self.create_button.setStyleSheet(style.button_style)
        self.create_button.setFixedHeight(36)
        self.create_button.clicked.connect(self.criar_novo_evento)

        self.actions_layout.addWidget(self.cancel_button)
        self.actions_layout.addWidget(self.create_button)

        self.add_event_layout.addLayout(self.actions_layout)

        # Adicionar layouts e widgets ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addLayout(self.filter_layout)
        self.layout.addWidget(self.events_table)
        self.layout.addWidget(self.add_event_frame)

    def add_sample_events(self):
        # Dados de exemplo
        events = [
            [
                "Festival de Música",
                "18-20 Mai 2025",
                "Arena São Paulo",
                "Empresa ABC",
                "Em planejamento",
            ],
            [
                "Lançamento de Produto",
                "25 Mai 2025",
                "Centro de Convenções",
                "XYZ Corp",
                "Confirmado",
            ],
            [
                "Conferência Tech",
                "01 Jun 2025",
                "Hotel Grand",
                "Tech Solutions",
                "Em planejamento",
            ],
            [
                "Treinamento Corporativo",
                "15 Jun 2025",
                "Sede da Empresa",
                "Consultoria DEF",
                "Confirmado",
            ],
            [
                "Premiação Anual",
                "30 Jun 2025",
                "Teatro Municipal",
                "Associação GHI",
                "Em planejamento",
            ],
        ]

        status_colors = {
            "Em planejamento": style.cyan_color,
            "Confirmado": style.purple_color,
            "Em andamento": style.orange_color,
            "Concluído": style.green_color,
            "Cancelado": style.red_color,
        }

        self.events_table.setRowCount(len(events))

        for row, event in enumerate(events):
            # Nome do evento
            self.events_table.setItem(row, 0, QTableWidgetItem(event[0]))

            # Data
            self.events_table.setItem(row, 1, QTableWidgetItem(event[1]))

            # Local
            self.events_table.setItem(row, 2, QTableWidgetItem(event[2]))

            # Cliente
            self.events_table.setItem(row, 3, QTableWidgetItem(event[3]))

            # Status
            status_item = QTableWidgetItem(event[4])
            status_color = status_colors.get(event[4], style.comment_color)
            status_item.setForeground(QBrush(QColor(status_color)))
            self.events_table.setItem(row, 4, status_item)

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

            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
            edit_btn.setToolTip("Editar")
            edit_btn.setIconSize(QSize(16, 16))
            edit_btn.setFixedSize(28, 28)
            edit_btn.setStyleSheet(style.secondary_button_style)

            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon("./resources/icons/delete.svg"))
            delete_btn.setToolTip("Excluir")
            delete_btn.setIconSize(QSize(16, 16))
            delete_btn.setFixedSize(28, 28)
            delete_btn.setStyleSheet(style.secondary_button_style)

            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            actions_layout.addStretch()

            self.events_table.setCellWidget(row, 5, actions_widget)

    def criar_novo_evento(self):
        """Cria um novo evento com os dados do formulário"""
        nome = self.event_name_input.text()
        data = self.event_date_input.date().toString("dd/MM/yyyy")
        local = self.event_location_input.text()
        cliente = self.event_client_input.currentText()
        tipo = self.event_type_input.currentText()
        status = self.event_status_input.currentText()

        if not nome or cliente == "Selecione um cliente":
            QMessageBox.warning(self, "Erro", "Preencha todos os campos obrigatórios")
            return

        # Adicionar à tabela de eventos
        row = self.events_table.rowCount()
        self.events_table.insertRow(row)

        # Inserir os dados nas células
        self.events_table.setItem(row, 0, QTableWidgetItem(nome))
        self.events_table.setItem(row, 1, QTableWidgetItem(data))
        self.events_table.setItem(row, 2, QTableWidgetItem(local))
        self.events_table.setItem(row, 3, QTableWidgetItem(cliente))

        # Status com cor
        status_item = QTableWidgetItem(status)
        status_colors = {
            "Em planejamento": style.cyan_color,
            "Confirmado": style.purple_color,
            "Em andamento": style.orange_color,
            "Concluído": style.green_color,
            "Cancelado": style.red_color,
        }
        status_color = status_colors.get(status, style.comment_color)
        status_item.setForeground(QBrush(QColor(status_color)))
        self.events_table.setItem(row, 4, status_item)

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

        edit_btn = QPushButton()
        edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
        edit_btn.setToolTip("Editar")
        edit_btn.setIconSize(QSize(16, 16))
        edit_btn.setFixedSize(28, 28)
        edit_btn.setStyleSheet(style.secondary_button_style)

        delete_btn = QPushButton()
        delete_btn.setIcon(QIcon("./resources/icons/delete.svg"))
        delete_btn.setToolTip("Excluir")
        delete_btn.setIconSize(QSize(16, 16))
        delete_btn.setFixedSize(28, 28)
        delete_btn.setStyleSheet(style.secondary_button_style)

        actions_layout.addWidget(view_btn)
        actions_layout.addWidget(edit_btn)
        actions_layout.addWidget(delete_btn)
        actions_layout.addStretch()

        self.events_table.setCellWidget(row, 5, actions_widget)

        # Limpar campos
        self.event_name_input.clear()
        self.event_location_input.clear()
        self.event_client_input.setCurrentIndex(0)

        QMessageBox.information(self, "Sucesso", f"Evento '{nome}' criado com sucesso!")
