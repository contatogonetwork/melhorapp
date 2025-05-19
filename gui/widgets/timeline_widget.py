from PySide6.QtCore import QPoint, QRectF, QSize, Qt
from PySide6.QtGui import QBrush, QColor, QFont, QIcon, QPainter, QPen
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QGraphicsRectItem,
    QGraphicsScene,
    QGraphicsTextItem,
    QGraphicsView,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class TimelineWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Cabeçalho
        self.header_layout = QHBoxLayout()

        # Título
        self.title_label = QLabel("Timeline")
        self.title_label.setStyleSheet(
            f"color: {style.foreground_color}; font-size: 24px; font-weight: bold;"
        )

        # Seletor de evento
        self.event_selector = QComboBox()
        self.event_selector.setStyleSheet(style.combobox_style)
        self.event_selector.setFixedWidth(250)
        self.event_selector.setFixedHeight(36)
        self.event_selector.addItems(
            [
                "Festival de Música - 18-20 Mai 2025",
                "Lançamento de Produto - 25 Mai 2025",
                "Conferência Tech - 01 Jun 2025",
            ]
        )

        # Botões de ação
        self.refresh_button = QPushButton("Atualizar")
        self.refresh_button.setIcon(QIcon("./resources/icons/refresh.svg"))
        self.refresh_button.setStyleSheet(style.secondary_button_style)
        self.refresh_button.setFixedHeight(36)

        self.export_button = QPushButton("Exportar")
        self.export_button.setIcon(QIcon("./resources/icons/export.svg"))
        self.export_button.setStyleSheet(style.secondary_button_style)
        self.export_button.setFixedHeight(36)

        # Adicionar ao layout do cabeçalho
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(QLabel("Evento:"))
        self.header_layout.addWidget(self.event_selector)
        self.header_layout.addWidget(self.refresh_button)
        self.header_layout.addWidget(self.export_button)

        # Filtros
        self.filter_layout = QHBoxLayout()

        # Filtro por membro da equipe
        self.member_filter = QComboBox()
        self.member_filter.setStyleSheet(style.combobox_style)
        self.member_filter.setFixedHeight(36)
        self.member_filter.setFixedWidth(200)
        self.member_filter.addItems(
            [
                "Todos os Membros",
                "João Silva",
                "Maria Souza",
                "Carlos Lima",
                "Ana Costa",
            ]
        )

        # Filtro por tipo de atividade
        self.activity_filter = QComboBox()
        self.activity_filter.setStyleSheet(style.combobox_style)
        self.activity_filter.setFixedHeight(36)
        self.activity_filter.setFixedWidth(200)
        self.activity_filter.addItems(
            [
                "Todas as Atividades",
                "Captação",
                "Edição",
                "Entrega",
                "Aprovação",
            ]
        )

        # Filtro por status
        self.status_filter = QComboBox()
        self.status_filter.setStyleSheet(style.combobox_style)
        self.status_filter.setFixedHeight(36)
        self.status_filter.setFixedWidth(200)
        self.status_filter.addItems(
            [
                "Todos os Status",
                "Pendente",
                "Em andamento",
                "Concluído",
                "Atrasado",
            ]
        )

        # Adicionar filtros
        self.filter_layout.addWidget(QLabel("Membro:"))
        self.filter_layout.addWidget(self.member_filter)
        self.filter_layout.addWidget(QLabel("Atividade:"))
        self.filter_layout.addWidget(self.activity_filter)
        self.filter_layout.addWidget(QLabel("Status:"))
        self.filter_layout.addWidget(self.status_filter)
        self.filter_layout.addStretch()

        # View da timeline
        self.timeline_view = TimelineView()

        # Adicionar todos os layouts ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addLayout(self.filter_layout)
        self.layout.addWidget(self.timeline_view)


class TimelineView(QGraphicsView):
    def __init__(self):
        super().__init__()

        # Configuração da view
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(QBrush(QColor(style.background_color)))
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setViewportUpdateMode(
            QGraphicsView.ViewportUpdateMode.FullViewportUpdate
        )
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        # Criar a cena
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Configurar cena
        self.scene.setBackgroundBrush(QBrush(QColor(style.background_color)))

        # Gerar timeline de exemplo
        self.generate_example_timeline()

    def generate_example_timeline(self):
        # Limpar cena anterior
        self.scene.clear()

        # Definir dimensões da timeline
        timeline_width = 2000  # Largura total (scrollable)
        timeline_height = 600  # Altura visível

        # Configurar dimensões da cena
        self.scene.setSceneRect(0, 0, timeline_width, timeline_height)

        # Desenhar grid de horas (linhas verticais)
        hours = 12  # 12 horas na timeline
        hour_width = timeline_width / hours

        # Desenhar linhas horizontais (separadores de membros da equipe)
        team_members = [
            "João (Cinegrafia)",
            "Maria (Edição)",
            "Carlos (Drone)",
            "Ana (Coordenação)",
        ]
        row_height = timeline_height / (
            len(team_members) + 1
        )  # +1 para cabeçalho

        # Desenhar cabeçalho com horas
        header_rect = QGraphicsRectItem(0, 0, timeline_width, row_height)
        header_rect.setBrush(QBrush(QColor(style.current_line_color)))
        header_rect.setPen(QPen(QColor(style.comment_color)))
        self.scene.addItem(header_rect)

        # Adicionar horas ao cabeçalho
        for i in range(hours + 1):
            hour = 10 + i  # Começando às 10h
            hour_str = f"{hour}:00" if hour < 24 else f"{hour-24}:00"

            # Texto da hora
            hour_text = QGraphicsTextItem(hour_str)
            hour_text.setFont(QFont("Arial", 10))
            hour_text.setDefaultTextColor(QColor(style.foreground_color))
            hour_text.setPos(i * hour_width - 15, 10)
            self.scene.addItem(hour_text)

            # Linha vertical da hora
            if i > 0:
                hour_line = QGraphicsRectItem(
                    i * hour_width, 0, 1, timeline_height
                )
                hour_line.setBrush(QBrush(QColor(style.comment_color)))
                hour_line.setPen(QPen(QColor(style.comment_color)))
                self.scene.addItem(hour_line)

        # Adicionar membros da equipe e suas linhas
        for i, member in enumerate(team_members):
            # Posição vertical
            y_pos = (i + 1) * row_height

            # Linha horizontal (separador)
            line = QGraphicsRectItem(0, y_pos, timeline_width, 1)
            line.setBrush(QBrush(QColor(style.comment_color)))
            line.setPen(QPen(QColor(style.comment_color)))
            self.scene.addItem(line)

            # Nome do membro
            member_text = QGraphicsTextItem(member)
            member_text.setFont(QFont("Arial", 10))
            member_text.setDefaultTextColor(QColor(style.foreground_color))
            member_text.setPos(10, y_pos + 10)
            self.scene.addItem(member_text)

            # Adicionar tarefas para este membro
            self.add_tasks_for_member(i, y_pos, row_height, hour_width)

    def add_tasks_for_member(
        self, member_index, y_pos, row_height, hour_width
    ):
        # Cores para diferentes tipos de tarefas
        task_colors = {
            "captação": QColor(style.purple_color),
            "edição": QColor(style.orange_color),
            "entrega": QColor(style.green_color),
            "aprovação": QColor(style.cyan_color),
            "concluído": QColor(style.comment_color),
            "atrasado": QColor(style.red_color),
        }

        # Exemplo de tarefas para cada membro
        if member_index == 0:  # João (Cinegrafia)
            # Tarefa 1: Captação de palco
            self.add_task(
                1.5,
                2.0,
                y_pos,
                row_height,
                hour_width,
                "Captação - Palco Principal",
                task_colors["captação"],
            )

            # Tarefa 2: Captação de patrocinador
            self.add_task(
                4.0,
                1.0,
                y_pos,
                row_height,
                hour_width,
                "Patrocinador A - Stand",
                task_colors["captação"],
            )

            # Tarefa 3: Captação concluída
            self.add_task(
                7.5,
                1.5,
                y_pos,
                row_height,
                hour_width,
                "Captação - Backstage",
                task_colors["concluído"],
            )

        elif member_index == 1:  # Maria (Edição)
            # Tarefa 1: Edição em andamento
            self.add_task(
                2.0,
                1.5,
                y_pos,
                row_height,
                hour_width,
                "Edição - Abertura",
                task_colors["edição"],
            )

            # Tarefa 2: Entrega concluída
            self.add_task(
                5.0,
                0.5,
                y_pos,
                row_height,
                hour_width,
                "Entrega - Reels Patrocinador",
                task_colors["concluído"],
            )

            # Tarefa 3: Edição futura
            self.add_task(
                8.0,
                2.0,
                y_pos,
                row_height,
                hour_width,
                "Edição - Teaser Final",
                task_colors["edição"],
            )

        elif member_index == 2:  # Carlos (Drone)
            # Tarefa 1: Captação drone
            self.add_task(
                3.0,
                1.0,
                y_pos,
                row_height,
                hour_width,
                "Captação Drone - Área Externa",
                task_colors["captação"],
            )

            # Tarefa 2: Captação atrasada
            self.add_task(
                6.0,
                0.5,
                y_pos,
                row_height,
                hour_width,
                "Captação Drone - Vista Geral",
                task_colors["atrasado"],
            )

        elif member_index == 3:  # Ana (Coordenação)
            # Tarefa 1: Aprovação
            self.add_task(
                2.5,
                0.5,
                y_pos,
                row_height,
                hour_width,
                "Aprovação - Material Inicial",
                task_colors["aprovação"],
            )

            # Tarefa 2: Entrega
            self.add_task(
                4.5,
                0.5,
                y_pos,
                row_height,
                hour_width,
                "Entrega - Stories",
                task_colors["entrega"],
            )

            # Tarefa 3: Aprovação futura
            self.add_task(
                9.0,
                1.0,
                y_pos,
                row_height,
                hour_width,
                "Aprovação - Teaser",
                task_colors["aprovação"],
            )

    def add_task(
        self, start_hour, duration, y_pos, row_height, hour_width, title, color
    ):
        # Calcular posições
        x = start_hour * hour_width
        width = duration * hour_width
        height = row_height * 0.7
        y = y_pos + (row_height - height) / 2

        # Criar retângulo da tarefa
        task_rect = QGraphicsRectItem(x, y, width, height)
        task_rect.setBrush(QBrush(color))
        task_rect.setPen(QPen(QColor(style.background_color), 1))
        task_rect.setZValue(1)  # Sobrepor às linhas de grade

        # Adicionar texto
        task_text = QGraphicsTextItem(title)
        task_text.setFont(QFont("Arial", 8))
        task_text.setDefaultTextColor(QColor(style.background_color))

        # Centralizar texto (aproximadamente)
        text_width = task_text.boundingRect().width()
        text_height = task_text.boundingRect().height()
        text_x = x + (width - text_width) / 2
        text_y = y + (height - text_height) / 2

        task_text.setPos(text_x, text_y)
        task_text.setZValue(2)  # Sobrepor ao retângulo

        # Adicionar à cena
        self.scene.addItem(task_rect)
        self.scene.addItem(task_text)
