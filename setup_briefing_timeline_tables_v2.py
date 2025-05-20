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


def execute_sql_file(filepath, db):
    """
    Executa um arquivo SQL linha por linha

    Args:
        filepath: Caminho para o arquivo SQL
        db: Instância da classe Database

    Returns:
        bool: True se executado com sucesso
    """
    if not os.path.exists(filepath):
        print(f"  ✗ Arquivo SQL não encontrado: {filepath}")
        return False

    try:
        with open(filepath, "r", encoding="utf-8") as sql_file:
            # Lê o conteúdo completo
            sql_script = sql_file.read()

            # Divide em declarações individuais
            statements = sql_script.split(";")

            for statement in statements:
                statement = statement.strip()
                if statement:  # Ignora declarações vazias
                    try:
                        db.execute_query(statement + ";")
                    except sqlite3.Error as e:
                        if "already exists" not in str(e):
                            print(f"  ⚠️  Aviso ao executar: {e}")

            return True

    except Exception as e:
        print(f"  ✗ Erro ao processar arquivo SQL: {e}")
        return False


def create_tables():
    """Cria as tabelas necessárias para as abas Briefing e Timeline"""

    db = Database()

    print("\n[1] Criando tabelas para a aba Briefing...")
    briefing_sql_path = os.path.join("database", "schema", "briefing_tables.sql")

    if execute_sql_file(briefing_sql_path, db):
        print("  ✓ Tabelas de Briefing criadas com sucesso!")
    else:
        print("  ✗ Falha ao criar tabelas de Briefing")

    print("\n[2] Criando tabelas para a aba Timeline...")
    timeline_sql_path = os.path.join("database", "schema", "timeline_events.sql")

    if execute_sql_file(timeline_sql_path, db):
        print("  ✓ Tabelas de Timeline criadas com sucesso!")
    else:
        print("  ✗ Falha ao criar tabelas de Timeline")


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
