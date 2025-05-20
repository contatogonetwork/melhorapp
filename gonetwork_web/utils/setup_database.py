import os
import sqlite3

import streamlit as st


def initialize_database(db_path=None):
    """
    Inicializa o banco de dados, criando as tabelas necessárias se não existirem.

    Args:
        db_path: Caminho para o arquivo do banco de dados

    Returns:
        bool: True se a inicialização foi bem-sucedida
    """
    if db_path is None:
        # Caminho padrão para o banco de dados
        db_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "data",
            "gonetwork.db",
        )

    # Verificar se o diretório existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Tabelas principais para o sistema web
        tables = [
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
            """
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY,
                client_id TEXT,
                name TEXT NOT NULL,
                description TEXT,
                date TEXT NOT NULL,
                location TEXT,
                status TEXT DEFAULT 'pending',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (client_id) REFERENCES clients (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS team_members (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                role TEXT,
                email TEXT,
                phone TEXT,
                username TEXT UNIQUE,
                password_hash TEXT,
                access_level TEXT DEFAULT 'editor',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS event_team_members (
                id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                member_id TEXT NOT NULL,
                role TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events (id),
                FOREIGN KEY (member_id) REFERENCES team_members (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS briefings (
                id TEXT PRIMARY KEY,
                project_name TEXT NOT NULL,
                event_id TEXT,
                client_id TEXT,
                team_lead_id TEXT,
                content TEXT,
                delivery_date TEXT,
                requirements TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events (id),
                FOREIGN KEY (client_id) REFERENCES clients (id),
                FOREIGN KEY (team_lead_id) REFERENCES team_members (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS timeline_items (
                id TEXT PRIMARY KEY,
                event_id TEXT NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                responsible_id TEXT,
                location TEXT,
                status TEXT DEFAULT 'scheduled',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events (id),
                FOREIGN KEY (responsible_id) REFERENCES team_members (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS deliverables (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                event_id TEXT,
                client_id TEXT,
                responsible_id TEXT,
                deadline TEXT,
                status TEXT DEFAULT 'pending',
                progress INTEGER DEFAULT 0,
                content_path TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events (id),
                FOREIGN KEY (client_id) REFERENCES clients (id),
                FOREIGN KEY (responsible_id) REFERENCES team_members (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY,
                item_id TEXT NOT NULL,
                item_type TEXT NOT NULL,
                user_id TEXT,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                resolved INTEGER DEFAULT 0,
                parent_id TEXT,
                FOREIGN KEY (user_id) REFERENCES team_members (id),
                FOREIGN KEY (parent_id) REFERENCES comments (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id TEXT PRIMARY KEY,
                theme TEXT DEFAULT 'light',
                font_size INTEGER DEFAULT 14,
                notifications INTEGER DEFAULT 1,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES team_members (id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                title TEXT NOT NULL,
                content TEXT,
                type TEXT DEFAULT 'info',
                read INTEGER DEFAULT 0,
                created_at TEXT NOT NULL,
                expire_at TEXT,
                FOREIGN KEY (user_id) REFERENCES team_members (id)
            )
            """,
        ]

        # Executar a criação de cada tabela
        for table_sql in tables:
            cursor.execute(table_sql)

        # Criar índices para melhorar a performance
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_events_client ON events (client_id)",
            "CREATE INDEX IF NOT EXISTS idx_briefings_event ON briefings (event_id)",
            "CREATE INDEX IF NOT EXISTS idx_timeline_event ON timeline_items (event_id)",
            "CREATE INDEX IF NOT EXISTS idx_deliverables_event ON deliverables (event_id)",
            "CREATE INDEX IF NOT EXISTS idx_deliverables_client ON deliverables (client_id)",
            "CREATE INDEX IF NOT EXISTS idx_comments_item ON comments (item_id, item_type)",
            "CREATE INDEX IF NOT EXISTS idx_event_team ON event_team_members (event_id, member_id)",
        ]

        for index_sql in indexes:
            cursor.execute(index_sql)

        conn.commit()
        conn.close()

        return True
    except sqlite3.Error as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        return False


def create_demo_data(db_path=None):
    """
    Cria dados de demonstração no banco de dados.
    Útil para testes e demonstração do sistema.

    Args:
        db_path: Caminho para o arquivo do banco de dados

    Returns:
        bool: True se a criação foi bem-sucedida
    """
    if db_path is None:
        # Caminho padrão para o banco de dados
        db_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "data",
            "gonetwork.db",
        )

    import uuid
    from datetime import datetime, timedelta

    # Gerar timestamps
    now = datetime.now().isoformat()
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    tomorrow = (datetime.now() + timedelta(days=1)).isoformat()
    next_week = (datetime.now() + timedelta(days=7)).isoformat()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar se já existem dados
        cursor.execute("SELECT COUNT(*) FROM clients")
        client_count = cursor.fetchone()[0]

        if client_count > 0:
            # Já existem dados no banco
            conn.close()
            return False

        # Inserir clientes de demonstração
        clientes = [
            (
                str(uuid.uuid4()),
                "TechCorp Brasil",
                "Carlos Silva",
                "carlos@techcorp.com",
                "(11) 98765-4321",
                "Av. Paulista, 1000, São Paulo, SP",
                "Cliente desde 2023",
                1,  # has_access
                "techcorp",
                "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # "admin" em SHA-256
                "Visualização",
                now,
                now,
            ),
            (
                str(uuid.uuid4()),
                "EventBR",
                "Ana Rodrigues",
                "ana@eventbr.com.br",
                "(21) 97654-3210",
                "Rua Copacabana, 500, Rio de Janeiro, RJ",
                "Especialistas em eventos corporativos",
                0,  # has_access
                None,
                None,
                None,
                now,
                now,
            ),
            (
                str(uuid.uuid4()),
                "Mídia Digital",
                "Pedro Mendes",
                "pedro@midiadigital.net",
                "(31) 96543-2109",
                "Av. Brasil, 2500, Belo Horizonte, MG",
                "Foco em marketing digital",
                1,  # has_access
                "midia",
                "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb",  # "user" em SHA-256
                "Comentários",
                now,
                now,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO clients (id, company, contact_name, email, phone, address, notes,
                               has_access, username, password_hash, access_level, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            clientes,
        )

        # Guardar IDs para referências
        client_ids = [c[0] for c in clientes]

        # Inserir membros da equipe
        membros = [
            (
                str(uuid.uuid4()),
                "Maria Oliveira",
                "Editor Sênior",
                "maria@gonetwork.com",
                "(11) 91234-5678",
                "maria",
                "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918",  # "admin" em SHA-256
                "admin",
                now,
                now,
            ),
            (
                str(uuid.uuid4()),
                "João Santos",
                "Cinegrafista",
                "joao@gonetwork.com",
                "(11) 92345-6789",
                "joao",
                "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb",  # "user" em SHA-256
                "editor",
                now,
                now,
            ),
            (
                str(uuid.uuid4()),
                "Luciana Ferreira",
                "Diretora",
                "luciana@gonetwork.com",
                "(11) 93456-7890",
                "luciana",
                "04f8996da763b7a969b1028ee3007569eaf3a635486ddab211d512c85b9df8fb",  # "user" em SHA-256
                "editor",
                now,
                now,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO team_members (id, name, role, email, phone, username, password_hash,
                                    access_level, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            membros,
        )

        # Guardar IDs para referências
        member_ids = [m[0] for m in membros]

        # Inserir eventos
        eventos = [
            (
                str(uuid.uuid4()),
                client_ids[0],
                "Lançamento de Produto",
                "Lançamento do novo produto TechX",
                tomorrow,
                "Centro de Convenções, São Paulo, SP",
                "in_progress",
                yesterday,
                now,
            ),
            (
                str(uuid.uuid4()),
                client_ids[1],
                "Congresso Anual",
                "Congresso de Tecnologia EventBR",
                next_week,
                "Centro de Convenções, Rio de Janeiro, RJ",
                "pending",
                now,
                now,
            ),
            (
                str(uuid.uuid4()),
                client_ids[2],
                "Workshop de Marketing",
                "Workshop sobre estratégias de marketing digital",
                yesterday,
                "Hotel Business, Belo Horizonte, MG",
                "completed",
                (datetime.now() - timedelta(days=10)).isoformat(),
                yesterday,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO events (id, client_id, name, description, date, location,
                              status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            eventos,
        )

        # Guardar IDs para referências
        event_ids = [e[0] for e in eventos]

        # Associar membros da equipe aos eventos
        event_members = [
            (str(uuid.uuid4()), event_ids[0], member_ids[0], "Coordenadora", now),
            (str(uuid.uuid4()), event_ids[0], member_ids[1], "Cinegrafista", now),
            (str(uuid.uuid4()), event_ids[1], member_ids[0], "Diretora", now),
            (str(uuid.uuid4()), event_ids[1], member_ids[2], "Editora", now),
            (str(uuid.uuid4()), event_ids[2], member_ids[1], "Cinegrafista", now),
        ]

        cursor.executemany(
            """
            INSERT INTO event_team_members (id, event_id, member_id, role, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            event_members,
        )

        # Inserir briefings
        briefings = [
            (
                str(uuid.uuid4()),
                "Lançamento TechX",
                event_ids[0],
                client_ids[0],
                member_ids[0],
                """
                # Briefing do Lançamento do TechX

                ## Objetivo
                Documentar o lançamento do novo produto TechX.

                ## Entregas Esperadas
                - Vídeo de 5 minutos com os destaques
                - 30 fotos editadas
                - Entrevistas com executivos
                """,
                tomorrow,
                "Foco nos aspectos inovadores do produto",
                yesterday,
                now,
            ),
            (
                str(uuid.uuid4()),
                "Congresso EventBR",
                event_ids[1],
                client_ids[1],
                member_ids[2],
                """
                # Briefing do Congresso Anual

                ## Objetivo
                Cobertura completa do evento com transmissão ao vivo.

                ## Entregas Esperadas
                - Transmissão ao vivo
                - Vídeos resumo por dia
                - Highlights para redes sociais
                """,
                next_week,
                "Cobertura multimídia completa",
                now,
                now,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO briefings (id, project_name, event_id, client_id, team_lead_id,
                                 content, delivery_date, requirements, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            briefings,
        )

        # Inserir itens da timeline
        timeline_items = [
            (
                str(uuid.uuid4()),
                event_ids[0],
                "Chegada da equipe",
                "Chegada e montagem de equipamentos",
                (datetime.fromisoformat(tomorrow) - timedelta(hours=2)).isoformat(),
                (datetime.fromisoformat(tomorrow) - timedelta(hours=1)).isoformat(),
                member_ids[1],
                "Entrada de serviço",
                "scheduled",
                now,
                now,
            ),
            (
                str(uuid.uuid4()),
                event_ids[0],
                "Entrevista com CEO",
                "Entrevista exclusiva com CEO antes do evento",
                (datetime.fromisoformat(tomorrow) - timedelta(minutes=30)).isoformat(),
                datetime.fromisoformat(tomorrow).isoformat(),
                member_ids[0],
                "Sala VIP",
                "scheduled",
                now,
                now,
            ),
            (
                str(uuid.uuid4()),
                event_ids[0],
                "Apresentação do Produto",
                "Gravação da apresentação principal",
                datetime.fromisoformat(tomorrow).isoformat(),
                (datetime.fromisoformat(tomorrow) + timedelta(hours=1)).isoformat(),
                member_ids[1],
                "Auditório Principal",
                "scheduled",
                now,
                now,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO timeline_items (id, event_id, title, description, start_time, end_time,
                                      responsible_id, location, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            timeline_items,
        )

        # Inserir entregas/deliverables
        deliverables = [
            (
                str(uuid.uuid4()),
                "Vídeo - TechX - Apresentação Principal",
                "Edição da apresentação do produto com destaques",
                event_ids[0],
                client_ids[0],
                member_ids[0],
                (datetime.now() + timedelta(days=2)).isoformat(),
                "in_progress",
                30,
                None,
                yesterday,
                now,
            ),
            (
                str(uuid.uuid4()),
                "Vídeo - Entrevista com CEO TechCorp",
                "Edição da entrevista com o CEO",
                event_ids[0],
                client_ids[0],
                member_ids[2],
                (datetime.now() + timedelta(days=3)).isoformat(),
                "pending",
                0,
                None,
                now,
                now,
            ),
            (
                str(uuid.uuid4()),
                "Vídeo - Workshop Marketing Digital - Resumo",
                "Resumo das principais palestras",
                event_ids[2],
                client_ids[2],
                member_ids[2],
                (datetime.now() - timedelta(days=1)).isoformat(),
                "completed",
                100,
                "data/uploads/example_video.mp4",
                (datetime.now() - timedelta(days=5)).isoformat(),
                yesterday,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO deliverables (id, title, description, event_id, client_id, responsible_id,
                                     deadline, status, progress, content_path, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            deliverables,
        )

        # Guardar IDs para referências
        deliverable_ids = [d[0] for d in deliverables]

        # Inserir comentários
        comments = [
            (
                str(uuid.uuid4()),
                deliverable_ids[0],
                "deliverable",
                member_ids[0],
                "Favor destacar os recursos inovadores mencionados aos 15 minutos",
                yesterday,
                0,
                None,
            ),
            (
                str(uuid.uuid4()),
                deliverable_ids[0],
                "deliverable",
                client_ids[0],
                "O logo da empresa precisa estar mais visível na abertura",
                now,
                0,
                None,
            ),
            (
                str(uuid.uuid4()),
                deliverable_ids[2],
                "deliverable",
                client_ids[2],
                "Aprovado! Excelente trabalho na edição final.",
                (datetime.now() - timedelta(days=2)).isoformat(),
                1,
                None,
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO comments (id, item_id, item_type, user_id, content,
                                timestamp, resolved, parent_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            comments,
        )

        conn.commit()
        conn.close()

        return True
    except sqlite3.Error as e:
        print(f"Erro ao criar dados de demonstração: {e}")
        if conn:
            conn.close()
        return False


def verify_database():
    """
    Verifica se o banco de dados existe e tem as tabelas necessárias.

    Returns:
        bool: True se o banco de dados está configurado corretamente
    """
    # Caminho padrão para o banco de dados
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "data",
        "gonetwork.db",
    )

    if not os.path.exists(db_path):
        return False

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar as tabelas mínimas necessárias
        essential_tables = [
            "clients",
            "events",
            "team_members",
            "briefings",
            "timeline_items",
            "deliverables",
            "comments",
        ]

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing_tables = [row[0] for row in cursor.fetchall()]

        conn.close()

        # Retorna True se todas as tabelas essenciais existirem
        return all(table in existing_tables for table in essential_tables)
    except sqlite3.Error:
        return False


if __name__ == "__main__":
    # Se executado diretamente, inicializa o banco de dados
    if initialize_database():
        print("Banco de dados inicializado com sucesso!")

        # Perguntar se deseja criar dados de demonstração
        import sys

        if len(sys.argv) > 1 and sys.argv[1] == "--with-demo-data":
            create_demo_data()
            print("Dados de demonstração criados com sucesso!")
    else:
        print("Erro ao inicializar banco de dados.")
