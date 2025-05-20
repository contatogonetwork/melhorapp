#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar índices no banco de dados.

Este script cria índices nas tabelas do banco de dados para melhorar a performance
das consultas mais frequentes.
"""

import os
import sqlite3
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.Database import Database


def create_indices(db: Database) -> bool:
    """
    Cria os índices recomendados para melhorar a performance do banco de dados.

    Args:
        db: Instância da classe Database

    Returns:
        bool: True se todos os índices foram criados com sucesso
    """
    print("[1] Criando índices...")

    # Lista de tabelas e colunas que devem ter índices
    indices = [
        # Tabela events
        {"table": "events", "columns": ["id"], "name": "idx_events_id"},
        {"table": "events", "columns": ["client_id"], "name": "idx_events_client"},
        {"table": "events", "columns": ["start_date"], "name": "idx_events_date"},
        # Tabela team_members
        {"table": "team_members", "columns": ["id"], "name": "idx_team_members_id"},
        {"table": "team_members", "columns": ["role"], "name": "idx_team_members_role"},
        # Tabela clients
        {"table": "clients", "columns": ["id"], "name": "idx_clients_id"},
        {"table": "clients", "columns": ["company"], "name": "idx_clients_company"},
        # Tabela briefings
        {"table": "briefings", "columns": ["event_id"], "name": "idx_briefings_event"},
        # Tabela sponsors
        {
            "table": "sponsors",
            "columns": ["briefing_id"],
            "name": "idx_sponsors_briefing",
        },
        # Tabela sponsor_actions
        {
            "table": "sponsor_actions",
            "columns": ["sponsor_id"],
            "name": "idx_sponsor_actions_sponsor",
        },
        # Tabela stages
        {"table": "stages", "columns": ["briefing_id"], "name": "idx_stages_briefing"},
        # Tabela attractions
        {
            "table": "attractions",
            "columns": ["stage_id"],
            "name": "idx_attractions_stage",
        },
        # Tabela event_team
        {
            "table": "event_team",
            "columns": ["event_id"],
            "name": "idx_event_team_event",
        },
        {
            "table": "event_team",
            "columns": ["team_member_id"],
            "name": "idx_event_team_member",
        },
        {
            "table": "event_team",
            "columns": ["event_id", "team_member_id"],
            "name": "idx_event_team_combined",
        },
        # Tabelas timeline
        {
            "table": "timeline_items",
            "columns": ["event_id"],
            "name": "idx_timeline_items_event",
        },
        {
            "table": "timeline_items",
            "columns": ["responsible_id"],
            "name": "idx_timeline_items_responsible",
        },
        {
            "table": "timeline_items",
            "columns": ["status"],
            "name": "idx_timeline_items_status",
        },
        {
            "table": "timeline_milestones",
            "columns": ["event_id"],
            "name": "idx_timeline_milestones_event",
        },
        {
            "table": "timeline_notifications",
            "columns": ["timeline_item_id"],
            "name": "idx_timeline_notifications_item",
        },
        # Tabelas de vídeos
        {"table": "videos", "columns": ["event_id"], "name": "idx_videos_event"},
        {
            "table": "video_cuts",
            "columns": ["video_id"],
            "name": "idx_video_cuts_video",
        },
        {
            "table": "video_comments",
            "columns": ["video_id"],
            "name": "idx_video_comments_video",
        },
    ]

    success_count = 0

    # Verificar quais tabelas existem antes de criar índices
    tables_query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables_result = db.fetch_all(tables_query)
    existing_tables = [row["name"] for row in tables_result]

    # Verificar quais índices já existem
    indices_query = "SELECT name FROM sqlite_master WHERE type='index'"
    indices_result = db.fetch_all(indices_query)
    existing_indices = [row["name"] for row in indices_result]

    # Criar cada índice
    for index in indices:
        table = index["table"]
        columns = index["columns"]
        name = index["name"]

        # Verificar se a tabela existe
        if table not in existing_tables:
            print(f"  ⚠️ Ignorando índice {name}: tabela {table} não existe")
            continue

        # Verificar se o índice já existe
        if name in existing_indices:
            print(f"  ℹ️ Índice {name} já existe")
            success_count += 1
            continue

        # Criar o índice
        columns_str = ", ".join(columns)
        try:
            query = f"CREATE INDEX {name} ON {table} ({columns_str})"
            db.execute_query(query)
            print(f"  ✓ Índice {name} criado com sucesso")
            success_count += 1
        except Exception as e:
            print(f"  ✗ Falha ao criar índice {name}: {str(e)}")

    return success_count == len(indices)


def analyze_database(db: Database) -> bool:
    """
    Executa o comando ANALYZE do SQLite para atualizar estatísticas.

    Args:
        db: Instância da classe Database

    Returns:
        bool: True se a operação foi concluída com sucesso
    """
    print("\n[2] Atualizando estatísticas do banco de dados...")

    try:
        db.execute_query("ANALYZE")
        print("  ✓ Estatísticas atualizadas com sucesso")
        return True
    except Exception as e:
        print(f"  ✗ Falha ao atualizar estatísticas: {str(e)}")
        return False


def vacuum_database(db: Database) -> bool:
    """
    Executa o comando VACUUM do SQLite para otimizar o armazenamento.

    Args:
        db: Instância da classe Database

    Returns:
        bool: True se a operação foi concluída com sucesso
    """
    print("\n[3] Otimizando armazenamento (VACUUM)...")

    try:
        db.execute_query("VACUUM")
        print("  ✓ Banco de dados otimizado com sucesso")
        return True
    except Exception as e:
        print(f"  ✗ Falha ao otimizar o banco de dados: {str(e)}")
        return False


def main():
    """Função principal para executar a criação de índices e otimizações."""
    print("=" * 60)
    print("CRIAÇÃO DE ÍNDICES E OTIMIZAÇÃO DO BANCO DE DADOS")
    print("=" * 60)

    try:
        db = Database()

        # Criar índices
        indices_ok = create_indices(db)

        # Atualizar estatísticas
        analyze_ok = analyze_database(db)

        # Otimizar armazenamento
        vacuum_ok = vacuum_database(db)

        # Resumo
        print("\n" + "=" * 60)
        print("RESUMO")
        print("=" * 60)
        print(f"Criação de índices: {'✓' if indices_ok else '⚠️ Parcial'}")
        print(f"Atualização de estatísticas: {'✓' if analyze_ok else '✗'}")
        print(f"Otimização de armazenamento: {'✓' if vacuum_ok else '✗'}")

        all_ok = analyze_ok and vacuum_ok  # Não considerar indices_ok como crítico
        print("\nStatus geral:", "✓ OK" if all_ok else "⚠️ Concluído com avisos")

        return 0 if all_ok else 1

    except Exception as e:
        print(f"Erro durante a otimização: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
