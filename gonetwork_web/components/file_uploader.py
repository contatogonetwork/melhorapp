import os
import random
import string
from datetime import datetime

import streamlit as st


def handle_uploaded_file(uploaded_file, folder_path=None):
    """
    Manipula o upload de um arquivo e o salva no diretório especificado.

    Args:
        uploaded_file: O arquivo carregado pelo usuário via st.file_uploader
        folder_path: O diretório onde o arquivo deve ser salvo

    Returns:
        str: O caminho para o arquivo salvo, ou None se houver falha
    """
    if not uploaded_file:
        return None

    if folder_path is None:
        # Caminho padrão para uploads
        folder_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data",
            "uploads",
        )

    # Garantir que o diretório exista
    os.makedirs(folder_path, exist_ok=True)

    # Gerar um nome de arquivo único baseado em timestamp e string aleatória
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=5))
    file_extension = os.path.splitext(uploaded_file.name)[1]

    # Criar o novo nome de arquivo
    safe_filename = f"{timestamp}_{random_string}{file_extension}"
    file_path = os.path.join(folder_path, safe_filename)

    try:
        # Salvar o arquivo
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Retornar o caminho relativo para armazenar no banco de dados
        return os.path.join("data", "uploads", safe_filename)
    except Exception as e:
        st.error(f"Erro ao salvar arquivo: {e}")
        return None


def generate_thumbnail(file_path, size=(100, 100)):
    """
    Gera uma miniatura para um arquivo de imagem

    Args:
        file_path: Caminho para o arquivo de imagem
        size: Tamanho da miniatura (largura, altura)

    Returns:
        PIL Image: A imagem em miniatura
    """
    try:
        from PIL import Image

        # Verificar se o caminho é válido
        if not os.path.exists(file_path):
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            file_path = os.path.join(base_dir, file_path)

        if not os.path.exists(file_path):
            return None

        # Abrir a imagem e criar miniatura
        image = Image.open(file_path)
        image.thumbnail(size)
        return image
    except Exception as e:
        return None
