#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar a tabela event_team e associar membros aos eventos
"""

import os
import random
import sys
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.Database import Database

def create_event_team_table():
    """Cria a tabela event_team e popula com dados de exemplo"""
    db = Database()
    
    print("Criando tabela event_team...")
    
    # Criar a tabela event_team
    create_sql = """
    CREATE TABLE IF NOT EXISTS event_team (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_id TEXT NOT NULL,
        team_member_id TEXT NOT NULL,
        role TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (event_id) REFERENCES events(id),
        FOREIGN KEY (team_member_id) REFERENCES team_members(id),
        UNIQUE(event_id, team_member_id)
    );
    """
    
    try:
        db.execute_query(create_sql)
        print("Tabela event_team criada com sucesso!")
        
        # Verificar se a tabela existe
        check_sql = "SELECT name FROM sqlite_master WHERE type='table' AND name='event_team'"
        result = db.fetch_one(check_sql)
        if result:
            print("Confirmado: a tabela event_team foi criada e existe no banco de dados.")
        else:
            print("Erro: a tabela event_team não foi encontrada após a criação.")
            return False
        
        return True
    except Exception as e:
        print(f"Erro ao criar a tabela event_team: {e}")
        return False

def associate_team_to_events():
    """Associa membros da equipe aos eventos"""
    db = Database()
    
    # Buscar todos os eventos
    events = db.fetch_all("SELECT id FROM events")
    if not events:
        print("Nenhum evento encontrado para associar membros.")
        return False
    
    # Buscar todos os membros da equipe
    members = db.fetch_all("SELECT id FROM team_members")
    if not members:
        print("Nenhum membro da equipe encontrado para associar a eventos.")
        return False
    
    event_ids = [event['id'] for event in events]
    member_ids = [member['id'] for member in members]
    
    print(f"Encontrados {len(event_ids)} eventos e {len(member_ids)} membros da equipe.")
    
    # Limpar associações anteriores
    try:
        db.execute_query("DELETE FROM event_team")
        print("Associações anteriores removidas.")
    except Exception as e:
        print(f"Aviso ao limpar associações: {e}")
    
    # Associar membros a eventos
    count = 0
    try:
        for event_id in event_ids:
            # Cada evento recebe entre 2 e 5 membros aleatórios da equipe
            num_members = min(random.randint(2, 5), len(member_ids))
            selected_members = random.sample(member_ids, num_members)
            
            for member_id in selected_members:
                # Definir um papel aleatório
                roles = ["Produtor", "Editor", "Fotógrafo", "Diretor", "Assistente"]
                role = random.choice(roles)
                
                # Inserir na tabela event_team
                query = """
                INSERT INTO event_team (event_id, team_member_id, role, created_at)
                VALUES (?, ?, ?, ?)
                """
                db.insert(query, (event_id, member_id, role, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                count += 1
        
        print(f"Criadas {count} associações entre membros e eventos.")
        return True
    except Exception as e:
        print(f"Erro ao associar membros aos eventos: {e}")
        return False

if __name__ == "__main__":
    if create_event_team_table():
        associate_team_to_events()
        print("Processo concluído com sucesso!")
    else:
        print("Não foi possível continuar devido a erros na criação da tabela.")
