from database import Database, EventRepository, TeamRepository, BriefingRepository
from datetime import datetime, timedelta
import random

def generate_sample_data():
    """Gera dados de exemplo para demonstração"""
    
    print("Inicializando banco de dados...")
    db = Database()
    
    # Repositórios
    team_repo = TeamRepository()
    event_repo = EventRepository()
    briefing_repo = BriefingRepository()
    
    # Limpar dados existentes (opcional)
    db.execute_query("DELETE FROM briefings")
    db.execute_query("DELETE FROM events")
    db.execute_query("DELETE FROM team_members")
    db.execute_query("DELETE FROM clients")
    
    print("Gerando dados de amostra...")
    
    # Gerar membros da equipe
    team_members = [
        {"name": "Maria Souza", "role": "Editora de Vídeo", "email": "maria@gonetwork.ai", "contact": "(11) 98765-4321"},
        {"name": "Pedro Alves", "role": "Diretor de Fotografia", "email": "pedro@gonetwork.ai", "contact": "(11) 97654-3210"},
        {"name": "Ana Silva", "role": "Produtora", "email": "ana@gonetwork.ai", "contact": "(11) 96543-2109"},
        {"name": "Carlos Mendes", "role": "Editor de Áudio", "email": "carlos@gonetwork.ai", "contact": "(11) 95432-1098"},
        {"name": "Luciana Santos", "role": "Motion Designer", "email": "luciana@gonetwork.ai", "contact": "(11) 94321-0987"}
    ]
    
    member_ids = []
    for member in team_members:
        member_id = team_repo.create_member(member)
        member_ids.append(member_id)
    
    print(f"Criados {len(member_ids)} membros da equipe")
    
    # Gerar clientes
    clients = [
        {"company": "Empresa ABC", "contact_person": "João Oliveira", "email": "joao@empresaabc.com", "phone": "(11) 3456-7890"},
        {"company": "XYZ Corp", "contact_person": "Fernanda Gomes", "email": "fernanda@xyzcorp.com", "phone": "(11) 2345-6789"},
        {"company": "Tech Solutions", "contact_person": "Ricardo Dias", "email": "ricardo@techsolutions.com", "phone": "(11) 4567-8901"},
        {"company": "Consultoria DEF", "contact_person": "Amanda Cruz", "email": "amanda@def.com.br", "phone": "(11) 5678-9012"},
        {"company": "Associação GHI", "contact_person": "Roberto Lima", "email": "roberto@ghi.org.br", "phone": "(11) 6789-0123"}
    ]
    
    client_ids = []
    for client in clients:
        client_id = team_repo.create_client(client)
        client_ids.append(client_id)
    
    print(f"Criados {len(client_ids)} clientes")
    
    # Gerar eventos
    today = datetime.now()
    event_types = ["Corporativo", "Festival", "Conferência", "Lançamento", "Outro"]
    event_statuses = ["Em planejamento", "Confirmado", "Em andamento", "Concluído", "Cancelado"]
    
    events = [
        {
            "name": "Festival de Música",
            "date": (today + timedelta(days=30)).strftime("%Y-%m-%d"),
            "location": "Arena São Paulo",
            "client_id": client_ids[0],
            "type": "Festival",
            "status": "Em planejamento"
        },
        {
            "name": "Lançamento de Produto",
            "date": (today + timedelta(days=45)).strftime("%Y-%m-%d"),
            "location": "Centro de Convenções",
            "client_id": client_ids[1],
            "type": "Lançamento",
            "status": "Confirmado"
        },
        {
            "name": "Conferência Tech",
            "date": (today + timedelta(days=60)).strftime("%Y-%m-%d"),
            "location": "Hotel Grand",
            "client_id": client_ids[2],
            "type": "Conferência",
            "status": "Em planejamento"
        }
    ]
    
    # Adicionar alguns eventos passados e futuros
    for i in range(5):
        past_date = (today - timedelta(days=random.randint(5, 60))).strftime("%Y-%m-%d")
        future_date = (today + timedelta(days=random.randint(70, 180))).strftime("%Y-%m-%d")
        
        events.append({
            "name": f"Evento Passado {i+1}",
            "date": past_date,
            "location": f"Local {i+1}",
            "client_id": random.choice(client_ids),
            "type": random.choice(event_types),
            "status": random.choice(["Concluído", "Cancelado"])
        })
        
        events.append({
            "name": f"Evento Futuro {i+1}",
            "date": future_date,
            "location": f"Local {i+10}",
            "client_id": random.choice(client_ids),
            "type": random.choice(event_types),
            "status": random.choice(["Em planejamento", "Confirmado"])
        })
    
    event_ids = []
    for event in events:
        event_id = event_repo.create(event)
        event_ids.append(event_id)
    
    print(f"Criados {len(event_ids)} eventos")
    
    # Gerar briefings
    briefing_contents = [
        "Este briefing aborda os detalhes do evento, incluindo público-alvo, mensagens-chave, e cronograma.",
        "Descrição detalhada do projeto, com objetivos, entregáveis e cronograma de produção.",
        "Planejamento completo com requisitos, recursos necessários e prazos para cada etapa.",
        "Documento com especificações técnicas, necessidades de equipamentos e equipe.",
        "Briefing detalhado com planejamento de conteúdo, estratégia e distribuição."
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
            "content": random.choice(briefing_contents)
        }
        
        briefing_repo.create(briefing_data)
    
    print("Criação de dados concluída!")
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    generate_sample_data()