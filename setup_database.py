"""
Script para inicialização e configuração do banco de dados do GoNetwork AI.

Este script cria as tabelas necessárias no banco de dados e
opcionalmente insere dados de exemplo para desenvolvimento e testes.
"""

import logging
import os
import sqlite3
import sys
from datetime import datetime, timedelta

import bcrypt

from database.db_manager import DatabaseManager
from utils.constants import (
    ASSET_TYPES,
    DELIVERY_STATUS,
    EVENT_STATUS,
    TEAM_ROLES,
)

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("setup_database")


def setup_database():
    """
    Inicializa o banco de dados e cria todas as tabelas necessárias.

    Returns:
        bool: True se as tabelas foram criadas com sucesso, False caso contrário
    """
    logger.info("Inicializando banco de dados...")
    db = None

    try:
        db = DatabaseManager()
        success = db.create_tables()

        if success:
            logger.info("Tabelas criadas com sucesso!")
            return True
        else:
            logger.error("Erro ao criar tabelas.")
            return False
    except Exception as e:
        logger.error(f"Erro inesperado ao configurar banco de dados: {str(e)}")
        return False


def insert_sample_data():
    """
    Insere dados de exemplo no banco de dados para desenvolvimento e testes.

    Returns:
        bool: True se os dados foram inseridos com sucesso, False caso contrário
    """
    logger.info("Inserindo dados de exemplo...")
    db = DatabaseManager()

    try:
        # Criar usuários de exemplo
        admin_password = bcrypt.hashpw(
            "admin123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        editor_password = bcrypt.hashpw(
            "editor123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        client_password = bcrypt.hashpw(
            "client123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Administrador
        admin_id = db.insert(
            "users",
            {
                "username": "admin",
                "email": "admin@gonetwork.ai",
                "password": admin_password,
                "full_name": "Administrador",
                "role": "admin",
                "profile_picture": None,
                "created_at": now,
                "updated_at": now,
            },
        )

        # Editor
        editor_id = db.insert(
            "users",
            {
                "username": "maria",
                "email": "maria@gonetwork.ai",
                "password": editor_password,
                "full_name": "Maria Souza",
                "role": "editor",
                "profile_picture": None,
                "created_at": now,
                "updated_at": now,
            },
        )

        # Cinegrafista
        cameraman_id = db.insert(
            "users",
            {
                "username": "joao",
                "email": "joao@gonetwork.ai",
                "password": editor_password,
                "full_name": "João Silva",
                "role": "cameraman",
                "profile_picture": None,
                "created_at": now,
                "updated_at": now,
            },
        )

        # Cliente
        client_id = db.insert(
            "users",
            {
                "username": "cliente",
                "email": "cliente@empresa.com",
                "password": client_password,
                "full_name": "Cliente XYZ",
                "role": "client",
                "profile_picture": None,
                "created_at": now,
                "updated_at": now,
            },
        )

        # Criar evento de exemplo
        start_date = datetime.now() + timedelta(days=15)
        end_date = start_date + timedelta(days=2)

        event_id = db.insert(
            "events",
            {
                "name": "Festival de Música",
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "location": "São Paulo, SP",
                "client_id": client_id,
                "status": EVENT_STATUS["SCHEDULED"],
                "created_by": admin_id,
                "created_at": now,
                "updated_at": now,
            },
        )

        # Adicionar equipe ao evento
        db.insert(
            "event_team",
            {
                "event_id": event_id,
                "user_id": editor_id,
                "role": TEAM_ROLES["EDITOR"],
                "equipment": "Laptop, Adobe Premiere",
            },
        )

        db.insert(
            "event_team",
            {
                "event_id": event_id,
                "user_id": cameraman_id,
                "role": TEAM_ROLES["CAMERAMAN"],
                "equipment": "Sony A7III, DJI Ronin",
            },
        )

        # Criar briefing básico
        briefing_id = db.insert(
            "briefings",
            {
                "event_id": event_id,
                "general_info": "Festival de música com diversos artistas. Evento de 3 dias com 2 palcos principais.",
                "style_info": "Estilo visual dinâmico, cores vibrantes, cortes rápidos para reels.",
                "references_info": "Ver links de referência em: https://example.com/referencias",
                "created_at": now,
                "updated_at": now,
            },
        )

        # Adicionar patrocinadores
        sponsor_id = db.insert(
            "sponsors", {"event_id": event_id, "name": "Bebidas RefreshCo"}
        )

        # Adicionar ações do patrocinador
        db.insert(
            "sponsor_actions",
            {
                "sponsor_id": sponsor_id,
                "action_name": "Stand de degustação",
                "capture_time": "15:30",
                "is_free_time": False,
                "responsible_id": cameraman_id,
                "is_real_time": True,
                "delivery_time": "16:30",
                "editor_id": editor_id,
                "instructions": "Captar interações dos visitantes com os produtos. Destacar logomarca.",
            },
        )

        # Adicionar palco
        stage_id = db.insert(
            "stages", {"event_id": event_id, "name": "Palco Principal"}
        )

        # Adicionar atrações
        db.insert(
            "attractions",
            {
                "stage_id": stage_id,
                "name": "Banda Principal",
                "time": "21:00",
                "notes": "Headliner do festival. Foco especial nas transições entre músicas.",
            },
        )

        db.insert(
            "attractions",
            {
                "stage_id": stage_id,
                "name": "DJ Opening",
                "time": "18:00",
                "notes": "Set de abertura. Captar reações do público.",
            },
        )

        # Adicionar entregas Real Time
        db.insert(
            "realtime_deliveries",
            {
                "event_id": event_id,
                "title": "Abertura do evento",
                "delivery_time": "19:00",
                "editor_id": editor_id,
                "platforms": "Reels,Stories",
                "instructions": "Vídeo de 30 segundos com os highlights da entrada do público e início do evento.",
            },
        )

        db.insert(
            "realtime_deliveries",
            {
                "event_id": event_id,
                "title": "Patrocinador - RefreshCo",
                "delivery_time": "20:30",
                "editor_id": editor_id,
                "platforms": "Feed,Stories",
                "instructions": "Destaque para o espaço do patrocinador com interação do público.",
            },
        )

        # Adicionar entrega pós-evento
        db.insert(
            "post_deliveries",
            {
                "event_id": event_id,
                "deadline": 7,
                "deadline_unit": "dias",
                "has_aftermovie": True,
                "has_highlights": True,
                "has_sponsor_versions": True,
                "notes": "Aftermovie com duração de 2-3 minutos. Highlights de 30-45 segundos.",
            },
        )

        # Adicionar alguns vídeos
        video_id = db.insert(
            "videos",
            {
                "event_id": event_id,
                "title": "Teaser - Festival de Música",
                "description": "Vídeo teaser promocional para redes sociais",
                "editor_id": editor_id,
                "status": DELIVERY_STATUS["IN_REVIEW"],
                "version": "2.1",
                "file_path": "/uploads/videos/teaser_v2-1.mp4",
                "created_at": now,
                "updated_at": now,
            },
        )

        # Adicionar comentário no vídeo
        db.insert(
            "video_comments",
            {
                "video_id": video_id,
                "user_id": client_id,
                "comment": "Gostei muito da edição, mas poderia aumentar o tempo da logomarca no final.",
                "timestamp": "00:22",
                "created_at": now,
            },
        )

        # Adicionar assets
        db.insert(
            "assets",
            {
                "event_id": event_id,
                "name": "Logo_RefreshCo.png",
                "file_path": "/uploads/assets/Logo_RefreshCo.png",
                "asset_type": ASSET_TYPES["LOGO"],
                "category": "Patrocinadores",
                "uploaded_by": admin_id,
                "uploaded_at": now,
            },
        )

        logger.info("Dados de exemplo inseridos com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro ao inserir dados de exemplo: {e}")
        return False


# Corrigindo tabelas ausentes no banco de dados
def criar_tabelas():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    tabelas = {
        "events": """CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL
        )""",
        "team_members": """CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT NOT NULL
        )""",
        "clients": """CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL
        )""",
        "users": """CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )""",
        "briefings": """CREATE TABLE IF NOT EXISTS briefings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER NOT NULL,
            details TEXT NOT NULL,
            FOREIGN KEY(event_id) REFERENCES events(id)
        )""",
    }

    for nome, sql in tabelas.items():
        cursor.execute(sql)

    conn.commit()
    conn.close()


def main():
    """Função principal para executar a configuração do banco de dados."""
    if not os.path.exists("./database"):
        os.makedirs("./database")

    db_success = setup_database()
    if (
        db_success
        and input("Deseja inserir dados de exemplo? (s/n): ").lower() == "s"
    ):
        insert_sample_data()

    criar_tabelas()
    print("Tabelas criadas ou já existentes no banco de dados.")

    print("\nProcesso de configuração do banco de dados concluído!")
    print("\nCredenciais de acesso:")
    print("- Admin: username=admin, senha=admin123")
    print("- Editor: username=maria, senha=editor123")
    print("- Cliente: username=cliente, senha=client123")


if __name__ == "__main__":
    main()
