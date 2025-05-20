"""
Script para gerar dados de exemplo para as tabelas do banco de dados GoNetwork Web
"""

import os
import random
import sqlite3
import uuid
from datetime import datetime, timedelta


def generate_data():
    """Gera dados de exemplo para o banco de dados"""
    db_path = os.path.join("c:\\melhor", "data", "gonetwork.db")

    if not os.path.exists(db_path):
        print(f"[❌] Banco de dados não encontrado em: {db_path}")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Verificar se já existem dados
        print("[ℹ️] Verificando dados existentes...")

        cursor.execute("SELECT COUNT(*) FROM briefings")
        briefings_count = cursor.fetchone()[0]
        print(f"  - Briefings: {briefings_count}")

        cursor.execute("SELECT COUNT(*) FROM timeline_items")
        timeline_count = cursor.fetchone()[0]
        print(f"  - Timeline: {timeline_count}")

        cursor.execute("SELECT COUNT(*) FROM deliverables")
        deliverables_count = cursor.fetchone()[0]
        print(f"  - Deliverables: {deliverables_count}")

        # Criar dados faltantes
        if briefings_count == 0:
            print("[ℹ️] Gerando briefings...")
            generate_briefings(cursor)

        if timeline_count == 0:
            print("[ℹ️] Gerando timeline...")
            generate_timeline(cursor)

        if deliverables_count == 0:
            print("[ℹ️] Gerando deliverables...")
            generate_deliverables(cursor)

        conn.commit()
        conn.close()

        print("[✅] Dados gerados com sucesso!")
        return True

    except Exception as e:
        conn.close()
        print(f"[❌] Erro: {e}")
        return False


def generate_briefings(cursor):
    """Gera dados de exemplo para a tabela de briefings"""
    # Verificar se existem eventos
    cursor.execute("SELECT id, name FROM events")
    events = cursor.fetchall()

    if not events:
        print("  - Não há eventos para associar briefings")
        return

    # Verificar se existem clientes
    cursor.execute("SELECT id FROM clients")
    client_ids = cursor.fetchall()
    client_ids = [c[0] for c in client_ids] if client_ids else None

    # Verificar se existem membros da equipe
    cursor.execute("SELECT id FROM team_members")
    team_ids = cursor.fetchall()
    team_ids = [t[0] for t in team_ids] if team_ids else None

    # Criar briefings para cada evento
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for event_id, event_name in events:
        # Escolher aleatoriamente um cliente e um líder de equipe
        client_id = random.choice(client_ids) if client_ids else None
        team_lead_id = random.choice(team_ids) if team_ids else None

        # Definir data de entrega (entre 10 e 30 dias a partir de agora)
        delivery_date = (
            datetime.now() + timedelta(days=random.randint(10, 30))
        ).strftime("%Y-%m-%d")

        # Conteúdo do briefing
        content = f"""# Briefing para {event_name}

## Descrição
Este é o briefing para o projeto {event_name}.

## Requisitos
- Vídeo com alta qualidade
- Legendas em português e inglês
- Duração máxima de 8 minutos

## Público-alvo
Profissionais da área, faixa etária 25-45 anos

## Mensagens-chave
1. Inovação
2. Qualidade
3. Excelência"""

        # Inserir no banco de dados
        cursor.execute(
            """
            INSERT INTO briefings
            (id, event_id, project_name, client_id, delivery_date, team_lead_id, content, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                random.randint(100, 9999),
                event_id,
                f"Briefing - {event_name}",
                client_id,
                delivery_date,
                team_lead_id,
                content,
                now,
                now,
            ),
        )

    print(f"  - {len(events)} briefings criados")


def generate_timeline(cursor):
    """Gera dados de exemplo para a tabela de timeline"""
    # Verificar se existem eventos
    cursor.execute("SELECT id, name, date FROM events")
    events = cursor.fetchall()

    if not events:
        print("  - Não há eventos para adicionar à timeline")
        return

    # Verificar se existem membros da equipe
    cursor.execute("SELECT id FROM team_members")
    team_ids = cursor.fetchall()
    team_ids = [t[0] for t in team_ids] if team_ids else None

    # Criar itens de timeline para cada evento
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = 0

    for event_id, event_name, event_date in events:
        # Calcular datas com base na data do evento
        try:
            base_date = datetime.fromisoformat(event_date)
        except (ValueError, TypeError):
            try:
                base_date = datetime.strptime(event_date, "%Y-%m-%d")
            except (ValueError, TypeError):
                # Se não conseguir parsear a data, usar a data atual
                base_date = datetime.now()

        # Definir atividades para a timeline
        activities = [
            (
                "Pré-produção",
                -15,
                -10,
                "Preparação inicial para o evento",
                "Reunião",
                1,
                "blue",
            ),
            ("Roteiro", -10, -7, "Desenvolvimento do roteiro", "Tarefa", 2, "green"),
            ("Filmagem", -2, 0, "Captação de imagens no evento", "Tarefa", 3, "red"),
            (
                "Edição preliminar",
                1,
                3,
                "Primeira versão da edição",
                "Tarefa",
                2,
                "orange",
            ),
            (
                "Revisão com cliente",
                4,
                4,
                "Apresentação para aprovação",
                "Reunião",
                1,
                "purple",
            ),
            ("Finalização", 5, 7, "Ajustes finais da edição", "Tarefa", 2, "green"),
            ("Entrega", 8, 8, "Entrega final do material", "Milestone", 3, "blue"),
        ]

        for activity in activities:
            title, start_offset, end_offset, description, task_type, priority, color = (
                activity
            )

            # Calcular datas de início e fim
            start_time = (base_date + timedelta(days=start_offset)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            end_time = (base_date + timedelta(days=end_offset)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            # Selecionar um membro aleatório da equipe como responsável
            responsible_id = random.choice(team_ids) if team_ids else None

            # Status baseado nas datas (para simular progresso)
            today = datetime.now()
            if base_date + timedelta(days=end_offset) < today:
                status = "concluído"
            elif (
                base_date + timedelta(days=start_offset)
                <= today
                <= base_date + timedelta(days=end_offset)
            ):
                status = "em andamento"
            else:
                status = "agendado"

            # Local da atividade
            location = "Escritório GoNetwork" if "Reunião" in task_type else event_name

            # Dependências (para alguns itens)
            dependencies = "" if random.random() < 0.7 else "1,2"

            # Inserir no banco de dados
            cursor.execute(
                """
                INSERT INTO timeline_items
                (id, event_id, title, description, start_time, end_time, responsible_id,
                task_type, status, priority, color, dependencies, location, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    str(uuid.uuid4()),
                    event_id,
                    title,
                    description,
                    start_time,
                    end_time,
                    responsible_id,
                    task_type,
                    status,
                    priority,
                    color,
                    dependencies,
                    location,
                    now,
                    now,
                ),
            )
            count += 1

    print(f"  - {count} itens de timeline criados")


def generate_deliverables(cursor):
    """Gera dados de exemplo para a tabela de deliverables"""
    # Verificar se existem eventos
    cursor.execute("SELECT id, name FROM events")
    events = cursor.fetchall()

    if not events:
        print("  - Não há eventos para adicionar deliverables")
        return

    # Verificar se existem clientes
    cursor.execute("SELECT id FROM clients")
    client_ids = cursor.fetchall()
    client_ids = [c[0] for c in client_ids] if client_ids else None

    # Criar deliverables para cada evento
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    count = 0

    for event_id, event_name in events:
        # Tipo de entregas para cada evento
        deliverables = [
            (f"Vídeo principal - {event_name}", 75),
            (f"Teaser para redes sociais - {event_name}", 100),
            (f"Highlights do evento - {event_name}", 50),
            (f"Entrevistas editadas - {event_name}", 25),
            (f"Pacote de fotos - {event_name}", 90),
        ]

        # Escolher cliente aleatório
        client_id = random.choice(client_ids) if client_ids else None

        # Data limite (entre 5 e 15 dias a partir de agora)
        deadline = (datetime.now() + timedelta(days=random.randint(5, 15))).strftime(
            "%Y-%m-%d"
        )

        for title, progress in deliverables:
            # Definir status baseado no progresso
            if progress == 100:
                status = "concluído"
            elif progress >= 75:
                status = "revisão"
            elif progress >= 25:
                status = "em produção"
            else:
                status = "não iniciado"

            # Inserir no banco de dados
            cursor.execute(
                """
                INSERT INTO deliverables
                (id, title, event_id, client_id, deadline, status, progress, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    random.randint(100, 9999),
                    title,
                    event_id,
                    client_id,
                    deadline,
                    status,
                    progress,
                    now,
                    now,
                ),
            )
            count += 1

    print(f"  - {count} deliverables criados")


if __name__ == "__main__":
    generate_data()
