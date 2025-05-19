import os
import json
import random
import string
import datetime
from PySide6.QtWidgets import QMessageBox
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QSize, Qt

def load_config():
    """Carrega o arquivo de configuração."""
    try:
        with open("./config.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar configurações: {e}")
        return {}

def show_message(title, text, icon=QMessageBox.Icon.Information):
    """Exibe uma mensagem em um QMessageBox."""
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(icon)
    msg.exec()

def confirm_action(title, text):
    """Solicita confirmação do usuário para uma ação."""
    msg = QMessageBox()
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.setIcon(QMessageBox.Icon.Question)
    msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    msg.setDefaultButton(QMessageBox.StandardButton.No)
    return msg.exec() == QMessageBox.StandardButton.Yes

def generate_random_string(length=10):
    """Gera uma string aleatória com o comprimento especificado."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def format_date(date_str, input_format="%Y-%m-%d", output_format="%d/%m/%Y"):
    """Formata uma string de data."""
    try:
        date_obj = datetime.datetime.strptime(date_str, input_format)
        return date_obj.strftime(output_format)
    except:
        return date_str

def format_timestamp(timestamp):
    """Formata um timestamp para exibição."""
    if not timestamp:
        return ""
    
    try:
        if isinstance(timestamp, str):
            timestamp = float(timestamp)
        
        minutes = int(timestamp / 60)
        seconds = int(timestamp % 60)
        return f"{minutes:02d}:{seconds:02d}"
    except:
        return "00:00"

def ensure_directory_exists(path):
    """Garante que um diretório existe, criando-o se necessário."""
    if not os.path.exists(path):
        os.makedirs(path)

def sanitize_filename(filename):
    """Sanitiza um nome de arquivo, removendo caracteres inválidos."""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_file_extension(filename):
    """Retorna a extensão de um arquivo."""
    return os.path.splitext(filename)[1].lower()

def image_to_pixmap(image_path, max_size=None):
    """Converte uma imagem para QPixmap, redimensionando se necessário."""
    pixmap = QPixmap(image_path)
    
    if max_size and (pixmap.width() > max_size.width() or pixmap.height() > max_size.height()):
        pixmap = pixmap.scaled(max_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    
    return pixmap

def bytes_to_pixmap(data, max_size=None):
    """Converte dados binários para QPixmap, redimensionando se necessário."""
    image = QImage()
    image.loadFromData(data)
    pixmap = QPixmap.fromImage(image)
    
    if max_size and (pixmap.width() > max_size.width() or pixmap.height() > max_size.height()):
        pixmap = pixmap.scaled(max_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    
    return pixmap

def format_file_size(size):
    """Formata um tamanho de arquivo para exibição."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"

def time_since(timestamp):
    """Retorna uma string amigável representando o tempo desde o timestamp."""
    now = datetime.datetime.now()
    
    if isinstance(timestamp, str):
        try:
            timestamp = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        except:
            return timestamp
    
    diff = now - timestamp
    
    if diff.days > 365:
        return f"{diff.days // 365} ano(s) atrás"
    if diff.days > 30:
        return f"{diff.days // 30} mês(es) atrás"
    if diff.days > 0:
        return f"{diff.days} dia(s) atrás"
    if diff.seconds > 3600:
        return f"{diff.seconds // 3600} hora(s) atrás"
    if diff.seconds > 60:
        return f"{diff.seconds // 60} minuto(s) atrás"
    return "Agora mesmo"