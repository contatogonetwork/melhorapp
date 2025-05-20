import os
import random
import sqlite3
import uuid
from datetime import datetime, timedelta

import streamlit as st


def setup_database_schema():
    """
    Configura o esquema do banco de dados com todas as tabelas necessárias.
    """
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "gonetwork.db",
    )

    # Verificar se o diretório existe
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Criar tabelas se não existirem
        cursor.executescript(
            """
            -- Tabela de usuários do sistema
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
            );

            -- Tabela de membros da equipe
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
            );

            -- Tabela de clientes
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
            );

            -- Tabela de eventos/projetos
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
            );

            -- Tabela de membros da equipe por evento
            CREATE TABLE IF NOT EXISTS event_team_members (
                event_id TEXT,
                member_id TEXT,
                project_role TEXT,
                created_at TEXT NOT NULL,
                PRIMARY KEY (event_id, member_id),
                FOREIGN KEY (event_id) REFERENCES events(id),
                FOREIGN KEY (member_id) REFERENCES team_members(id)
            );

            -- Tabela de entregas
            CREATE TABLE IF NOT EXISTS deliverables (
                id TEXT PRIMARY KEY,
                event_id TEXT,
                title TEXT NOT NULL,
                description TEXT,
                deadline TEXT,
                status TEXT DEFAULT 'não iniciado',
                progress INTEGER DEFAULT 0,
                client_id TEXT,
                responsible_id TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (event_id) REFERENCES events(id),
                FOREIGN KEY (client_id) REFERENCES clients(id),
                FOREIGN KEY (responsible_id) REFERENCES team_members(id)
            );

            -- Tabela de comentários
            CREATE TABLE IF NOT EXISTS comments (
                id TEXT PRIMARY KEY,
                item_id TEXT NOT NULL,
                item_type TEXT NOT NULL,
                content TEXT NOT NULL,
                user_id TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            -- Tabela de arquivos
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
            );
        """
        )

        # Verificar se já existe um usuário admin
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 1")
        admin_count = cursor.fetchone()[0]

        # Se não houver admin, cria um padrão
        if admin_count == 0:
            now = datetime.now().isoformat()
            admin_id = f"usr_{uuid.uuid4().hex[:8]}"

            # Senha padrão: admin123
            cursor.execute(
                """
                INSERT INTO users (id, username, password_hash, name, email, role, is_admin, created_at, updated_at)
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

        return True
    except Exception as e:
        st.error(f"Erro ao configurar banco de dados: {e}")
        return False


def generate_demo_data():
    """
    Gera dados de demonstração para o sistema.
    Útil para testar funcionalidades e demonstrar o sistema.
    """
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "gonetwork.db",
    )

    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Verificar se já existem dados
        cursor.execute("SELECT COUNT(*) FROM clients")
        client_count = cursor.fetchone()[0]

        if client_count > 0:
            return True  # Já existem dados, não precisa gerar novamente

        now = datetime.now().isoformat()

        # Inserir clientes de exemplo
        clients = [
            ("Empresa ABC Ltda.", "João Silva", "joao@abc.com.br", "(11) 98765-4321"),
            ("XYZ Corporação", "Maria Oliveira", "maria@xyz.com", "(21) 91234-5678"),
            (
                "Tech Solutions",
                "Pedro Santos",
                "pedro@techsolutions.com",
                "(31) 99876-5432",
            ),
            ("Creative Media", "Ana Costa", "ana@creativemedia.com", "(41) 98765-4321"),
            (
                "Global Ventures",
                "Carlos Mendes",
                "carlos@globalventures.com",
                "(51) 95555-1234",
            ),
        ]

        client_ids = []
        for client in clients:
            client_id = f"cli_{uuid.uuid4().hex[:8]}"
            client_ids.append(client_id)

            cursor.execute(
                """
                INSERT INTO clients
                (id, company, contact_name, email, phone, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (client_id, client[0], client[1], client[2], client[3], now, now),
            )

        # Inserir membros da equipe de exemplo
        team_roles = [
            ("Diretor", "Produção"),
            ("Cinegrafista", "Produção"),
            ("Editor", "Pós-produção"),
            ("Produtor", "Produção"),
            ("Designer", "Arte"),
            ("Gerente de Projetos", "Administrativo"),
            ("Iluminador", "Produção"),
            ("Sonoplasta", "Produção"),
            ("Roteirista", "Pré-produção"),
            ("Assistente", "Produção"),
        ]

        team_members = [
            (
                "Roberto Almeida",
                "roberto@gonetwork.com",
                "(11) 91234-5678",
                team_roles[0][0],
                team_roles[0][1],
            ),
            (
                "Fernanda Lima",
                "fernanda@gonetwork.com",
                "(11) 98765-4321",
                team_roles[1][0],
                team_roles[1][1],
            ),
            (
                "Marcelo Santos",
                "marcelo@gonetwork.com",
                "(11) 99999-8888",
                team_roles[2][0],
                team_roles[2][1],
            ),
            (
                "Juliana Costa",
                "juliana@gonetwork.com",
                "(11) 97777-6666",
                team_roles[3][0],
                team_roles[3][1],
            ),
            (
                "Gabriel Oliveira",
                "gabriel@gonetwork.com",
                "(11) 96666-5555",
                team_roles[4][0],
                team_roles[4][1],
            ),
            (
                "Camila Rodrigues",
                "camila@gonetwork.com",
                "(11) 95555-4444",
                team_roles[5][0],
                team_roles[5][1],
            ),
            (
                "Lucas Ferreira",
                "lucas@gonetwork.com",
                "(11) 94444-3333",
                team_roles[6][0],
                team_roles[6][1],
            ),
            (
                "Amanda Silva",
                "amanda@gonetwork.com",
                "(11) 93333-2222",
                team_roles[7][0],
                team_roles[7][1],
            ),
            (
                "Bruno Martins",
                "bruno@gonetwork.com",
                "(11) 92222-1111",
                team_roles[8][0],
                team_roles[8][1],
            ),
            (
                "Larissa Pereira",
                "larissa@gonetwork.com",
                "(11) 91111-0000",
                team_roles[9][0],
                team_roles[9][1],
            ),
        ]

        team_member_ids = []
        for member in team_members:
            member_id = f"mem_{uuid.uuid4().hex[:8]}"
            team_member_ids.append(member_id)

            cursor.execute(
                """
                INSERT INTO team_members
                (id, name, email, phone, role, department, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    member_id,
                    member[0],
                    member[1],
                    member[2],
                    member[3],
                    member[4],
                    1,
                    now,
                    now,
                ),
            )

        # Inserir eventos/projetos de exemplo
        projects = [
            (
                "Evento de Lançamento ABC",
                "Lançamento do novo produto da empresa ABC",
                client_ids[0],
                "São Paulo",
            ),
            (
                "Conferência Anual XYZ",
                "Conferência anual da XYZ Corp com palestrantes internacionais",
                client_ids[1],
                "Rio de Janeiro",
            ),
            (
                "Workshop Tech Solutions",
                "Workshop de novas tecnologias",
                client_ids[2],
                "Belo Horizonte",
            ),
            (
                "Campanha Publicitária Creative",
                "Produção de vídeos para campanha publicitária",
                client_ids[3],
                "Curitiba",
            ),
            (
                "Documentário Global",
                "Documentário sobre iniciativas sustentáveis",
                client_ids[4],
                "Porto Alegre",
            ),
            (
                "Treinamento Corporativo ABC",
                "Série de vídeos para treinamento interno",
                client_ids[0],
                "São Paulo",
            ),
            (
                "Feira de Negócios XYZ",
                "Cobertura completa da feira de negócios",
                client_ids[1],
                "Rio de Janeiro",
            ),
        ]

        # Status possíveis
        statuses = ["planejamento", "em andamento", "concluído", "cancelado"]

        # Gerar datas para os projetos (distribuídas nos próximos 3 meses)
        now_date = datetime.now()

        project_ids = []
        for i, project in enumerate(projects):
            project_id = f"proj_{uuid.uuid4().hex[:8]}"
            project_ids.append(project_id)

            # Gerar uma data nos próximos 90 dias
            project_date = now_date + timedelta(days=random.randint(-30, 90))
            project_date_str = project_date.isoformat()

            # Definir status com base na data
            if project_date < now_date:
                status = "concluído" if random.random() < 0.8 else "cancelado"
            elif (project_date - now_date).days < 30:
                status = "em andamento" if random.random() < 0.7 else "planejamento"
            else:
                status = "planejamento"

            # Tags para o projeto
            tags = ",".join(
                random.sample(
                    [
                        "corporativo",
                        "evento",
                        "publicitário",
                        "treinamento",
                        "documentário",
                        "institucional",
                    ],
                    k=random.randint(1, 3),
                )
            )

            cursor.execute(
                """
                INSERT INTO events
                (id, name, description, date, location, client_id, status, tags, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    project_id,
                    project[0],
                    project[1],
                    project_date_str,
                    project[3],
                    project[2],
                    status,
                    tags,
                    now,
                    now,
                ),
            )

            # Associar membros da equipe a cada projeto (entre 3 e 6 membros)
            team_count = random.randint(3, min(6, len(team_member_ids)))
            selected_members = random.sample(team_member_ids, team_count)

            for member_id in selected_members:
                # Buscar o papel da pessoa na equipe
                cursor.execute(
                    "SELECT role FROM team_members WHERE id = ?", (member_id,)
                )
                member_role = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO event_team_members
                    (event_id, member_id, project_role, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (project_id, member_id, member_role, now),
                )

            # Criar entregas para cada projeto (entre 3 e 8 entregas)
            deliverable_count = random.randint(3, 8)

            for j in range(deliverable_count):
                deliverable_id = f"del_{uuid.uuid4().hex[:8]}"

                # Tipos de entregas comuns
                deliverable_types = [
                    "Roteiro",
                    "Filmagem",
                    "Edição",
                    "Finalização",
                    "Revisão",
                    "Aprovação",
                    "Publicação",
                    "Material Gráfico",
                    "Trilha Sonora",
                    "Legendas",
                ]

                title = (
                    f"{deliverable_types[j % len(deliverable_types)]} - {project[0]}"
                )

                # Calcular prazo com base na data do evento
                if status == "concluído":
                    # Para eventos concluídos, prazos no passado
                    deadline = project_date - timedelta(days=random.randint(1, 30))
                elif status == "em andamento":
                    # Para eventos em andamento, alguns prazos no passado, outros no futuro
                    deadline = project_date - timedelta(days=random.randint(-20, 20))
                else:
                    # Para eventos em planejamento, prazos no futuro
                    deadline = project_date - timedelta(days=random.randint(5, 30))

                deadline_str = deadline.isoformat()

                # Definir status da entrega
                if deadline < now_date:
                    del_status = "concluído" if random.random() < 0.8 else "atrasado"
                    progress = (
                        100 if del_status == "concluído" else random.randint(60, 95)
                    )
                else:
                    if status == "em andamento":
                        del_status = random.choice(
                            ["não iniciado", "em andamento", "aguardando"]
                        )
                        progress = (
                            0
                            if del_status == "não iniciado"
                            else random.randint(10, 70)
                        )
                    else:
                        del_status = "não iniciado"
                        progress = 0

                # Atribuir um responsável
                responsible_id = (
                    random.choice(selected_members) if selected_members else None
                )

                cursor.execute(
                    """
                    INSERT INTO deliverables
                    (id, event_id, title, description, deadline, status, progress,
                     client_id, responsible_id, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        deliverable_id,
                        project_id,
                        title,
                        f"Descrição para {title}",
                        deadline_str,
                        del_status,
                        progress,
                        project[2],  # client_id
                        responsible_id,
                        now,
                        now,
                    ),
                )

                # Adicionar alguns comentários
                if random.random() < 0.5:
                    comment_count = random.randint(0, 3)
                    for k in range(comment_count):
                        comment_id = f"com_{uuid.uuid4().hex[:8]}"
                        comment_date = now_date - timedelta(
                            days=random.randint(1, 10), hours=random.randint(1, 23)
                        )

                        cursor.execute(
                            """
                            INSERT INTO comments
                            (id, item_id, item_type, content, user_id, timestamp)
                            VALUES (?, ?, ?, ?, ?, ?)
                            """,
                            (
                                comment_id,
                                deliverable_id,
                                "deliverable",
                                f"Comentário de exemplo #{k+1} para esta entrega.",
                                random.choice(team_member_ids),
                                comment_date.isoformat(),
                            ),
                        )

        conn.commit()
        conn.close()

        return True
    except Exception as e:
        st.error(f"Erro ao gerar dados de demonstração: {e}")
        return False


def initialize_database():
    """
    Inicializa o banco de dados com esquema e dados de demonstração.
    """
    schema_ok = setup_database_schema()
    if not schema_ok:
        return False

    demo_ok = generate_demo_data()
    if not demo_ok:
        return False

    return True
