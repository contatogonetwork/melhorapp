#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.Database import Database


def list_tables():
    """Lista todas as tabelas no banco de dados"""
    db = Database()

    # Buscar todas as tabelas
    query = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
    tables = db.fetch_all(query)

    print("Tabelas no banco de dados:")
    for table in tables:
        print(f"- {table['name']}")

        # Verificar colunas da tabela
        cols = db.fetch_all(f"PRAGMA table_info({table['name']})")
        print(f"  Colunas: {len(cols)}")

        # Contar registros
        count = db.fetch_one(f"SELECT COUNT(*) as count FROM {table['name']}")
        print(f"  Registros: {count['count']}")
        print()


if __name__ == "__main__":
    list_tables()
