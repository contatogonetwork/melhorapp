from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTabWidget,
    QTextEdit,
    QTimeEdit,
    QVBoxLayout,
    QWidget,
)

import gui.themes.dracula as style


class BriefingWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Cabeçalho
        self.header_layout = QHBoxLayout()

        # Título
        self.title_label = QLabel("Briefing")
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

        # Botão de gerar timeline
        self.timeline_button = QPushButton("Gerar Timeline")
        self.timeline_button.setIcon(QIcon("./resources/icons/timeline-generate.svg"))
        self.timeline_button.setStyleSheet(style.button_style)
        self.timeline_button.setFixedHeight(36)

        # Botão de salvar
        self.save_button = QPushButton("Salvar")
        self.save_button.setIcon(QIcon("./resources/icons/save.svg"))
        self.save_button.setStyleSheet(style.secondary_button_style)
        self.save_button.setFixedHeight(36)

        # Adicionar ao layout do cabeçalho
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(QLabel("Evento:"))
        self.header_layout.addWidget(self.event_selector)
        self.header_layout.addWidget(self.save_button)
        self.header_layout.addWidget(self.timeline_button)

        # Criar abas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(style.tab_style)

        # Abas do briefing
        self.info_tab = self.create_info_tab()
        self.style_tab = self.create_style_tab()
        self.references_tab = self.create_references_tab()
        self.sponsors_tab = self.create_sponsors_tab()
        self.schedule_tab = self.create_schedule_tab()
        self.deliveries_tab = self.create_deliveries_tab()

        # Adicionar abas ao widget de abas
        self.tabs.addTab(self.info_tab, "Informações Gerais")
        self.tabs.addTab(self.style_tab, "Estilo")
        self.tabs.addTab(self.references_tab, "Referências")
        self.tabs.addTab(self.sponsors_tab, "Patrocinadores")
        self.tabs.addTab(self.schedule_tab, "Programação")
        self.tabs.addTab(self.deliveries_tab, "Entregas")

        # Adicionar todos os layouts ao layout principal
        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.tabs)

    def create_info_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        info_edit = QTextEdit()
        info_edit.setStyleSheet(style.input_style)
        info_edit.setPlaceholderText("Insira informações gerais sobre o evento...")

        layout.addWidget(info_edit)

        return tab

    def create_style_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        style_edit = QTextEdit()
        style_edit.setStyleSheet(style.input_style)
        style_edit.setPlaceholderText(
            "Descreva o estilo visual desejado para as produções..."
        )

        layout.addWidget(style_edit)

        return tab

    def create_references_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        references_edit = QTextEdit()
        references_edit.setStyleSheet(style.input_style)
        references_edit.setPlaceholderText(
            "Links e referências para o estilo visual..."
        )

        layout.addWidget(references_edit)

        return tab

    def create_sponsors_tab(self):
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        tab.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """
        )

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(20)

        # Instruções
        instructions = QLabel(
            "Adicione patrocinadores e suas ações/ativações durante o evento:"
        )
        instructions.setStyleSheet(f"color: {style.foreground_color}; font-size: 14px;")
        instructions.setWordWrap(True)

        layout.addWidget(instructions)

        # Botão para adicionar patrocinador
        add_sponsor_btn = QPushButton("+ Novo Patrocinador")
        add_sponsor_btn.setStyleSheet(style.button_style)
        add_sponsor_btn.setFixedWidth(200)

        layout.addWidget(add_sponsor_btn)

        # Exemplo de patrocinador com ações
        sponsor_widget = self.create_sponsor_widget("Patrocinador A")
        layout.addWidget(sponsor_widget)

        # Outro exemplo
        sponsor_widget2 = self.create_sponsor_widget("Patrocinador B")
        layout.addWidget(sponsor_widget2)

        layout.addStretch()

        tab.setWidget(content)
        return tab

    def create_sponsor_widget(self, name):
        # Frame para o patrocinador
        frame = QFrame()
        frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
            }}
        """
        )

        layout = QVBoxLayout(frame)

        # Cabeçalho com nome do patrocinador
        header = QHBoxLayout()

        sponsor_selector = QComboBox()
        sponsor_selector.addItem(name)
        sponsor_selector.addItems(
            ["+ Novo patrocinador", "Patrocinador C", "Patrocinador D"]
        )
        sponsor_selector.setStyleSheet(style.combobox_style)
        sponsor_selector.setFixedWidth(250)

        remove_btn = QPushButton()
        remove_btn.setIcon(QIcon("./resources/icons/trash.svg"))
        remove_btn.setIconSize(QSize(16, 16))
        remove_btn.setFixedSize(30, 30)
        remove_btn.setStyleSheet(style.secondary_button_style)

        header.addWidget(QLabel("Patrocinador:"))
        header.addWidget(sponsor_selector)
        header.addStretch()
        header.addWidget(remove_btn)

        layout.addLayout(header)

        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(f"background-color: {style.current_line_color};")

        layout.addWidget(separator)

        # Container para ações
        actions_container = QVBoxLayout()
        actions_container.setSpacing(15)

        # Adicionar algumas ações de exemplo
        actions_container.addWidget(self.create_action_widget())
        actions_container.addWidget(self.create_action_widget())

        layout.addLayout(actions_container)

        # Botão para adicionar ação
        add_action_btn = QPushButton("+ Nova Ação")
        add_action_btn.setStyleSheet(style.secondary_button_style)
        add_action_btn.setFixedWidth(150)

        layout.addWidget(add_action_btn, 0, Qt.AlignLeft)

        return frame

    def create_action_widget(self):
        # Frame para a ação
        frame = QFrame()
        frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.current_line_color};
                border-radius: 8px;
            }}
        """
        )

        layout = QVBoxLayout(frame)

        # Cabeçalho com opção de remover
        header = QHBoxLayout()

        action_title = QLabel("Ação / Ativação")
        action_title.setStyleSheet(f"color: {style.purple_color}; font-weight: bold;")

        remove_btn = QPushButton()
        remove_btn.setIcon(QIcon("./resources/icons/trash.svg"))
        remove_btn.setIconSize(QSize(16, 16))
        remove_btn.setFixedSize(28, 28)
        remove_btn.setStyleSheet(style.secondary_button_style)

        header.addWidget(action_title)
        header.addStretch()
        header.addWidget(remove_btn)

        layout.addLayout(header)

        # Formulário para detalhes da ação
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignRight)
        form.setSpacing(15)

        # Campos do formulário
        action_name = QLineEdit()
        action_name.setStyleSheet(style.input_style)
        action_name.setPlaceholderText("Nome da ação/ativação")

        time_layout = QHBoxLayout()
        action_time = QTimeEdit()
        action_time.setStyleSheet(style.input_style)
        free_time = QCheckBox("Horário Livre")
        free_time.setStyleSheet(style.toggle_style)
        time_layout.addWidget(action_time)
        time_layout.addWidget(free_time)

        responsible = QComboBox()
        responsible.setStyleSheet(style.combobox_style)
        responsible.addItems(
            [
                "Selecionar responsável",
                "João Silva",
                "Maria Souza",
                "Carlos Lima",
            ]
        )

        realtime = QCheckBox("Entrega Real Time?")
        realtime.setStyleSheet(style.toggle_style)

        rt_time = QTimeEdit()
        rt_time.setStyleSheet(style.input_style)

        editor = QComboBox()
        editor.setStyleSheet(style.combobox_style)
        editor.addItems(["Selecionar editor", "Maria Souza", "Pedro Alves"])

        instructions = QTextEdit()
        instructions.setStyleSheet(style.input_style)
        instructions.setPlaceholderText("Orientações específicas...")
        instructions.setMaximumHeight(100)

        # Adicionar campos ao formulário
        form.addRow("Ação / Ativação:", action_name)
        form.addRow("Horário de captação:", time_layout)
        form.addRow("Responsável pela captação:", responsible)
        form.addRow("", realtime)
        form.addRow("Horário da entrega RT:", rt_time)
        form.addRow("Editor responsável:", editor)
        form.addRow("Orientações:", instructions)

        layout.addLayout(form)

        return frame

    def create_schedule_tab(self):
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        tab.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """
        )

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(20)

        # Instruções
        instructions = QLabel(
            "Adicione a programação completa do evento, organizada por palco:"
        )
        instructions.setStyleSheet(f"color: {style.foreground_color}; font-size: 14px;")
        instructions.setWordWrap(True)

        layout.addWidget(instructions)

        # Botão para adicionar palco
        add_stage_btn = QPushButton("+ Novo Palco")
        add_stage_btn.setStyleSheet(style.button_style)
        add_stage_btn.setFixedWidth(200)

        layout.addWidget(add_stage_btn)

        # Exemplo de palco com atrações
        stage_widget = self.create_stage_widget("Palco Principal")
        layout.addWidget(stage_widget)

        # Outro exemplo
        stage_widget2 = self.create_stage_widget("Palco Secundário")
        layout.addWidget(stage_widget2)

        layout.addStretch()

        tab.setWidget(content)
        return tab

    def create_stage_widget(self, name):
        # Frame para o palco
        frame = QFrame()
        frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.background_color};
                border-radius: 8px;
            }}
        """
        )

        layout = QVBoxLayout(frame)

        # Cabeçalho com nome do palco
        header = QHBoxLayout()

        stage_input = QLineEdit(name)
        stage_input.setStyleSheet(style.input_style)
        stage_input.setFixedWidth(250)

        remove_btn = QPushButton()
        remove_btn.setIcon(QIcon("./resources/icons/trash.svg"))
        remove_btn.setIconSize(QSize(16, 16))
        remove_btn.setFixedSize(30, 30)
        remove_btn.setStyleSheet(style.secondary_button_style)

        header.addWidget(QLabel("Palco:"))
        header.addWidget(stage_input)
        header.addStretch()
        header.addWidget(remove_btn)

        layout.addLayout(header)

        # Separador
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(f"background-color: {style.current_line_color};")

        layout.addWidget(separator)

        # Container para atrações
        attractions_container = QVBoxLayout()
        attractions_container.setSpacing(15)

        # Adicionar algumas atrações de exemplo
        attractions_container.addWidget(self.create_attraction_widget())
        attractions_container.addWidget(self.create_attraction_widget())

        layout.addLayout(attractions_container)

        # Botão para adicionar atração
        add_attraction_btn = QPushButton("+ Nova Atração")
        add_attraction_btn.setStyleSheet(style.secondary_button_style)
        add_attraction_btn.setFixedWidth(150)

        layout.addWidget(add_attraction_btn, 0, Qt.AlignLeft)

        return frame

    def create_attraction_widget(self):
        # Frame para a atração
        frame = QFrame()
        frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.current_line_color};
                border-radius: 8px;
            }}
        """
        )

        layout = QFormLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setLabelAlignment(Qt.AlignRight)

        # Campos do formulário
        artist = QLineEdit()
        artist.setStyleSheet(style.input_style)
        artist.setPlaceholderText("Nome do artista/atração")

        showtime = QTimeEdit()
        showtime.setStyleSheet(style.input_style)

        notes = QTextEdit()
        notes.setStyleSheet(style.input_style)
        notes.setPlaceholderText("Observações (opcional)...")
        notes.setMaximumHeight(80)

        # Botão de remover no canto superior direito
        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Atração"))
        header_layout.addStretch()

        remove_btn = QPushButton()
        remove_btn.setIcon(QIcon("./resources/icons/trash.svg"))
        remove_btn.setIconSize(QSize(16, 16))
        remove_btn.setFixedSize(28, 28)
        remove_btn.setStyleSheet(style.secondary_button_style)
        header_layout.addWidget(remove_btn)

        # Adicionar campos ao formulário
        layout.addRow(header_layout)
        layout.addRow("Artista:", artist)
        layout.addRow("Horário:", showtime)
        layout.addRow("Observações:", notes)

        return frame

    def create_deliveries_tab(self):
        tab = QScrollArea()
        tab.setWidgetResizable(True)
        tab.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """
        )

        content = QWidget()
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(30)

        # Seção Real Time
        rt_group = QGroupBox("Entregas Real Time")
        rt_group.setStyleSheet(
            f"""
            QGroupBox {{
                background-color: {style.background_color};
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: {style.purple_color};
                padding-top: 20px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding-left: 10px;
                padding-right: 10px;
                margin-top: 10px;
            }}
        """
        )

        rt_layout = QVBoxLayout(rt_group)

        # Container para entregas RT
        rt_deliveries = QVBoxLayout()
        rt_deliveries.setSpacing(15)

        # Adicionar entregas de exemplo
        rt_deliveries.addWidget(self.create_rt_delivery_widget())
        rt_deliveries.addWidget(self.create_rt_delivery_widget())
        rt_deliveries.addWidget(self.create_rt_delivery_widget())

        # Botão para adicionar nova entrega RT
        add_rt_btn = QPushButton("+ Nova Entrega Real Time")
        add_rt_btn.setStyleSheet(style.button_style)
        add_rt_btn.setFixedWidth(200)

        # Teaser final
        teaser_form = QFormLayout()
        teaser_form.setLabelAlignment(Qt.AlignRight)
        teaser_form.setSpacing(15)
        teaser_form.setContentsMargins(0, 10, 0, 0)

        teaser_time = QTimeEdit()
        teaser_time.setStyleSheet(style.input_style)

        teaser_form.addRow("Horário do teaser final:", teaser_time)

        rt_layout.addLayout(rt_deliveries)
        rt_layout.addWidget(add_rt_btn, 0, Qt.AlignLeft)
        rt_layout.addLayout(teaser_form)

        # Seção Pós-Evento
        post_group = QGroupBox("Entregas Pós-Evento")
        post_group.setStyleSheet(
            f"""
            QGroupBox {{
                background-color: {style.background_color};
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                color: {style.cyan_color};
                padding-top: 20px;
                margin-top: 10px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding-left: 10px;
                padding-right: 10px;
                margin-top: 10px;
            }}
        """
        )

        post_layout = QVBoxLayout(post_group)

        # Formulário para pós-evento
        post_form = QFormLayout()
        post_form.setLabelAlignment(Qt.AlignRight)
        post_form.setSpacing(15)

        # Campos
        deadline_layout = QHBoxLayout()
        deadline = QSpinBox()
        deadline.setMinimum(1)
        deadline.setMaximum(30)
        deadline.setValue(7)
        deadline.setStyleSheet(style.input_style)

        deadline_unit = QComboBox()
        deadline_unit.addItems(["horas", "dias"])
        deadline_unit.setStyleSheet(style.combobox_style)

        deadline_layout.addWidget(deadline)
        deadline_layout.addWidget(deadline_unit)

        # Opções de pacote
        package_group = QGroupBox("Opções de pacote:")
        package_group.setStyleSheet(
            f"""
            QGroupBox {{
                border: 1px solid {style.current_line_color};
                border-radius: 5px;
                margin-top: 15px;
                font-size: 14px;
                color: {style.foreground_color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                padding: 0 5px;
            }}
        """
        )

        package_layout = QVBoxLayout(package_group)

        aftermovie = QCheckBox("Aftermovie")
        aftermovie.setStyleSheet(style.toggle_style)

        highlights = QCheckBox("Vídeo de melhores momentos")
        highlights.setStyleSheet(style.toggle_style)

        sponsor_versions = QCheckBox("Versões individuais por patrocinador")
        sponsor_versions.setStyleSheet(style.toggle_style)

        package_layout.addWidget(aftermovie)
        package_layout.addWidget(highlights)
        package_layout.addWidget(sponsor_versions)

        # Notas adicionais
        notes = QTextEdit()
        notes.setStyleSheet(style.input_style)
        notes.setPlaceholderText("Anotações adicionais para entregas pós-evento...")
        notes.setMaximumHeight(100)

        # Adicionar ao formulário
        post_form.addRow("Prazo de entrega:", deadline_layout)
        post_form.addRow("", package_group)
        post_form.addRow("Anotações:", notes)

        post_layout.addLayout(post_form)

        # Adicionar seções ao layout principal
        layout.addWidget(rt_group)
        layout.addWidget(post_group)
        layout.addStretch()

        tab.setWidget(content)
        return tab

    def create_rt_delivery_widget(self):
        # Frame para a entrega RT
        frame = QFrame()
        frame.setStyleSheet(
            f"""
            QFrame {{
                background-color: {style.current_line_color};
                border-radius: 8px;
            }}
        """
        )

        layout = QFormLayout(frame)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 15, 10, 15)
        layout.setLabelAlignment(Qt.AlignRight)

        # Cabeçalho com opção de remover
        header = QHBoxLayout()
        header.addWidget(QLabel("Entrega Real Time"))
        header.addStretch()

        remove_btn = QPushButton()
        remove_btn.setIcon(QIcon("./resources/icons/trash.svg"))
        remove_btn.setIconSize(QSize(16, 16))
        remove_btn.setFixedSize(28, 28)
        remove_btn.setStyleSheet(style.secondary_button_style)
        header.addWidget(remove_btn)

        # Campos do formulário
        title = QLineEdit()
        title.setStyleSheet(style.input_style)
        title.setPlaceholderText("Título/descrição da entrega")

        delivery_time = QTimeEdit()
        delivery_time.setStyleSheet(style.input_style)

        editor = QComboBox()
        editor.setStyleSheet(style.combobox_style)
        editor.addItems(["Selecionar editor", "Maria Souza", "Pedro Alves"])

        # Plataformas
        platforms_group = QGroupBox("Plataforma de destino:")
        platforms_group.setStyleSheet(
            f"""
            QGroupBox {{
                border: 1px solid {style.comment_color};
                border-radius: 5px;
                margin-top: 10px;
                font-size: 12px;
                color: {style.foreground_color};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                padding: 0 5px;
            }}
        """
        )

        platforms_layout = QHBoxLayout(platforms_group)

        reels = QCheckBox("Reels")
        reels.setStyleSheet(style.toggle_style)

        stories = QCheckBox("Stories")
        stories.setStyleSheet(style.toggle_style)

        feed = QCheckBox("Feed")
        feed.setStyleSheet(style.toggle_style)

        other = QCheckBox("Outros")
        other.setStyleSheet(style.toggle_style)

        platforms_layout.addWidget(reels)
        platforms_layout.addWidget(stories)
        platforms_layout.addWidget(feed)
        platforms_layout.addWidget(other)

        instructions = QTextEdit()
        instructions.setStyleSheet(style.input_style)
        instructions.setPlaceholderText("Orientações específicas...")
        instructions.setMaximumHeight(80)

        # Adicionar ao layout
        layout.addRow(header)
        layout.addRow("Título/Descrição:", title)
        layout.addRow("Horário de entrega:", delivery_time)
        layout.addRow("Editor responsável:", editor)
        layout.addRow("", platforms_group)
        layout.addRow("Orientações:", instructions)

        return frame
