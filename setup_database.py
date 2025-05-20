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

        # Criar assets de exemplo
        for asset in [
            {
                "event_id": event_id,
                "name": "Logo_RefreshCo.png",
                "file_path": "/uploads/assets/Logo_RefreshCo.png",
                "asset_type": ASSET_TYPES["LOGO"],
                "category": "Patrocinadores",
                "uploaded_by": admin_id,
                "uploaded_at": now,
            },
        ]:
            db.execute(
                """
                INSERT INTO assets (event_id, name, file_path, asset_type, category, uploaded_by, uploaded_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    asset["event_id"],
                    asset["name"],
                    asset["file_path"],
                    asset["asset_type"],
                    asset["category"],
                    asset["uploaded_by"],
                    asset["uploaded_at"],
                ),
            )

        # Criar edições de vídeo de exemplo
        video_edit_id_1 = "ed-1-" + now.replace(" ", "-").replace(":", "")
        video_edit_id_2 = "ed-2-" + now.replace(" ", "-").replace(":", "")

        # Adicionar edições de vídeo
        for video_edit in [
            {
                "id": video_edit_id_1,
                "event_id": event_id,
                "editor_id": editor_id,
                "title": "Vídeo de Abertura - Evento RefreshCo",
                "deadline": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
                "style": "Corporativo Moderno",
                "status": "Em edição",
                "video_path": "uploads/20250513_2343_Sleek Riviera Logo_simple_compose_01jv6at3t1e0g80czm73q5m66a.mp4",
                "created_at": now,
                "updated_at": now,
            },
            {
                "id": video_edit_id_2,
                "event_id": event_id,
                "editor_id": editor_id,
                "title": "Resumo do Evento - RefreshCo",
                "deadline": (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"),
                "style": "Dinâmico com Motion Graphics",
                "status": "Planejamento",
                "video_path": "",
                "created_at": now,
                "updated_at": now,
            },
        ]:
            db.execute(
                """
                INSERT INTO video_edits (id, event_id, editor_id, title, deadline, style, status, video_path, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    video_edit["id"],
                    video_edit["event_id"],
                    video_edit["editor_id"],
                    video_edit["title"],
                    video_edit["deadline"],
                    video_edit["style"],
                    video_edit["status"],
                    video_edit["video_path"],
                    video_edit["created_at"],
                    video_edit["updated_at"],
                ),
            )

        # Adicionar comentários às edições de vídeo
        comment_id_1 = "com-1-" + now.replace(" ", "-").replace(":", "")
        comment_id_2 = "com-2-" + now.replace(" ", "-").replace(":", "")

        for comment in [
            {
                "id": comment_id_1,
                "video_edit_id": video_edit_id_1,
                "user_id": client_id,
                "timestamp": 5000,  # 5 segundos no vídeo
                "comment": "Preciso que o logo da empresa apareça por mais tempo nesta parte inicial",
                "is_resolved": 0,
                "created_at": now,
            },
            {
                "id": comment_id_2,
                "video_edit_id": video_edit_id_1,
                "user_id": admin_id,
                "timestamp": 15000,  # 15 segundos no vídeo
                "comment": "Vamos trocar esta transição por algo mais suave?",
                "is_resolved": 1,
                "created_at": now,
            },
        ]:
            db.execute(
                """
                INSERT INTO video_comments (id, video_edit_id, user_id, timestamp, comment, is_resolved, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    comment["id"],
                    comment["video_edit_id"],
                    comment["user_id"],
                    comment["timestamp"],
                    comment["comment"],
                    comment["is_resolved"],
                    comment["created_at"],
                ),
            )

        # Adicionar uma entrega de editor
        delivery_id = "del-1-" + now.replace(" ", "-").replace(":", "")

        db.execute(
            """
            INSERT INTO editor_deliveries (id, video_edit_id, asset_refs, is_submitted, submitted_at, approval_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                delivery_id,
                video_edit_id_1,
                "uploads/20250513_2343_Sleek Riviera Logo_simple_compose_01jv6at3t1e0g80czm73q5m66a.mp4",
                1,
                now,
                "Pendente",
                now,
                now,
            ),
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

    # Definições das tabelas
    table_definitions = {
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
        "video_edits": """CREATE TABLE IF NOT EXISTS video_edits (
            id TEXT PRIMARY KEY,
            event_id TEXT NOT NULL,
            editor_id TEXT NOT NULL,
            title TEXT NOT NULL,
            deadline TEXT NOT NULL,
            style TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Em edição',
            video_path TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (editor_id) REFERENCES team_members(id)
        )""",
        "video_comments": """CREATE TABLE IF NOT EXISTS video_comments (
            id TEXT PRIMARY KEY,
            video_edit_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            timestamp INTEGER NOT NULL,  -- Em segundos
            comment TEXT NOT NULL,
            is_resolved INTEGER NOT NULL DEFAULT 0,  -- 0=pendente, 1=resolvido
            created_at TEXT NOT NULL,
            FOREIGN KEY (video_edit_id) REFERENCES video_edits(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )""",
        "editor_deliveries": """CREATE TABLE IF NOT EXISTS editor_deliveries (
            id TEXT PRIMARY KEY,
            video_edit_id TEXT NOT NULL,
            asset_refs TEXT,  -- Referências ou links para os assets
            is_submitted INTEGER NOT NULL DEFAULT 0,  -- 0=não, 1=sim
            submitted_at TEXT,
            approval_status TEXT NOT NULL DEFAULT 'Pendente',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (video_edit_id) REFERENCES video_edits(id)
        )""",
    }

    for nome, sql in table_definitions.items():
        cursor.execute(sql)

    conn.commit()
    conn.close()


def apply_edits_schema():
    """
    Aplica o esquema SQL para tabelas relacionadas à edição de vídeo.

    Returns:
        bool: True se as tabelas foram criadas com sucesso, False caso contrário
    """
    logger.info("Aplicando esquema para tabelas de edição de vídeo...")

    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect("./database/gonetwork.db")
        cursor = conn.cursor()

        # Ler o arquivo SQL
        schema_path = os.path.join("database", "schema", "video_edits_tables.sql")
        if not os.path.exists(schema_path):
            logger.error(f"Arquivo de esquema não encontrado: {schema_path}")
            return False

        with open(schema_path, "r", encoding="utf-8") as sql_file:
            sql_script = sql_file.read()

        # Executar as instruções SQL
        cursor.executescript(sql_script)
        conn.commit()

        # Verificar se as tabelas foram criadas
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name IN ('video_edits', 'video_comments', 'editor_deliveries')"
        )
        tables = cursor.fetchall()

        conn.close()

        if len(tables) == 3:
            logger.info("Tabelas de edição criadas com sucesso!")
            return True
        else:
            logger.warning(
                f"Nem todas as tabelas de edição foram criadas. Encontradas: {len(tables)}"
            )
            return False
    except Exception as e:
        logger.error(f"Erro ao aplicar esquema de edição: {str(e)}")
        return False


def main():
    """Função principal para executar a configuração do banco de dados."""
    if not os.path.exists("./database"):
        os.makedirs("./database")

    db_success = setup_database()
    if db_success and input("Deseja inserir dados de exemplo? (s/n): ").lower() == "s":
        insert_sample_data()

    criar_tabelas()
    print("Tabelas criadas ou já existentes no banco de dados.")

    # Aplicar esquema para tabelas de edição
    apply_edits_schema()

    print("\nProcesso de configuração do banco de dados concluído!")
    print("\nCredenciais de acesso:")
    print("- Admin: username=admin, senha=admin123")
    print("- Editor: username=maria, senha=editor123")
    print("- Cliente: username=cliente, senha=client123")


if __name__ == "__main__":
    main()
