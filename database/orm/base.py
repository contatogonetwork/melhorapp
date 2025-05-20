#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuração e base do ORM SQLAlchemy para o GoNetwork AI.

Este módulo define a sessão do SQLAlchemy, o engine de conexão com o banco de dados
e a classe base para todos os modelos ORM.
"""

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from utils.logger import get_logger

# Configurar logger para o ORM
logger = get_logger("database.orm")

# Caminho do banco de dados
DATA_DIR = Path("data")
DB_PATH = DATA_DIR / "gonetwork.db"

# Garantir que o diretório de dados exista
DATA_DIR.mkdir(exist_ok=True)

# Criar engine do SQLAlchemy
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Para SQLite
    echo=False,  # Desativar saída SQL para produção, True para debugging
)

# Criar fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para todos os modelos
Base = declarative_base()


@contextmanager
def get_db_session() -> Generator[Session, None, None]:
    """
    Fornece uma sessão do SQLAlchemy para uso em um bloco with.
    Garante que a sessão seja fechada após o uso.

    Yields:
        Session: Uma sessão do SQLAlchemy

    Examples:
        >>> with get_db_session() as db:
        ...     users = db.query(User).all()
    """
    session = SessionLocal()
    try:
        logger.debug("Sessão SQLAlchemy iniciada")
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"Erro na sessão SQLAlchemy: {e}")
        raise
    finally:
        session.close()
        logger.debug("Sessão SQLAlchemy fechada")
