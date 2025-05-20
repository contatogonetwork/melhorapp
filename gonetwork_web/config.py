import json
import os

import streamlit as st


def load_config():
    """
    Carrega as configurações do aplicativo.
    Primeiro verifica se existe um arquivo de configuração na pasta de configuração do aplicativo web.
    Se não existir, tenta carregar do arquivo de configuração principal do aplicativo desktop.
    """
    # Diretório raiz do aplicativo web
    web_root = os.path.dirname(os.path.abspath(__file__))

    # Caminho para o arquivo de configuração web
    web_config_path = os.path.join(web_root, "config", "app_config.json")

    # Caminho para o arquivo de configuração desktop
    desktop_config_path = os.path.join(os.path.dirname(web_root), "config.json")

    # Primeiro, tenta carregar do arquivo de configuração web
    if os.path.exists(web_config_path):
        try:
            with open(web_config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configuração web: {e}")

    # Se não existir ou falhar, tenta carregar do arquivo de configuração desktop
    if os.path.exists(desktop_config_path):
        try:
            with open(desktop_config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configuração desktop: {e}")

    # Se nenhum arquivo de configuração for encontrado, retorna uma configuração padrão
    return {
        "app_name": "GoNetwork AI Web",
        "version": "1.0.0",
        "database": {
            "path": os.path.join(os.path.dirname(web_root), "data", "gonetwork.db")
        },
        "theme": {
            "primary_color": "#1E88E5",
            "secondary_color": "#64B5F6",
            "accent_color": "#FFC107",
        },
    }


def save_config(config_data):
    """
    Salva as configurações do aplicativo no arquivo de configuração web.
    """
    # Diretório raiz do aplicativo web
    web_root = os.path.dirname(os.path.abspath(__file__))

    # Caminho para o arquivo de configuração web
    config_dir = os.path.join(web_root, "config")
    config_path = os.path.join(config_dir, "app_config.json")

    # Garante que o diretório de configuração existe
    os.makedirs(config_dir, exist_ok=True)

    # Salva o arquivo de configuração
    try:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar configuração: {e}")
        return False


# Configurações padrão do aplicativo
DEFAULT_CONFIG = {
    "app_name": "GoNetwork AI Web",
    "version": "1.0.0",
    "database": {"path": "../data/gonetwork.db"},
    "theme": {
        "primary_color": "#1E88E5",
        "secondary_color": "#64B5F6",
        "accent_color": "#FFC107",
    },
}


def get_secret(key, default=None):
    """
    Obtém um valor de segredo do arquivo de secrets do Streamlit.
    Se não estiver disponível, retorna o valor padrão.

    Args:
        key: Chave do segredo, pode incluir subcategorias (ex: "db_credentials.password")
        default: Valor padrão se o segredo não for encontrado

    Returns:
        O valor do segredo ou o valor padrão
    """
    try:
        # Dividir a chave em partes (para acessar subcategorias)
        parts = key.split(".")

        # Tentar obter o segredo
        value = st.secrets
        for part in parts:
            value = value[part]

        return value
    except (KeyError, TypeError):
        return default
