"""
Funções para criar dados de exemplo para a aplicação web GoNetwork.
Usado principalmente para demonstração e desenvolvimento.
"""

import os
import random
import sqlite3
import uuid
from datetime import datetime, timedelta


def init_sample_data():
    """
    Inicializa dados de exemplo no banco de dados.
    Verifica primeiro se já existem dados antes de inserir.
    """
    db_path = os.path.join(
        "c:\\melhor",
        "data",
        "gonetwork.db",
    )

    if not os.path.exists(db_path):
        print(f"Banco de dados não encontrado em: {db_path}")
        return False    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Verificar se as tabelas estão vazias
        cursor.execute("SELECT COUNT(*) FROM briefings")
        briefings_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM timeline_items")
        timeline_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM deliverables")
        deliverables_count = cursor.fetchone()[0]

        # Verificar se alguma tabela importante está vazia
        if briefings_count == 0 or timeline_count == 0 or deliverables_count == 0:
            # Criar dados de exemplo para as tabelas vazias
            cursor.execute("SELECT COUNT(*) FROM clients")
            client_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM team_members")
            team_count = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM events")
            event_count = cursor.fetchone()[0]

            if client_count == 0:
                create_sample_clients(cursor)
                print("[✅] Criados dados de exemplo para clientes")

            if team_count == 0:
                create_sample_team_members(cursor)
                print("[✅] Criados dados de exemplo para membros da equipe")

            if event_count == 0:
                create_sample_events(cursor)
                print("[✅] Criados dados de exemplo para eventos")

            if briefings_count == 0:
                create_sample_briefings(cursor)
                print("[✅] Criados dados de exemplo para briefings")

            if timeline_count == 0:
                create_sample_timeline(cursor)
                print("[✅] Criados dados de exemplo para timeline")

            if deliverables_count == 0:
                create_sample_deliverables(cursor)
                print("[✅] Criados dados de exemplo para entregas")

            conn.commit()
            print("[✅] Dados de exemplo criados com sucesso!")
        else:
            print("[ℹ️] Todas as tabelas já possuem dados. Pulando criação.")

        conn.close()
        return True

    except Exception as e:
        print(f"[❌] Erro ao criar dados de exemplo: {e}")
        return False


def create_sample_clients(cursor):
    """Criar clientes de exemplo"""
    current_time = datetime.now().isoformat()

    clients = [
        (
            "MegaCorp",
            "João Silva",
            "joao@megacorp.com",
            "(11) 98765-4321",
            "São Paulo, SP",
            "Cliente premium",
        ),
        (
            "TechSolutions",
            "Maria Oliveira",
            "maria@techsolutions.com",
            "(21) 91234-5678",
            "Rio de Janeiro, RJ",
            "Novo cliente",
        ),
        (
            "InoveMarketing",
            "Carlos Santos",
            "carlos@inove.com",
            "(31) 99876-5432",
            "Belo Horizonte, MG",
            "",
        ),
        (
            "NaturaBrasil",
            "Fernanda Lima",
            "fernanda@natura.com",
            "(41) 95555-1234",
            "Curitiba, PR",
            "Cliente antigo",
        ),
        (
            "GoNextGen",
            "Paulo Mendes",
            "paulo@gonextgen.com",
            "(51) 94444-9876",
            "Porto Alegre, RS",
            "Parceiro estratégico",
        ),
    ]

    for client in clients:
        client_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO clients
            (id, company, contact_name, email, phone, address, notes, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (client_id, *client, current_time, current_time),
        )


def create_sample_team_members(cursor):
    """Criar membros da equipe de exemplo"""
    current_time = datetime.now().isoformat()

    members = [
        (
            "Ana Souza",
            "ana@gonetwork.com.br",
            "(11) 97777-8888",
            "Editor Chefe",
            "Edição",
        ),
        (
            "Pedro Costa",
            "pedro@gonetwork.com.br",
            "(11) 96666-9999",
            "Cinegrafista",
            "Produção",
        ),
        (
            "Lúcia Ferreira",
            "lucia@gonetwork.com.br",
            "(11) 95555-7777",
            "Roteirista",
            "Criação",
        ),
        (
            "Marcos Silva",
            "marcos@gonetwork.com.br",
            "(11) 94444-5555",
            "Editor",
            "Edição",
        ),
        (
            "Juliana Matos",
            "juliana@gonetwork.com.br",
            "(11) 93333-4444",
            "Diretor",
            "Produção",
        ),
        (
            "Rodrigo Lima",
            "rodrigo@gonetwork.com.br",
            "(11) 92222-3333",
            "Social Media",
            "Marketing",
        ),
    ]

    for member in members:
        member_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO team_members
            (id, name, email, phone, role, department, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
            """,
            (member_id, *member, current_time, current_time),
        )


def create_sample_events(cursor):
    """Criar eventos/projetos de exemplo"""
    current_time = datetime.now().isoformat()

    # Obter IDs dos clientes
    cursor.execute("SELECT id FROM clients")
    client_ids = [row[0] for row in cursor.fetchall()]

    # Eventos com datas próximas (para timeline)
    events = [
        (
            "Lançamento Produto X",
            "Cobertura completa do evento de lançamento",
            (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
            "Centro de Convenções ABC",
            random.choice(client_ids),
            "planejamento",
            "lançamento,produto,evento",
        ),
        (
            "Entrevista CEO",
            "Entrevista exclusiva com o CEO",
            (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "Sede da Empresa",
            random.choice(client_ids),
            "confirmado",
            "entrevista,executivo",
        ),
        (
            "Workshop Marketing",
            "Workshop sobre estratégias digitais",
            (datetime.now() + timedelta(days=12)).strftime("%Y-%m-%d"),
            "Hotel Continental",
            random.choice(client_ids),
            "orçamento",
            "workshop,marketing,treinamento",
        ),
        (
            "Feira de Tecnologia",
            "Cobertura da feira anual de tecnologia",
            (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
            "Expo Center Norte",
            random.choice(client_ids),
            "confirmado",
            "feira,tecnologia,cobertura",
        ),
        (
            "Campanha Institucional",
            "Produção de vídeo institucional",
            (datetime.now() + timedelta(days=20)).strftime("%Y-%m-%d"),
            "Estúdio Principal",
            random.choice(client_ids),
            "em andamento",
            "institucional,marca,campanha",
        ),
    ]

    for event in events:
        event_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO events
            (id, name, description, date, location, client_id, status, tags, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (event_id, *event, current_time, current_time),
        )

        # Associar membros da equipe a este evento
        associate_team_to_event(cursor, event_id, current_time)


def associate_team_to_event(cursor, event_id, current_time):
    """Associa membros da equipe aleatórios a um evento"""
    cursor.execute("SELECT id FROM team_members")
    team_ids = [row[0] for row in cursor.fetchall()]

    # Selecionar até 3 membros aleatórios para o evento
    selected_members = random.sample(team_ids, min(3, len(team_ids)))

    roles = ["Diretor", "Cinegrafista", "Editor", "Roteirista"]

    for member_id in selected_members:
        cursor.execute(
            """
            INSERT INTO event_team_members
            (event_id, member_id, project_role, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (event_id, member_id, random.choice(roles), current_time),
        )


def create_sample_briefings(cursor):
    """Criar briefings de exemplo para os eventos"""
    current_time = datetime.now().isoformat()

    cursor.execute("SELECT id FROM events")
    event_ids = [row[0] for row in cursor.fetchall()]

    for event_id in event_ids:
        # Obter informações do evento
        cursor.execute("SELECT name, client_id FROM events WHERE id = ?", (event_id,))
        event_name, client_id = cursor.fetchone()

        briefing_id = str(uuid.uuid4())

        # Criar o briefing
        cursor.execute(
            """
            INSERT INTO briefings
            (id, event_id, project_name, project_description, target_audience,
             key_messages, special_requests, deadline, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                briefing_id,
                event_id,
                f"Briefing - {event_name}",
                f"Descrição detalhada do projeto {event_name}",
                "Profissionais da área, faixa etária 25-45 anos",
                "Inovação, Qualidade, Excelência",
                "Legenda em inglês, alta qualidade",
                (datetime.now() + timedelta(days=random.randint(10, 30))).strftime(
                    "%Y-%m-%d"
                ),
                current_time,
                current_time,
            ),
        )


def create_sample_timeline(cursor):
    """Criar itens de timeline para os eventos"""
    current_time = datetime.now().isoformat()

    cursor.execute("SELECT id, date FROM events")
    events = cursor.fetchall()

    cursor.execute("SELECT id FROM team_members")
    team_ids = [row[0] for row in cursor.fetchall()]

    for event_id, event_date in events:
        # Converter para datetime
        try:
            base_date = datetime.fromisoformat(event_date)
        except ValueError:
            base_date = datetime.strptime(event_date, "%Y-%m-%d")

        # Adicionar algumas atividades na timeline para este evento
        activities = [
            (
                "Pré-produção",
                timedelta(days=-10),
                timedelta(days=-8),
                "Planejamento inicial do projeto",
            ),
            (
                "Produção de roteiro",
                timedelta(days=-7),
                timedelta(days=-5),
                "Desenvolvimento do roteiro e storyboard",
            ),
            (
                "Captação de imagens",
                timedelta(days=-2),
                timedelta(days=0),
                "Filmagem no local do evento",
            ),
            (
                "Edição inicial",
                timedelta(days=1),
                timedelta(days=3),
                "Primeiro corte da edição",
            ),
            (
                "Revisão com cliente",
                timedelta(days=4),
                timedelta(days=4),
                "Apresentação do material para aprovação",
            ),
            (
                "Edição final",
                timedelta(days=5),
                timedelta(days=7),
                "Finalização após feedback",
            ),
            (
                "Entrega",
                timedelta(days=8),
                timedelta(days=8),
                "Entrega do material final",
            ),
        ]

        for title, start_offset, end_offset, description in activities:
            start_time = (base_date + start_offset).isoformat()
            end_time = (base_date + end_offset).isoformat()

            timeline_id = str(uuid.uuid4())
            responsible_id = random.choice(team_ids) if team_ids else None

            cursor.execute(
                """
                INSERT INTO timeline_items
                (id, event_id, title, description, start_time, end_time,
                 responsible_id, status, color, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    timeline_id,
                    event_id,
                    title,
                    description,
                    start_time,
                    end_time,
                    responsible_id,
                    random.choice(
                        ["agendado", "concluído", "em andamento", "atrasado"]
                    ),
                    random.choice(["blue", "green", "orange", "red", "purple"]),
                    current_time,
                    current_time,
                ),
            )


def create_sample_deliverables(cursor):
    """Criar entregas de conteúdo para os eventos"""
    current_time = datetime.now().isoformat()

    cursor.execute("SELECT id, name FROM events")
    events = cursor.fetchall()

    for event_id, event_name in events:
        # Criar diferentes tipos de entregas para cada evento
        deliverables = [
            (
                f"Vídeo principal - {event_name}",
                "video",
                "Material principal editado",
                "mp4",
                "1920x1080",
                "5-8 minutos",
            ),
            (
                f"Teaser - {event_name}",
                "video",
                "Teaser para redes sociais",
                "mp4",
                "1080x1080",
                "30-45 segundos",
            ),
            (
                f"Highlights - {event_name}",
                "video",
                "Melhores momentos",
                "mp4",
                "1920x1080",
                "2-3 minutos",
            ),
            (
                f"Entrevista - {event_name}",
                "video",
                "Entrevista com participantes",
                "mp4",
                "1920x1080",
                "3-5 minutos",
            ),
            (
                f"Fotos - {event_name}",
                "imagem",
                "Seleção das melhores fotos",
                "jpg",
                "N/A",
                "25-30 imagens",
            ),
        ]

        for title, type_, description, format_, resolution, duration in deliverables:
            deliverable_id = str(uuid.uuid4())

            cursor.execute(
                """
                INSERT INTO deliverables
                (id, event_id, title, type, description, format, resolution, duration,
                 status, feedback, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    deliverable_id,
                    event_id,
                    title,
                    type_,
                    description,
                    format_,
                    resolution,
                    duration,
                    random.choice(["em produção", "revisão", "aprovado", "entregue"]),
                    "",
                    current_time,
                    current_time,
                ),
            )


if __name__ == "__main__":
    init_sample_data()
