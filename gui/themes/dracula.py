# Tema PyDracula para GoNetwork AI

# Cores principais
background_color = "#282A36"
current_line_color = "#44475A"
foreground_color = "#F8F8F2"
comment_color = "#6272A4"
cyan_color = "#8BE9FD"
green_color = "#50FA7B"
orange_color = "#FFB86C"
pink_color = "#FF79C6"
purple_color = "#BD93F9"
red_color = "#FF5555"
yellow_color = "#F1FA8C"

# Variáveis adicionais necessárias
PRIMARY = purple_color
PRIMARY_LIGHT = "#CBA5FE" 
BG_THREE = "#383A59"
BG_FOUR = "#2D303E"
SUCCESS = green_color
FONT_COLOR = foreground_color

# Estilos para componentes

# Estilo da barra de título
title_bar_style = f"""
    QFrame {{
        background-color: {background_color};
        border: none;
    }}
"""

# Estilo para o título
title_label_style = f"""
    QLabel {{
        color: {purple_color};
        font-size: 16px;
        font-weight: bold;
        padding-left: 5px;
    }}
"""

# Estilo para botões de controle de janela
window_button_style = f"""
    QPushButton {{
        background-color: {background_color};
        border-radius: 5px;
        border: none;
    }}
    QPushButton:hover {{
        background-color: {current_line_color};
    }}
    QPushButton:pressed {{
        background-color: {comment_color};
    }}
"""

# Estilo específico para o botão fechar
close_button_style = f"""
    QPushButton {{
        background-color: {background_color};
        border-radius: 5px;
        border: none;
    }}
    QPushButton:hover {{
        background-color: {red_color};
    }}
    QPushButton:pressed {{
        background-color: #AA3333;
    }}
"""

# Estilo para o botão de toggle do menu
toggle_button_style = f"""
    QPushButton {{
        background-color: {background_color};
        border-radius: 5px;
        border: none;
    }}
    QPushButton:hover {{
        background-color: {current_line_color};
    }}
    QPushButton:pressed {{
        background-color: {comment_color};
    }}
"""

# Estilo para o menu lateral
sidebar_style = f"""
    QFrame {{
        background-color: {background_color};
        border-top-right-radius: 10px;
    }}
"""

# Estilo para botões de menu
menu_button_style = f"""
    QPushButton {{
        color: {foreground_color};
        background-color: transparent;
        text-align: left;
        border-radius: 5px;
        padding: 5px;
    }}
    QPushButton:hover {{
        background-color: {current_line_color};
    }}
    QPushButton:checked {{
        background-color: {purple_color};
        color: {background_color};
    }}
"""

# Estilo para botões de menu ativos
menu_button_active_style = f"""
    QPushButton {{
        color: {background_color};
        background-color: {purple_color};
        text-align: left;
        border-radius: 5px;
        padding: 5px;
        font-weight: bold;
    }}
"""

# Estilo para a área de conteúdo
content_area_style = f"""
    QStackedWidget {{
        background-color: #21232D;
        border-radius: 10px;
    }}
"""

# Estilo para widgets de input
input_style = f"""
    QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox, QTimeEdit, QDateEdit, QDateTimeEdit {{
        background-color: {current_line_color};
        color: {foreground_color};
        border-radius: 5px;
        border: 1px solid {comment_color};
        padding: 5px;
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus,
    QTimeEdit:focus, QDateEdit:focus, QDateTimeEdit:focus {{
        border: 2px solid {purple_color};
    }}
"""

# Estilo para checkbox e radio button
toggle_style = f"""
    QCheckBox, QRadioButton {{
        color: {foreground_color};
    }}
    QCheckBox::indicator, QRadioButton::indicator {{
        width: 18px;
        height: 18px;
        background-color: {current_line_color};
        border: 1px solid {comment_color};
        border-radius: 3px;
    }}
    QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
        background-color: {purple_color};
    }}
    QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
        border: 1px solid {purple_color};
    }}
"""

# Estilo para combobox
combobox_style = f"""
    QComboBox {{
        background-color: {current_line_color};
        color: {foreground_color};
        border-radius: 5px;
        border: 1px solid {comment_color};
        padding: 5px;
        padding-right: 20px;
    }}
    QComboBox:focus {{
        border: 2px solid {purple_color};
    }}
    QComboBox::drop-down {{
        border: none;
        background-color: transparent;
    }}
    QComboBox::down-arrow {{
        image: url(./resources/icons/arrow-down.svg);
        width: 12px;
        height: 12px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {background_color};
        color: {foreground_color};
        border: 1px solid {comment_color};
        selection-background-color: {purple_color};
        selection-color: {background_color};
        border-radius: 0px;
    }}
"""

# Estilo para botões
button_style = f"""
    QPushButton {{
        background-color: {purple_color};
        color: {background_color};
        border-radius: 5px;
        padding: 8px 15px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: {PRIMARY_LIGHT};
    }}
    QPushButton:pressed {{
        background-color: #A77BDB;
    }}
    QPushButton:disabled {{
        background-color: {current_line_color};
        color: {comment_color};
    }}
"""

# Botão primário (referência ao button_style)
btn_primary = button_style

# Estilo para botões secundários
btn_secondary = f"""
    QPushButton {{
        background-color: {current_line_color};
        border-radius: 5px;
        border: none;
        padding: 5px 10px;
        color: {foreground_color};
    }}
    QPushButton:hover {{
        background-color: {comment_color};
    }}
    QPushButton:pressed {{
        background-color: {purple_color};
        color: {background_color};
    }}
"""

# Estilo para botões secundários
secondary_button_style = f"""
    QPushButton {{
        background-color: {comment_color};
        color: {foreground_color};
        border-radius: 5px;
        padding: 8px 15px;
    }}
    QPushButton:hover {{
        background-color: #7D8AC1;
    }}
    QPushButton:pressed {{
        background-color: #4D5A8E;
    }}
"""

# Botões específicos para status
btn_success = f"""
    QPushButton {{
        background-color: {green_color};
        color: {background_color};
        border-radius: 5px;
        padding: 8px 15px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #6DFB93;
    }}
    QPushButton:pressed {{
        background-color: #42E869;
    }}
"""

btn_danger = f"""
    QPushButton {{
        background-color: {red_color};
        color: {foreground_color};
        border-radius: 5px;
        padding: 8px 15px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #FF7777;
    }}
    QPushButton:pressed {{
        background-color: #E64545;
    }}
"""

btn_warning = f"""
    QPushButton {{
        background-color: {orange_color};
        color: {background_color};
        border-radius: 5px;
        padding: 8px 15px;
        font-weight: bold;
    }}
    QPushButton:hover {{
        background-color: #FFCA8F;
    }}
    QPushButton:pressed {{
        background-color: #E5A658;
    }}
"""

# Estilo para tabelas e listas
table_style = f"""
    QTableView, QListView, QTreeView {{
        background-color: {background_color};
        color: {foreground_color};
        border-radius: 5px;
        border: 1px solid {comment_color};
    }}
    QTableView::item, QListView::item, QTreeView::item {{
        padding: 5px;
    }}
    QTableView::item:selected, QListView::item:selected, QTreeView::item:selected {{
        background-color: {purple_color};
        color: {background_color};
    }}
    QHeaderView::section {{
        background-color: {current_line_color};
        color: {foreground_color};
        padding: 5px;
        border: none;
    }}
"""

# Estilo para barras de rolagem
scrollbar_style = f"""
    QScrollBar:vertical {{
        border: none;
        background-color: {background_color};
        width: 12px;
        margin: 12px 0 12px 0;
        border-radius: 0px;
    }}
    QScrollBar::handle:vertical {{
        background-color: {comment_color};
        min-height: 25px;
        border-radius: 6px;
    }}
    QScrollBar::handle:vertical:hover {{
        background-color: {purple_color};
    }}
    QScrollBar::sub-line:vertical {{
        border: none;
        background-color: {current_line_color};
        height: 12px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        subcontrol-position: top;
        subcontrol-origin: margin;
    }}
    QScrollBar::sub-line:vertical:hover {{
        background-color: {comment_color};
    }}
    QScrollBar::add-line:vertical {{
        border: none;
        background-color: {current_line_color};
        height: 12px;
        border-bottom-left-radius: 6px;
        border-bottom-right-radius: 6px;
        subcontrol-position: bottom;
        subcontrol-origin: margin;
    }}
    QScrollBar::add-line:vertical:hover {{
        background-color: {comment_color};
    }}
    QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
        background: none;
    }}
    QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
        background: none;
    }}

    QScrollBar:horizontal {{
        border: none;
        background-color: {background_color};
        height: 12px;
        margin: 0 12px 0 12px;
        border-radius: 0px;
    }}
    QScrollBar::handle:horizontal {{
        background-color: {comment_color};
        min-width: 25px;
        border-radius: 6px;
    }}
    QScrollBar::handle:horizontal:hover {{
        background-color: {purple_color};
    }}
    QScrollBar::sub-line:horizontal {{
        border: none;
        background-color: {current_line_color};
        width: 12px;
        border-top-left-radius: 6px;
        border-bottom-left-radius: 6px;
        subcontrol-position: left;
        subcontrol-origin: margin;
    }}
    QScrollBar::sub-line:horizontal:hover {{
        background-color: {comment_color};
    }}
    QScrollBar::add-line:horizontal {{
        border: none;
        background-color: {current_line_color};
        width: 12px;
        border-top-right-radius: 6px;
        border-bottom-right-radius: 6px;
        subcontrol-position: right;
        subcontrol-origin: margin;
    }}
    QScrollBar::add-line:horizontal:hover {{
        background-color: {comment_color};
    }}
    QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {{
        background: none;
    }}
    QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
        background: none;
    }}
"""

# Estilo para abas
tab_style = f"""
    QTabWidget::pane {{
        border: 1px solid {comment_color};
        border-radius: 5px;
        background-color: {background_color};
    }}
    QTabBar::tab {{
        background-color: {current_line_color};
        color: {foreground_color};
        padding: 8px 15px;
        margin-right: 2px;
        border-top-left-radius: 5px;
        border-top-right-radius: 5px;
    }}
    QTabBar::tab:selected {{
        background-color: {purple_color};
        color: {background_color};
    }}
    QTabBar::tab:hover:!selected {{
        background-color: {comment_color};
    }}
"""

# Estilo para mensagens e alertas
alert_style = {
    "info": f"""
        QFrame {{
            background-color: #3D59A1;
            color: {foreground_color};
            border-radius: 5px;
            padding: 10px;
        }}
    """,
    "success": f"""
        QFrame {{
            background-color: #4A8B4F;
            color: {foreground_color};
            border-radius: 5px;
            padding: 10px;
        }}
    """,
    "warning": f"""
        QFrame {{
            background-color: #9C7F29;
            color: {foreground_color};
            border-radius: 5px;
            padding: 10px;
        }}
    """,
    "error": f"""
        QFrame {{
            background-color: #A1453D;
            color: {foreground_color};
            border-radius: 5px;
            padding: 10px;
        }}
    """,
}