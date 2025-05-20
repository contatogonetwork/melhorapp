"""
Módulo de logging para o sistema GoNetwork AI.

Este módulo fornece funcionalidades de logging padronizadas para todo o projeto,
incluindo rotação de logs e diferentes níveis de logging para arquivo e console.
"""

import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional

# Cria o diretório de logs se não existir
log_dir = Path("logs")
if not log_dir.exists():
    log_dir.mkdir()

# Nome do arquivo de log base
log_filename = "gonetwork.log"
log_path = log_dir / log_filename

# Configuração do logger
logger = logging.getLogger("gonetwork")
logger.setLevel(logging.DEBUG)

# Handler para arquivo com rotação
# Máximo de 5MB por arquivo, mantém até 10 arquivos de backup
file_handler = RotatingFileHandler(
    log_path, maxBytes=5_000_000, backupCount=10, encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# Handler para console
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Formato de log detalhado com contexto
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s"
)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Adiciona os handlers ao logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Retorna um logger configurado para o módulo especificado.

    O logger retornado está configurado com handlers para arquivo (com rotação)
    e console, com níveis de logging diferentes para cada um. O arquivo de log
    captura mensagens de DEBUG e acima, enquanto o console mostra INFO e acima.

    Args:
        name (str, opcional): Nome do módulo. Se None, retorna o logger raiz.

    Returns:
        logging.Logger: Logger configurado para o módulo especificado.

    Examples:
        >>> logger = get_logger("database")
        >>> logger.info("Conexão com o banco de dados estabelecida")
        >>> logger.error("Erro ao executar consulta", exc_info=True)
    """
    if name:
        return logging.getLogger(f"gonetwork.{name}")
    return logger
