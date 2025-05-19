#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para criar as tabelas do banco de dados para as abas Briefing e Timeline
"""

import os
import sqlite3
import sys

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.Database import Database


def create_tables():
    """Cria as tabelas necessárias para as abas Briefing e Timeline"""

    db = Database()

    print("\n[1] Criando tabelas para a aba Briefing...")

    # Ler e executar o script SQL de briefing
    briefing_sql_path = os.path.join(
        "database", "schema", "briefing_tables.sql"
    )

    if os.path.exists(briefing_sql_path):
        with open(briefing_sql_path, "r", encoding="utf-8") as sql_file:
            sql_script = sql_file.read()

            try:
                db.execute_query(sql_script)
                print("  ✓ Tabelas de Briefing criadas com sucesso!")
            except sqlite3.Error as e:
                print(f"  ✗ Erro ao criar tabelas de Briefing: {e}")
    else:
        print(f"  ✗ Arquivo SQL não encontrado: {briefing_sql_path}")

    print("\n[2] Criando tabelas para a aba Timeline...")

    # Ler e executar o script SQL de timeline
    timeline_sql_path = os.path.join(
        "database", "schema", "timeline_events.sql"
    )

    if os.path.exists(timeline_sql_path):
        with open(timeline_sql_path, "r", encoding="utf-8") as sql_file:
            sql_script = sql_file.read()

            try:
                db.execute_query(sql_script)
                print("  ✓ Tabelas de Timeline criadas com sucesso!")
            except sqlite3.Error as e:
                print(f"  ✗ Erro ao criar tabelas de Timeline: {e}")
    else:
        print(f"  ✗ Arquivo SQL não encontrado: {timeline_sql_path}")


def verify_tables():
    """Verifica se as tabelas foram criadas corretamente"""

    db = Database()

    print("\n[3] Verificando tabelas criadas...")

    tables = [
        # Tabelas de Briefing
        "briefings",
        "sponsors",
        "sponsor_actions",
        "stages",
        "attractions",
        "realtime_deliveries",
        "post_deliveries",
        # Tabelas de Timeline
        "timeline_items",
        "timeline_milestones",
        "timeline_notifications",
        "timeline_history",
    ]

    for table in tables:
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = db.fetch_one(query, (table,))

        if result:
            print(f"  ✓ Tabela '{table}' encontrada")
        else:
            print(f"  ✗ Tabela '{table}' NÃO encontrada")


if __name__ == "__main__":
    print("=" * 60)
    print("CRIAÇÃO DE TABELAS PARA BRIEFING E TIMELINE")
    print("=" * 60)

    create_tables()
    verify_tables()

    print("\n" + "=" * 60)
    print("PROCESSO CONCLUÍDO")
    print("=" * 60)
