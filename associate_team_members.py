#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import random
import sys
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.Database import Database


def associate_members():
    db = Database()

    # Buscar IDs de eventos
    print("Buscando eventos...")
    events = db.fetch_all("SELECT id FROM events")
    if not events:
        print("Nenhum evento encontrado.")
        return False

    # Buscar IDs de membros da equipe
    print("Buscando membros da equipe...")
    members = db.fetch_all("SELECT id FROM team_members")
    if not members:
        print("Nenhum membro encontrado.")
        return False

    event_ids = [e["id"] for e in events]
    member_ids = [m["id"] for m in members]

    print(f"Encontrados {len(event_ids)} eventos e {len(member_ids)} membros.")

    # Limpar tabela existente
    print("Limpando dados existentes...")
    try:
        db.execute_query("DELETE FROM event_team")
    except Exception as e:
        print(f"Erro ao limpar dados: {e}")

    # Associar membros aos eventos
    count = 0
    print("Associando membros aos eventos...")
    for event_id in event_ids:
        # Selecionar 2-3 membros aleatoriamente
        num_members = min(3, len(member_ids))
        selected_members = random.sample(member_ids, num_members)

        for member_id in selected_members:
            # Papel aleatório
            role = random.choice(["Editor", "Produtor", "Fotógrafo"])

            # Inserir na tabela
            query = "INSERT INTO event_team (event_id, team_member_id, role) VALUES (?, ?, ?)"
            db.insert(query, (event_id, member_id, role))
            count += 1

    print(f"Associados {count} membros aos eventos com sucesso!")
    return True


if __name__ == "__main__":
    associate_members()
