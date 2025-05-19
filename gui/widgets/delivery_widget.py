from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QProgressBar
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QColor, QBrush, QFont  # Adicionado QFont aqui

import gui.themes.dracula as style

class DeliveryWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)
        
        # Cabeçalho
        self.header_layout = QHBoxLayout()
        
        # Título
        self.title_label = QLabel("Monitoramento de Entregas")
        self.title_label.setStyleSheet(f"color: {style.foreground_color}; font-size: 24px; font-weight: bold;")
        
        # Seletor de evento
        self.event_selector = QComboBox()
        self.event_selector.setStyleSheet(style.combobox_style)
        self.event_selector.setFixedWidth(250)
        self.event_selector.setFixedHeight(36)
        self.event_selector.addItems([
            "Festival de Música - 18-20 Mai 2025",
            "Lançamento de Produto - 25 Mai 2025",
            "Conferência Tech - 01 Jun 2025"
        ])
        
        # Refresh button
        self.refresh_button = QPushButton()
        self.refresh_button.setIcon(QIcon("./resources/icons/refresh.svg"))
        self.refresh_button.setIconSize(QSize(16, 16))
        self.refresh_button.setFixedSize(36, 36)
        self.refresh_button.setStyleSheet(style.secondary_button_style)
        
        # Adicionar ao layout do cabeçalho
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(QLabel("Evento:"))
        self.header_layout.addWidget(self.event_selector)
        self.header_layout.addWidget(self.refresh_button)
        
        # Estatísticas
        self.stats_layout = QHBoxLayout()
        self.stats_layout.setSpacing(15)
        
        # Total de entregas
        self.total_frame = QFrame()
        self.total_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
            }}
        """)
        self.total_layout = QVBoxLayout(self.total_frame)
        
        self.total_title = QLabel("Total de Entregas")
        self.total_title.setStyleSheet(f"color: {style.comment_color}; font-size: 14px;")
        
        self.total_value = QLabel("24")
        self.total_value.setStyleSheet(f"color: {style.foreground_color}; font-size: 30px; font-weight: bold;")
        self.total_value.setAlignment(Qt.AlignCenter)
        
        self.total_layout.addWidget(self.total_title)
        self.total_layout.addWidget(self.total_value)
        
        # Concluídas
        self.completed_frame = QFrame()
        self.completed_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
            }}
        """)
        self.completed_layout = QVBoxLayout(self.completed_frame)
        
        self.completed_title = QLabel("Concluídas")
        self.completed_title.setStyleSheet(f"color: {style.comment_color}; font-size: 14px;")
        
        self.completed_value = QLabel("16")
        self.completed_value.setStyleSheet(f"color: {style.green_color}; font-size: 30px; font-weight: bold;")
        self.completed_value.setAlignment(Qt.AlignCenter)
        
        self.completed_layout.addWidget(self.completed_title)
        self.completed_layout.addWidget(self.completed_value)
        
        # Em andamento
        self.progress_frame = QFrame()
        self.progress_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
            }}
        """)
        self.progress_layout = QVBoxLayout(self.progress_frame)
        
        self.progress_title = QLabel("Em Andamento")
        self.progress_title.setStyleSheet(f"color: {style.comment_color}; font-size: 14px;")
        
        self.progress_value = QLabel("6")
        self.progress_value.setStyleSheet(f"color: {style.orange_color}; font-size: 30px; font-weight: bold;")
        self.progress_value.setAlignment(Qt.AlignCenter)
        
        self.progress_layout.addWidget(self.progress_title)
        self.progress_layout.addWidget(self.progress_value)
        
        # Atrasadas
        self.late_frame = QFrame()
        self.late_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
            }}
        """)
        self.late_layout = QVBoxLayout(self.late_frame)
        
        self.late_title = QLabel("Atrasadas")
        self.late_title.setStyleSheet(f"color: {style.comment_color}; font-size: 14px;")
        
        self.late_value = QLabel("2")
        self.late_value.setStyleSheet(f"color: {style.red_color}; font-size: 30px; font-weight: bold;")
        self.late_value.setAlignment(Qt.AlignCenter)
        
        self.late_layout.addWidget(self.late_title)
        self.late_layout.addWidget(self.late_value)
        
        # Adicionar frames ao layout de estatísticas
        self.stats_layout.addWidget(self.total_frame, 1)
        self.stats_layout.addWidget(self.completed_frame, 1)
        self.stats_layout.addWidget(self.progress_frame, 1)
        self.stats_layout.addWidget(self.late_frame, 1)
        
        # Filtros
        self.filter_layout = QHBoxLayout()
        
        # Filtro por tipo
        self.type_filter = QComboBox()
        self.type_filter.setStyleSheet(style.combobox_style)
        self.type_filter.setFixedHeight(36)
        self.type_filter.addItems(["Todos os Tipos", "Real Time", "Pós-Evento"])
        
        # Filtro por status
        self.status_filter = QComboBox()
        self.status_filter.setStyleSheet(style.combobox_style)
        self.status_filter.setFixedHeight(36)
        self.status_filter.addItems([
            "Todos os Status",
            "Pendente",
            "Em andamento",
            "Entregue para revisão",
            "Em revisão",
            "Aprovada",
            "Em alteração",
            "Concluída"
        ])
        
        # Filtro por responsável
        self.responsible_filter = QComboBox()
        self.responsible_filter.setStyleSheet(style.combobox_style)
        self.responsible_filter.setFixedHeight(36)
        self.responsible_filter.addItems(["Todos os Responsáveis", "Maria Souza", "Pedro Alves"])
        
        # Adicionar filtros
        self.filter_layout.addWidget(QLabel("Tipo:"))
        self.filter_layout.addWidget(self.type_filter)
        self.filter_layout.addSpacing(10)
        self.filter_layout.addWidget(QLabel("Status:"))
        self.filter_layout.addWidget(self.status_filter)
        self.filter_layout.addSpacing(10)
        self.filter_layout.addWidget(QLabel("Responsável:"))
        self.filter_layout.addWidget(self.responsible_filter)
        self.filter_layout.addStretch()
        
        # Tabela de entregas
        self.deliveries_table = QTableWidget()
        self.deliveries_table.setColumnCount(6)
        self.deliveries_table.setHorizontalHeaderLabels(["Entrega", "Prazo", "Responsável", "Status", "Progresso", "Ações"])
        self.deliveries_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.deliveries_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.deliveries_table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.deliveries_table.setStyleSheet(style.table_style)
        
        # Adicionar algumas entregas de exemplo
        self.add_sample_deliveries()
        
        # Progresso geral
        self.overall_layout = QHBoxLayout()
        
        self.overall_label = QLabel("Progresso geral:")
        self.overall_label.setStyleSheet(f"color: {style.foreground_color}; font-size: 14px;")
        
        self.overall_bar = QProgressBar()
        self.overall_bar.setValue(66)  # 16/24 = 66.6%
        self.overall_bar.setFixedHeight(20)
        self.overall_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {style.current_line_color};
                border-radius: 10px;
                text-align: center;
                color: {style.background_color};
                font-weight: bold;
            }}
            QProgressBar::chunk {{
                background-color: {style.purple_color};
                border-radius: 10px;
            }}
        """)
        
        self.overall_percentage = QLabel("66%")
        self.overall_percentage.setStyleSheet(f"color: {style.purple_color}; font-size: 14px; font-weight: bold;")
        
        self.overall_layout.addWidget(self.overall_label)
        self.overall_layout.addWidget(self.overall_bar)
        self.overall_layout.addWidget(self.overall_percentage)
        
        # Adicionar todos os layouts ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addLayout(self.stats_layout)
        self.layout.addLayout(self.filter_layout)
        self.layout.addWidget(self.deliveries_table)
        self.layout.addLayout(self.overall_layout)
    
    def add_sample_deliveries(self):
        # Status colors
        status_colors = {
            "Pendente": style.comment_color,
            "Em andamento": style.orange_color,
            "Entregue para revisão": style.cyan_color,
            "Em revisão": style.purple_color,
            "Aprovada": style.green_color,
            "Em alteração": style.pink_color,
            "Concluída": style.green_color,
            "Atrasada": style.red_color
        }
        
        # Dados de exemplo
        deliveries = [
            ["Abertura do evento", "Hoje, 18:30", "Maria Souza", "Em andamento", 60],
            ["Entrevista com artista principal", "Hoje, 19:45", "Pedro Alves", "Entregue para revisão", 90],
            ["Patrocinador A - Ativação", "Hoje, 20:00", "Maria Souza", "Atrasada", 30],
            ["Teaser final", "Hoje, 22:30", "Pedro Alves", "Pendente", 0],
            ["Aftermovie", "25 Mai, 18:00", "Maria Souza", "Pendente", 10],
            ["Melhores momentos", "26 Mai, 12:00", "Pedro Alves", "Pendente", 0]
        ]
        
        self.deliveries_table.setRowCount(len(deliveries))
        
        for row, delivery in enumerate(deliveries):
            # Nome da entrega
            self.deliveries_table.setItem(row, 0, QTableWidgetItem(delivery[0]))
            
            # Prazo
            self.deliveries_table.setItem(row, 1, QTableWidgetItem(delivery[1]))
            
            # Responsável
            self.deliveries_table.setItem(row, 2, QTableWidgetItem(delivery[2]))
            
            # Status
            status_item = QTableWidgetItem(delivery[3])
            status_color = status_colors.get(delivery[3], style.comment_color)
            status_item.setForeground(QBrush(QColor(status_color)))
            status_item.setFont(QFont("Arial", 9, QFont.Bold))
            self.deliveries_table.setItem(row, 3, status_item)
            
            # Progresso
            progress_bar = QProgressBar()
            progress_bar.setValue(delivery[4])
            progress_bar.setFixedHeight(15)
            progress_color = style.purple_color
            if delivery[4] >= 100:
                progress_color = style.green_color
            elif delivery[3] == "Atrasada":
                progress_color = style.red_color
                
            progress_bar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {style.current_line_color};
                    border-radius: 6px;
                    text-align: center;
                    color: transparent;
                }}
                QProgressBar::chunk {{
                    background-color: {progress_color};
                    border-radius: 6px;
                }}
            """)
            
            self.deliveries_table.setCellWidget(row, 4, progress_bar)
            
            # Ações
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(5, 0, 5, 0)
            actions_layout.setSpacing(5)
            
            view_btn = QPushButton()
            view_btn.setIcon(QIcon("./resources/icons/view.svg"))
            view_btn.setIconSize(QSize(16, 16))
            view_btn.setFixedSize(28, 28)
            view_btn.setStyleSheet(style.secondary_button_style)
            
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon("./resources/icons/edit.svg"))
            edit_btn.setIconSize(QSize(16, 16))
            edit_btn.setFixedSize(28, 28)
            edit_btn.setStyleSheet(style.secondary_button_style)
            
            actions_layout.addWidget(view_btn)
            actions_layout.addWidget(edit_btn)
            
            actions_widget = QWidget()
            actions_widget.setLayout(actions_layout)
            self.deliveries_table.setCellWidget(row, 5, actions_widget)