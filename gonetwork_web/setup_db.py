"""
Script para configurar o banco de dados da aplicação web GoNetwork.
Este script deve ser executado pelo menos uma vez antes de usar a aplicação.
"""

import os
import sqlite3
import uuid
from datetime import datetime


def setup_database():
    """
    Configura o banco de dados da aplicação, criando todas as tabelas necessárias.
    """
    # Caminho para o banco de dados
    db_path = os.path.join(
        "c:\\melhor",
        "data",
        "gonetwork.db",
    )

    # Verificar se o diretório existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    # Conectar ao banco de dados
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Lista de comandos SQL para criar as tabelas
    create_tables_commands = [
        # Tabela de usuários
        """
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
            last_login TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        # Tabela de clientes
        """
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            company TEXT NOT NULL,
            contact_name TEXT,
            email TEXT,
            phone TEXT,
            address TEXT,
            notes TEXT,
            has_access INTEGER DEFAULT 0,
            username TEXT UNIQUE,
            password_hash TEXT,
            access_level TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """,
        # Tabela de membros da equipe
        """
        CREATE TABLE IF NOT EXISTS team_members (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT NOT NULL,
            department TEXT,
            is_active INTEGER DEFAULT 1,
            user_id TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        # Tabela de eventos/projetos
        """
        CREATE TABLE IF NOT EXISTS events (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            location TEXT,
            client_id TEXT,
            status TEXT DEFAULT 'planejamento',
            tags TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        """,
        # Tabela de membros da equipe por evento
        """
        CREATE TABLE IF NOT EXISTS event_team_members (
            event_id TEXT,
            member_id TEXT,
            project_role TEXT,
            created_at TEXT NOT NULL,
            PRIMARY KEY (event_id, member_id),
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (member_id) REFERENCES team_members(id)
        )
        """,
        # Tabela de briefings
        """
        CREATE TABLE IF NOT EXISTS briefings (
            id TEXT PRIMARY KEY,
            event_id TEXT,
            project_name TEXT NOT NULL,
            project_description TEXT,
            target_audience TEXT,
            key_messages TEXT,
            special_requests TEXT,
            deadline TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
        """,
        # Tabela de timeline
        """
        CREATE TABLE IF NOT EXISTS timeline_items (
            id TEXT PRIMARY KEY,
            event_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            responsible_id TEXT,
            status TEXT DEFAULT 'agendado',
            color TEXT DEFAULT 'blue',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (responsible_id) REFERENCES team_members(id)
        )
        """,
        # Tabela de entregas
        """
        CREATE TABLE IF NOT EXISTS deliverables (
            id TEXT PRIMARY KEY,
            event_id TEXT,
            title TEXT NOT NULL,
            type TEXT,
            description TEXT,
            format TEXT,
            resolution TEXT,
            duration TEXT,
            status TEXT DEFAULT 'em produção',
            feedback TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
        """,
        # Tabela de comentários
        """
        CREATE TABLE IF NOT EXISTS comments (
            id TEXT PRIMARY KEY,
            item_id TEXT NOT NULL,
            item_type TEXT NOT NULL,
            content TEXT NOT NULL,
            user_id TEXT,
            timestamp TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        # Tabela de notificações
        """
        CREATE TABLE IF NOT EXISTS notifications (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL,
            read INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """,
        # Tabela de arquivos
        """
        CREATE TABLE IF NOT EXISTS files (
            id TEXT PRIMARY KEY,
            filename TEXT NOT NULL,
            filepath TEXT NOT NULL,
            filetype TEXT,
            filesize INTEGER,
            related_id TEXT,
            related_type TEXT,
            uploaded_by TEXT,
            upload_date TEXT NOT NULL,
            FOREIGN KEY (uploaded_by) REFERENCES users(id)
        )
        """,
    ]

    # Executar cada comando para criar as tabelas
    for command in create_tables_commands:
        cursor.execute(command)

    # Verificar se já existe um usuário admin
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
    admin_count = cursor.fetchone()[0]

    # Se não houver admin, criar um padrão
    if admin_count == 0:
        now = datetime.now().isoformat()
        admin_id = str(uuid.uuid4())

        # Senha padrão: admin123
        cursor.execute(
            """
            INSERT INTO users
            (id, username, password_hash, name, email, role, is_admin, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                admin_id,
                "admin",
                "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",  # SHA-256 de 'admin123'
                "Administrador",
                "admin@gonetwork.com.br",
                "Administrador",
                1,
                now,
                now,
            ),
        )

    # Commit para salvar as alterações
    conn.commit()
    conn.close()

    print(f"[✅] Banco de dados configurado com sucesso em: {db_path}")
    return True


if __name__ == "__main__":
    setup_database()
