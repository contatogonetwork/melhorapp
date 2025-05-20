#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para configurar o Alembic para migrações de banco de dados.

Este script inicializa a estrutura de diretórios e arquivos para usar o Alembic
para gerenciar migrações de banco de dados na aplicação GoNetwork AI.
"""

import os
import subprocess
import sys
from pathlib import Path

from utils.logger import get_logger

# Configurar logger
logger = get_logger("setup_migrations")

# Diretório raiz do projeto
ROOT_DIR = Path(__file__).parent.resolve()
# Diretório para as migrações
MIGRATIONS_DIR = ROOT_DIR / "migrations"


def criar_estrutura_alembic():
    """Cria a estrutura de diretórios e arquivos para o Alembic."""
    logger.info("Criando estrutura de diretórios para migrações...")

    # Verificar se o diretório de migrações já existe
    if MIGRATIONS_DIR.exists():
        logger.warning(f"Diretório de migrações {MIGRATIONS_DIR} já existe")
        resposta = input("Deseja recriar a estrutura? [s/N] ")
        if resposta.lower() != "s":
            logger.info("Operação cancelada pelo usuário")
            return False

    # Criar diretório de migrações se não existir
    MIGRATIONS_DIR.mkdir(exist_ok=True)

    # Inicializar o Alembic
    try:
        logger.info("Inicializando Alembic...")
        result = subprocess.run(
            ["alembic", "init", "migrations"],
            cwd=ROOT_DIR,
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(f"Alembic inicializado: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao inicializar Alembic: {e.stderr}")
        return False


def configurar_alembic():
    """Configura os arquivos do Alembic para usar SQLAlchemy."""
    logger.info("Configurando Alembic...")

    # Caminho do arquivo de configuração do Alembic
    config_path = ROOT_DIR / "alembic.ini"

    if not config_path.exists():
        logger.error(f"Arquivo de configuração {config_path} não encontrado")
        return False

    try:
        # Atualizar arquivo de configuração
        with open(config_path, "r", encoding="utf-8") as f:
            config_content = f.read()

        # Atualizar URL do banco de dados
        config_content = config_content.replace(
            "sqlalchemy.url = driver://user:pass@localhost/dbname",
            "sqlalchemy.url = sqlite:///data/gonetwork.db",
        )

        with open(config_path, "w", encoding="utf-8") as f:
            f.write(config_content)

        logger.info("Arquivo alembic.ini atualizado com sucesso")

        # Atualizar arquivo env.py
        env_path = ROOT_DIR / "migrations" / "env.py"

        with open(env_path, "r", encoding="utf-8") as f:
            env_content = f.read()

        # Modificar para importar modelos e metadata automaticamente
        import_statement = (
            "import os\n"
            "import sys\n"
            "sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))\n"
            "from database.orm.base import Base\n"
            "from database.orm.models import *\n\n"
            "target_metadata = Base.metadata\n"
        )

        env_content = env_content.replace("target_metadata = None", import_statement)

        with open(env_path, "w", encoding="utf-8") as f:
            f.write(env_content)

        logger.info("Arquivo env.py atualizado com sucesso")

        return True
    except Exception as e:
        logger.error(f"Erro ao configurar Alembic: {e}")
        return False


def criar_migracao_inicial():
    """Cria a migração inicial."""
    logger.info("Criando migração inicial...")

    try:
        result = subprocess.run(
            ["alembic", "revision", "--autogenerate", "-m", "Migração inicial"],
            cwd=ROOT_DIR,
            check=True,
            capture_output=True,
            text=True,
        )
        logger.info(f"Migração inicial criada: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro ao criar migração inicial: {e.stderr}")
        return False


def main():
    """Função principal."""
    logger.info("Iniciando configuração de migrações com Alembic...")

    # Criar estrutura
    if not criar_estrutura_alembic():
        logger.error("Falha ao criar estrutura do Alembic")
        sys.exit(1)

    # Configurar Alembic
    if not configurar_alembic():
        logger.error("Falha ao configurar Alembic")
        sys.exit(1)

    # Criar migração inicial
    if not criar_migracao_inicial():
        logger.error("Falha ao criar migração inicial")
        sys.exit(1)

    logger.info("Configuração de migrações concluída com sucesso!")
    logger.info("\nPara aplicar migrações, execute:")
    logger.info("alembic upgrade head")
    logger.info("\nPara criar novas migrações após alterar modelos:")
    logger.info('alembic revision --autogenerate -m "Descrição da mudança"')


if __name__ == "__main__":
    main()
