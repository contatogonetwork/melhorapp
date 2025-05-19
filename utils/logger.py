"""
Módulo de logging para o sistema GoNetwork AI.

Este módulo fornece funcionalidades de logging padronizadas para todo o projeto.
"""

import logging
import os
from datetime import datetime
from pathlib import Path

# Cria o diretório de logs se não existir
log_dir = Path("logs")
if not log_dir.exists():
    log_dir.mkdir()

# Nome do arquivo de log com data atual
log_filename = f"gonetwork_{datetime.now().strftime('%Y%m%d')}.log"
log_path = log_dir / log_filename

# Configuração do logger
logger = logging.getLogger("gonetwork")
logger.setLevel(logging.DEBUG)

# Handler para arquivo
file_handler = logging.FileHandler(log_path)
file_handler.setLevel(logging.DEBUG)

# Handler para console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formato de log
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Adiciona os handlers ao logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_logger(name=None):
    """
    Retorna um logger configurado para o módulo especificado.

    Args:
        name (str, opcional): Nome do módulo. Se None, retorna o logger raiz.

    Returns:
        logging.Logger: Logger configurado.
    """
    if name:
        return logging.getLogger(f"gonetwork.{name}")
    return logger
