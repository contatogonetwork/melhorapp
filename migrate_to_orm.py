#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para migrar o banco de dados para uso com SQLAlchemy ORM.

Este script cria as tabelas do SQLAlchemy e migra os dados do banco de dados SQLite
existente para as novas tabelas, preservando os dados.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.resolve()))

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from database.Database import Database as OldDatabase
from database.orm.base import Base, engine
from database.orm.models.briefing import Briefing
from database.orm.models.client import Client
from database.orm.models.event import Event
from database.orm.models.event_team_members import event_team_members
from database.orm.models.team_member import TeamMember
from database.orm.models.user import User
from utils.logger import get_logger

# Configurar logger
logger = get_logger("migrate_to_orm")


def create_schema():
    """Cria o esquema do banco de dados baseado nos modelos SQLAlchemy."""
    logger.info("Criando esquema do banco de dados com SQLAlchemy...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Esquema criado com sucesso")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro ao criar esquema: {e}")
        return False


def migrate_users():
    """Migra os dados da tabela de usuários para o modelo SQLAlchemy."""
    logger.info("Migrando usuários...")
    db_old = OldDatabase()

    try:
        # Obter todos os usuários do banco antigo
        users = db_old.fetch_all("SELECT * FROM users")

        if not users:
            logger.warning("Nenhum usuário encontrado para migrar")
            return True

        # Inserir usuários no novo esquema
        with engine.begin() as conn:
            for user in users:
                conn.execute(
                    text(
                        """
                    INSERT INTO users (
                        id, username, email, full_name, password_hash, salt,
                        role, profile_picture, is_active, created_at, updated_at
                    ) VALUES (
                        :id, :username, :email, :full_name, :password_hash, :salt,
                        :role, :profile_picture, :is_active, :created_at, :updated_at
                    )
                    """
                    ),
                    {
                        "id": user["id"],
                        "username": user["username"],
                        "email": user["email"],
                        "full_name": user["full_name"],
                        "password_hash": user["password_hash"],
                        "salt": user["salt"],
                        "role": user["role"],
                        "profile_picture": user["profile_picture"],
                        "is_active": True,
                        "created_at": user["created_at"],
                        "updated_at": (
                            user["updated_at"]
                            if "updated_at" in user
                            else user["created_at"]
                        ),
                    },
                )

        logger.info(f"Migrados {len(users)} usuários com sucesso")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro ao migrar usuários: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao migrar usuários: {e}")
        return False


def migrate_clients():
    """Migra os dados da tabela de clientes para o modelo SQLAlchemy."""
    logger.info("Migrando clientes...")
    db_old = OldDatabase()

    try:
        # Obter todos os clientes do banco antigo
        clients = db_old.fetch_all("SELECT * FROM clients")

        if not clients:
            logger.warning("Nenhum cliente encontrado para migrar")
            return True

        # Inserir clientes no novo esquema
        with engine.begin() as conn:
            for client in clients:
                conn.execute(
                    text(
                        """
                    INSERT INTO clients (
                        id, company, contact_person, email, phone, created_at, updated_at
                    ) VALUES (
                        :id, :company, :contact_person, :email, :phone, :created_at, :updated_at
                    )
                    """
                    ),
                    {
                        "id": client["id"],
                        "company": client["company"],
                        "contact_person": client["contact_person"],
                        "email": client["email"],
                        "phone": client["phone"],
                        "created_at": client["created_at"],
                        "updated_at": (
                            client["updated_at"]
                            if "updated_at" in client
                            else client["created_at"]
                        ),
                    },
                )

        logger.info(f"Migrados {len(clients)} clientes com sucesso")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro ao migrar clientes: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao migrar clientes: {e}")
        return False


def migrate_team_members():
    """Migra os dados da tabela de membros da equipe para o modelo SQLAlchemy."""
    logger.info("Migrando membros da equipe...")
    db_old = OldDatabase()

    try:
        # Obter todos os membros da equipe do banco antigo
        members = db_old.fetch_all("SELECT * FROM team_members")

        if not members:
            logger.warning("Nenhum membro de equipe encontrado para migrar")
            return True

        # Inserir membros da equipe no novo esquema
        with engine.begin() as conn:
            for member in members:
                conn.execute(
                    text(
                        """
                    INSERT INTO team_members (
                        id, name, role, email, contact, created_at, updated_at
                    ) VALUES (
                        :id, :name, :role, :email, :contact, :created_at, :updated_at
                    )
                    """
                    ),
                    {
                        "id": member["id"],
                        "name": member["name"],
                        "role": member["role"],
                        "email": member["email"] if "email" in member else None,
                        "contact": member["contact"],
                        "created_at": member["created_at"],
                        "updated_at": (
                            member["updated_at"]
                            if "updated_at" in member
                            else member["created_at"]
                        ),
                    },
                )

        logger.info(f"Migrados {len(members)} membros de equipe com sucesso")
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro ao migrar membros de equipe: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao migrar membros de equipe: {e}")
        return False


def migrate_events():
    """Migra os dados da tabela de eventos para o modelo SQLAlchemy."""
    logger.info("Migrando eventos...")
    db_old = OldDatabase()

    try:
        # Obter todos os eventos do banco antigo
        events = db_old.fetch_all("SELECT * FROM events")

        if not events:
            logger.warning("Nenhum evento encontrado para migrar")
            return True

        # Inserir eventos no novo esquema
        with engine.begin() as conn:
            for event in events:
                conn.execute(
                    text(
                        """
                    INSERT INTO events (
                        id, name, date, location, client_id, type, status, created_at, updated_at
                    ) VALUES (
                        :id, :name, :date, :location, :client_id, :type, :status, :created_at, :updated_at
                    )
                    """
                    ),
                    {
                        "id": event["id"],
                        "name": event["name"],
                        "date": event["date"],
                        "location": event["location"],
                        "client_id": event["client_id"],
                        "type": event["type"],
                        "status": event["status"],
                        "created_at": event["created_at"],
                        "updated_at": (
                            event["updated_at"]
                            if "updated_at" in event
                            else event["created_at"]
                        ),
                    },
                )

        # Migrar relação entre eventos e membros de equipe
        event_team = db_old.fetch_all("SELECT * FROM event_team_members")

        if event_team:
            with engine.begin() as conn:
                for relation in event_team:
                    conn.execute(
                        text(
                            """
                        INSERT INTO event_team_members (
                            event_id, team_member_id, role, created_at
                        ) VALUES (
                            :event_id, :team_member_id, :role, :created_at
                        )
                        """
                        ),
                        {
                            "event_id": relation["event_id"],
                            "team_member_id": relation["team_member_id"],
                            "role": relation["role"] if "role" in relation else None,
                            "created_at": (
                                relation["created_at"]
                                if "created_at" in relation
                                else None
                            ),
                        },
                    )

        logger.info(f"Migrados {len(events)} eventos com sucesso")
        logger.info(
            f"Migradas {len(event_team) if event_team else 0} relações evento-equipe"
        )
        return True
    except SQLAlchemyError as e:
        logger.error(f"Erro ao migrar eventos: {e}")
        return False
    except Exception as e:
        logger.error(f"Erro inesperado ao migrar eventos: {e}")
        return False


def main():
    """Função principal de migração."""
    logger.info("Iniciando migração para SQLAlchemy ORM...")

    # Criar esquema
    if not create_schema():
        logger.error("Falha ao criar esquema. Mirgação cancelada.")
        sys.exit(1)

    # Migrar dados
    success = (
        migrate_users()
        and migrate_clients()
        and migrate_team_members()
        and migrate_events()
    )

    if success:
        logger.info("Migração concluída com sucesso!")
    else:
        logger.error("Migração concluída com erros. Verifique o log para detalhes.")
        sys.exit(1)


if __name__ == "__main__":
    main()
