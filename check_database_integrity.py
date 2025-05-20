#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para verificar a integridade do banco de dados.

Este script realiza várias verificações no banco de dados para garantir
que ele esteja consistente e funcionando corretamente:
1. Verifica se todas as tabelas definidas no schema existem
2. Verifica se há chaves estrangeiras danificadas
3. Verifica se há índices ausentes que poderiam melhorar a performance
4. Executa verificações de integridade do SQLite
"""

import os
import sqlite3
import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.Database import Database


def check_tables_existence(db: Database) -> bool:
    """
    Verifica se todas as tabelas esperadas existem.

    Args:
        db: Instância da classe Database

    Returns:
        bool: True se todas as tabelas existirem
    """
    print("\n[1] Verificando existência das tabelas...")

    # Lista de todas as tabelas esperadas
    expected_tables = [
        "users",
        "events",
        "team_members",
        "clients",
        "briefings",
        "sponsors",
        "sponsor_actions",
        "stages",
        "attractions",
        "realtime_deliveries",
        "post_deliveries",
        "event_team",
        "timeline_items",
        "timeline_milestones",
        "timeline_notifications",
        "timeline_history",
        "videos",
        "video_cuts",
        "video_comments",
        "video_tags",
    ]

    query = "SELECT name FROM sqlite_master WHERE type='table'"
    results = db.fetch_all(query)

    existing_tables = [row["name"] for row in results]

    all_tables_exist = True
    for table in expected_tables:
        if table in existing_tables:
            print(f"  ✓ Tabela '{table}' encontrada")
        else:
            print(f"  ✗ Tabela '{table}' NÃO encontrada")
            all_tables_exist = False

    return all_tables_exist


def check_foreign_keys(db: Database) -> bool:
    """
    Verifica se há chaves estrangeiras danificadas.

    Args:
        db: Instância da classe Database

    Returns:
        bool: True se todas as chaves estrangeiras forem válidas
    """
    print("\n[2] Verificando integridade das chaves estrangeiras...")

    try:
        # Ativar verificação de chaves estrangeiras (pode estar desativada por padrão)
        db.execute_query("PRAGMA foreign_key_check;")
        results = db.fetch_all("PRAGMA foreign_key_check;")

        if results:
            print("  ✗ Encontradas chaves estrangeiras danificadas:")
            for row in results:
                print(
                    f"    - Tabela: {row['table']}, Rowid: {row['rowid']}, Parent: {row['parent']}, FK: {row['fkid']}"
                )
            return False
        else:
            print("  ✓ Todas as chaves estrangeiras estão íntegras")
            return True
    except Exception as e:
        print(f"  ✗ Erro ao verificar chaves estrangeiras: {str(e)}")
        return False


def check_missing_indices(db: Database) -> bool:
    """
    Verifica se há índices ausentes que poderiam melhorar a performance.

    Args:
        db: Instância da classe Database

    Returns:
        bool: True se todos os índices recomendados estiverem presentes
    """
    print("\n[3] Verificando índices...")

    # Relações de tabelas e colunas que deveriam ter índices
    recommended_indices = {
        "events": ["id"],
        "team_members": ["id"],
        "clients": ["id"],
        "briefings": ["event_id"],
        "sponsors": ["briefing_id"],
        "sponsor_actions": ["sponsor_id"],
        "stages": ["briefing_id"],
        "attractions": ["stage_id"],
        "event_team": ["event_id", "team_member_id"],
        "timeline_items": ["event_id", "responsible_id"],
        "videos": ["event_id"],
    }

    all_indices_exist = True

    # Obter todos os índices existentes
    indices_query = "SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index'"
    indices_results = db.fetch_all(indices_query)

    # Mapear índices para suas tabelas e colunas
    existing_indices = {}
    for row in indices_results:
        if row["tbl_name"] not in existing_indices:
            existing_indices[row["tbl_name"]] = []

        # Extrair nome das colunas do SQL do índice
        sql = row["sql"]
        if sql:
            # Extrai as colunas do SQL do índice
            try:
                columns = sql.split("(")[1].split(")")[0].replace("`", "").split(",")
                columns = [c.strip() for c in columns]
                existing_indices[row["tbl_name"]].extend(columns)
            except:
                pass

    # Verificar se os índices recomendados existem
    for table, columns in recommended_indices.items():
        for column in columns:
            if table not in existing_indices or column not in existing_indices[table]:
                print(f"  ✗ Índice ausente para {table}.{column}")
                all_indices_exist = False
            else:
                print(f"  ✓ Índice encontrado para {table}.{column}")

    return all_indices_exist


def check_sqlite_integrity(db: Database) -> bool:
    """
    Executa verificações de integridade internas do SQLite.

    Args:
        db: Instância da classe Database

    Returns:
        bool: True se o banco de dados estiver íntegro
    """
    print("\n[4] Executando verificação de integridade do SQLite...")

    try:
        integrity_check = db.fetch_one("PRAGMA integrity_check;")
        if integrity_check and integrity_check["integrity_check"] == "ok":
            print("  ✓ Verificação de integridade do SQLite: OK")
            return True
        else:
            print("  ✗ Verificação de integridade do SQLite falhou")
            return False
    except Exception as e:
        print(f"  ✗ Erro ao verificar integridade do SQLite: {str(e)}")
        return False


def main():
    """Função principal para executar todas as verificações."""
    print("=" * 60)
    print("VERIFICAÇÃO DE INTEGRIDADE DO BANCO DE DADOS")
    print("=" * 60)

    try:
        db = Database()

        # Executar todas as verificações
        tables_ok = check_tables_existence(db)
        fk_ok = check_foreign_keys(db)
        indices_ok = check_missing_indices(db)
        integrity_ok = check_sqlite_integrity(db)

        # Resumo dos resultados
        print("\n" + "=" * 60)
        print("RESUMO")
        print("=" * 60)
        print(f"Tabelas: {'✓' if tables_ok else '✗'}")
        print(f"Chaves Estrangeiras: {'✓' if fk_ok else '✗'}")
        print(f"Índices: {'✓' if indices_ok else '✗'}")
        print(f"Integridade SQLite: {'✓' if integrity_ok else '✗'}")

        all_ok = tables_ok and fk_ok and indices_ok and integrity_ok
        print("\nStatus geral:", "✓ OK" if all_ok else "✗ Problemas encontrados")

        return 0 if all_ok else 1

    except Exception as e:
        print(f"Erro durante a verificação: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
