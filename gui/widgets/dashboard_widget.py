from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QIcon
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Cabeçalho
        self.header_layout = QHBoxLayout()

        # Título
        self.title_label = QLabel("Dashboard")
        self.title_label.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 24px; font-weight: bold;"
        )

        # Adicionar ao layout do cabeçalho
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()

        # Cards de estatísticas
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(15)

        # Eventos próximos
        self.upcoming_events_frame = self.create_stat_card(
            "Eventos Próximos", "3", style.purple_color, "calendar-active"
        )

        # Entregas de hoje
        self.today_deliveries_frame = self.create_stat_card(
            "Entregas Hoje", "5", style.green_color, "delivery-today"
        )

        # Pendentes de edição
        self.pending_edits_frame = self.create_stat_card(
            "Edições Pendentes", "8", style.orange_color, "pending-edit"
        )

        # Aprovações pendentes
        self.pending_approvals_frame = self.create_stat_card(
            "Aprovações Pendentes", "2", style.red_color, "approval"
        )

        # Adicionar cards ao layout
        self.stats_layout.addWidget(self.upcoming_events_frame, 1)
        self.stats_layout.addWidget(self.today_deliveries_frame, 1)
        self.stats_layout.addWidget(self.pending_edits_frame, 1)
        self.stats_layout.addWidget(self.pending_approvals_frame, 1)

        # Seção de eventos
        self.events_section = QFrame()
        self.events_section.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
                border: 1px solid {style.current_line_color};
            }}
        """
        )

        self.events_layout = QVBoxLayout(self.events_section)
        self.events_layout.setContentsMargins(15, 15, 15, 15)
        self.events_layout.setSpacing(10)

        # Cabeçalho de eventos
        self.events_header = QHBoxLayout()
        self.events_title = QLabel("Eventos Recentes")
        self.events_title.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 16px; font-weight: bold;"
        )

        self.view_all_events = QPushButton("Ver Todos")
        self.view_all_events.setStyleSheet(style.secondary_button_style)
        self.view_all_events.setIcon(QIcon("./resources/icons/calendar.svg"))
        self.view_all_events.setIconSize(QSize(16, 16))
        self.view_all_events.clicked.connect(self.ver_todos_eventos)

        self.events_header.addWidget(self.events_title)
        self.events_header.addStretch()
        self.events_header.addWidget(self.view_all_events)
        self.events_layout.addLayout(self.events_header)

        # Tabela de eventos
        self.events_table = QTableWidget()
        self.events_table.setColumnCount(4)
        self.events_table.setHorizontalHeaderLabels(
            ["Nome do Evento", "Data", "Status", "Ações"]
        )
        self.events_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.events_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        self.events_table.setStyleSheet(style.table_style)

        # Adicionar dados de exemplo
        self.add_sample_events()

        self.events_layout.addWidget(self.events_table)

        # Seção de tarefas
        self.tasks_section = QFrame()
        self.tasks_section.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
                border: 1px solid {style.current_line_color};
            }}
        """
        )

        self.tasks_layout = QVBoxLayout(self.tasks_section)
        self.tasks_layout.setContentsMargins(15, 15, 15, 15)
        self.tasks_layout.setSpacing(10)

        # Cabeçalho de tarefas
        self.tasks_header = QHBoxLayout()
        self.tasks_title = QLabel("Tarefas Pendentes")
        self.tasks_title.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 16px; font-weight: bold;"
        )

        self.view_all_tasks = QPushButton("Ver Todas as Tarefas")
        self.view_all_tasks.setStyleSheet(style.secondary_button_style)
        self.view_all_tasks.setIcon(QIcon("./resources/icons/document.svg"))
        self.view_all_tasks.setIconSize(QSize(16, 16))
        self.view_all_tasks.clicked.connect(self.ver_todas_tarefas)

        self.tasks_header.addWidget(self.tasks_title)
        self.tasks_header.addStretch()
        self.tasks_header.addWidget(self.view_all_tasks)
        self.tasks_layout.addLayout(self.tasks_header)

        # Tabela de tarefas
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(4)
        self.tasks_table.setHorizontalHeaderLabels(
            ["Descrição", "Projeto", "Progresso", "Ações"]
        )
        self.tasks_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self.tasks_table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        self.tasks_table.horizontalHeader().setSectionResizeMode(
            3, QHeaderView.ResizeMode.ResizeToContents
        )
        self.tasks_table.setStyleSheet(style.table_style)

        # Adicionar dados de exemplo
        self.add_sample_tasks()

        self.tasks_layout.addWidget(self.tasks_table)

        # Adicionar todos os layouts ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addLayout(self.stats_layout)
        self.layout.addWidget(self.events_section)
        self.layout.addWidget(self.tasks_section)

    def create_stat_card(self, title, value, color, icon_name):
        """Criar um card de estatística"""

        frame = QFrame()
        frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
                border: 1px solid {style.current_line_color};
            }}
        """
        )

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        header_layout = QHBoxLayout()
        icon = QLabel()
        icon.setPixmap(
            QIcon(f"./resources/icons/{icon_name}.svg").pixmap(QSize(20, 20))
        )
        icon.setStyleSheet(f"color: {color};")

        title_label = QLabel(title)
        title_label.setStyleSheet(
            f"color: {style.comment_color}; font-size: 14px;"
        )

        header_layout.addWidget(icon)
        header_layout.addWidget(title_label)
        header_layout.addStretch()

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(
            f"color: {color}; font-size: 36px; font-weight: bold;"
        )

        view_details = QPushButton("Ver Detalhes")
        view_details.setStyleSheet(
            f"""
            QPushButton {{
                color: {color};
                background-color: transparent;
                border: none;
                text-decoration: underline;
                font-size: 12px;
            }}
            QPushButton:hover {{
                color: {style.foreground_color};
            }}
        """
        )
        view_details.setCursor(Qt.PointingHandCursor)
        view_details.clicked.connect(lambda: self.ver_detalhes(title))

        layout.addLayout(header_layout)
        layout.addWidget(value_label)
        layout.addWidget(view_details, 0, Qt.AlignCenter)

        return frame

    def add_sample_events(self):
        # Dados de exemplo
        events = [
            ["Festival de Música", "18-20 Mai 2025", "Em planejamento"],
            ["Lançamento de Produto", "25 Mai 2025", "Confirmado"],
            ["Conferência Tech", "01 Jun 2025", "Em planejamento"],
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

            # Status
            status_item = QTableWidgetItem(event[2])
            status_color = status_colors.get(event[2], style.comment_color)
            status_item.setForeground(QBrush(QColor(status_color)))
            self.events_table.setItem(row, 2, status_item)

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
            view_btn.clicked.connect(
                lambda checked=False, t=event[0]: self.ver_detalhes(t)
            )

            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
            edit_btn.setToolTip("Editar")
            edit_btn.setIconSize(QSize(16, 16))
            edit_btn.setFixedSize(28, 28)
            edit_btn.setStyleSheet(style.secondary_button_style)

            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(edit_btn)
            actions_layout.addStretch()

            self.events_table.setCellWidget(row, 3, actions_widget)

    def add_sample_tasks(self):
        # Dados de exemplo
        tasks = [
            ["Revisar timeline", "Festival de Música", 70],
            ["Enviar arquivos para aprovação", "Lançamento de Produto", 30],
            ["Confirmar equipamentos", "Conferência Tech", 50],
            ["Finalizar edição do vídeo", "Festival de Música", 80],
            ["Preparar roteiro da apresentação", "Lançamento de Produto", 20],
        ]

        self.tasks_table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            # Descrição
            self.tasks_table.setItem(row, 0, QTableWidgetItem(task[0]))

            # Projeto
            self.tasks_table.setItem(row, 1, QTableWidgetItem(task[1]))

            # Progresso
            progress_bar = QProgressBar()
            progress_bar.setValue(task[2])
            progress_bar.setStyleSheet(
                f"""
                QProgressBar {{
                    background-color: {style.current_line_color};
                    color: {style.foreground_color};
                    border-radius: 5px;
                    text-align: center;
                }}
                QProgressBar::chunk {{
                    background-color: {style.purple_color};
                    border-radius: 5px;
                }}
            """
            )
            self.tasks_table.setCellWidget(row, 2, progress_bar)

            # Ações
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 0, 5, 0)
            actions_layout.setSpacing(5)

            complete_btn = QPushButton()
            complete_btn.setIcon(QIcon("./resources/icons/check.svg"))
            complete_btn.setToolTip("Marcar como Concluído")
            complete_btn.setIconSize(QSize(16, 16))
            complete_btn.setFixedSize(28, 28)
            complete_btn.setStyleSheet(style.secondary_button_style)

            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
            edit_btn.setToolTip("Editar")
            edit_btn.setIconSize(QSize(16, 16))
            edit_btn.setFixedSize(28, 28)
            edit_btn.setStyleSheet(style.secondary_button_style)

            actions_layout.addWidget(complete_btn)
            actions_layout.addWidget(edit_btn)
            actions_layout.addStretch()

            self.tasks_table.setCellWidget(row, 3, actions_widget)

    def ver_todos_eventos(self):
        """Exibe todos os eventos"""
        QMessageBox.information(
            self, "Eventos", "Exibindo lista completa de todos os eventos"
        )

    def ver_detalhes(self, titulo="Item"):
        """Exibe detalhes de um item específico"""
        QMessageBox.information(
            self, f"Detalhes - {titulo}", f"Exibindo detalhes de: {titulo}"
        )

    def ver_todas_tarefas(self):
        """Exibe todas as tarefas"""
        QMessageBox.information(
            self, "Tarefas", "Exibindo lista completa de todas as tarefas"
        )
