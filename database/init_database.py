import os
import random
import sys
from datetime import datetime, timedelta

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.BriefingRepository import BriefingRepository
from database.Database import Database
from database.EventRepository import EventRepository
from database.TeamRepository import TeamRepository


def generate_sample_data():
    """Gera dados de exemplo para demonstração"""

    print("Inicializando banco de dados...")
    db = Database()

    # Repositórios
    team_repo = TeamRepository()
    event_repo = EventRepository()
    briefing_repo = BriefingRepository()

    # Criar a tabela event_team se não existir
    try:
        sql_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'schema',
            'event_team.sql'
        )
        with open(sql_file_path, 'r') as sql_file:
            sql_script = sql_file.read()
            db.execute_query(sql_script)
        print("Tabela event_team criada com sucesso")
    except Exception as e:
        print(f"Erro ao criar tabela event_team: {e}")

    # Limpar dados existentes (opcional)
    try:
        db.execute_query("DELETE FROM event_team")
    except Exception as e:
        print(f"Nota: Tabela event_team ainda não existe: {e}")

    db.execute_query("DELETE FROM briefings")
    db.execute_query("DELETE FROM events")
    db.execute_query("DELETE FROM team_members")
    db.execute_query("DELETE FROM clients")

    print("Gerando dados de amostra...")

    # Gerar membros da equipe
    team_members = [
        {
            "name": "Maria Souza",
            "role": "Editora de Vídeo",
            "email": "maria@gonetwork.ai",
            "contact": "(11) 98765-4321",
        },
        {
            "name": "Pedro Alves",
            "role": "Diretor de Fotografia",
            "email": "pedro@gonetwork.ai",
            "contact": "(11) 97654-3210",
        },
        {
            "name": "Ana Silva",
            "role": "Produtora",
            "email": "ana@gonetwork.ai",
            "contact": "(11) 96543-2109",
        },
        {
            "name": "João Santos",
            "role": "Editor Sênior",
            "email": "joao@gonetwork.ai",
            "contact": "(11) 95432-1098",
        },
        {
            "name": "Fernanda Lima",
            "role": "Diretora de Arte",
            "email": "fernanda@gonetwork.ai",
            "contact": "(11) 94321-0987",
        },
    ]

    member_ids = []
    for member in team_members:
        member_id = team_repo.create_member(member)
        member_ids.append(member_id)

    print(f"Criados {len(member_ids)} membros da equipe")

    # Gerar clientes
    clients = [
        {
            "company": "Tech Solutions",
            "contact_person": "Roberto Mendes",
            "email": "roberto@techsolutions.com",
            "phone": "(11) 3456-7890",
        },
        {
            "company": "Eventos Especiais",
            "contact_person": "Carla Dias",
            "email": "carla@eventosespeciais.com",
            "phone": "(11) 2345-6789",
        },
        {
            "company": "Marketing Digital",
            "contact_person": "Lucas Ferreira",
            "email": "lucas@marketingdigital.com",
            "phone": "(11) 1234-5678",
        },
    ]

    client_ids = []
    for client in clients:
        client_id = team_repo.create_client(client)
        client_ids.append(client_id)

    print(f"Criados {len(client_ids)} clientes")

    # Gerar eventos
    today = datetime.now()
    event_types = ["Conferência", "Festival", "Lançamento", "Show", "Corporativo"]

    events = [
        {
            "name": "Festival de Música",
            "date": (today + timedelta(days=30)).strftime("%Y-%m-%d"),
            "location": "Arena São Paulo",
            "client_id": client_ids[0],
            "type": "Festival",
            "status": "Em planejamento",
        },
        {
            "name": "Lançamento de Produto",
            "date": (today + timedelta(days=45)).strftime("%Y-%m-%d"),
            "location": "Centro de Convenções",
            "client_id": client_ids[1],
            "type": "Lançamento",
            "status": "Confirmado",
        },
        {
            "name": "Conferência Tech",
            "date": (today + timedelta(days=60)).strftime("%Y-%m-%d"),
            "location": "Hotel Grand",
            "client_id": client_ids[2],
            "type": "Conferência",
            "status": "Em planejamento",
        },
    ]

    # Adicionar alguns eventos passados e futuros
    for i in range(5):
        past_date = (today - timedelta(days=random.randint(5, 60))).strftime(
            "%Y-%m-%d"
        )
        future_date = (
            today + timedelta(days=random.randint(70, 180))
        ).strftime("%Y-%m-%d")

        events.append(
            {
                "name": f"Evento Passado {i+1}",
                "date": past_date,
                "location": f"Local {i+1}",
                "client_id": random.choice(client_ids),
                "type": random.choice(event_types),
                "status": random.choice(["Concluído", "Cancelado"]),
            }
        )

        events.append(
            {
                "name": f"Evento Futuro {i+1}",
                "date": future_date,
                "location": f"Local {i+10}",
                "client_id": random.choice(client_ids),
                "type": random.choice(event_types),
                "status": random.choice(["Em planejamento", "Confirmado"]),
            }
        )

    event_ids = []
    for event in events:
        event_id = event_repo.create(event)
        event_ids.append(event_id)

    print(f"Criados {len(event_ids)} eventos")

    # Associar membros da equipe aos eventos (event_team)
    print("Associando membros da equipe aos eventos...")

    for event_id in event_ids:
        # Cada evento recebe entre 2 e 5 membros aleatórios da equipe
        selected_members = random.sample(member_ids, random.randint(2, min(5, len(member_ids))))

        for member_id in selected_members:
            # Inserir na tabela event_team
            query = """
            INSERT INTO event_team (event_id, team_member_id, role, created_at)
            VALUES (?, ?, ?, ?)
            """

            # Definir um papel aleatório para o membro no evento
            roles = ["Produtor", "Editor", "Fotógrafo", "Diretor", "Assistente"]
            role = random.choice(roles)

            db.insert(query, (event_id, member_id, role, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    print("Membros da equipe associados aos eventos com sucesso!")

    # Gerar briefings
    briefing_contents = [
        "Este briefing aborda os detalhes do evento, incluindo público-alvo, mensagens-chave, e cronograma.",
        "Descrição detalhada do projeto, com objetivos, entregáveis e cronograma de produção.",
        "Planejamento completo com requisitos, recursos necessários e prazos para cada etapa.",
        "Documento com especificações técnicas, necessidades de equipamentos e equipe.",
        "Briefing detalhado com planejamento de conteúdo, estratégia e distribuição.",
    ]

    for i in range(len(event_ids)):
        event_id = event_ids[i]
        client_id = events[i]["client_id"]

        briefing_data = {
            "event_id": event_id,
            "project_name": f"Briefing - {events[i]['name']}",
            "client_id": client_id,
            "delivery_date": events[i]["date"],
            "team_lead_id": random.choice(member_ids),
            "content": random.choice(briefing_contents),
        }

        briefing_repo.create(briefing_data)

    print("Criação de dados concluída!")
    print("Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    generate_sample_data()
