import os
import sqlite3


def check_database():
    db_path = os.path.join("C:\\melhor", "data", "gonetwork.db")

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Obter a lista de tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        print("Tabelas encontradas:", tables)

        # Para cada tabela, listar suas colunas
        for table in tables:
            try:
                cursor.execute(f"PRAGMA table_info({table});")
                columns = [row[1] for row in cursor.fetchall()]
                print(f"Colunas da tabela {table}: {columns}")
            except Exception as e:
                print(f"Erro ao obter colunas da tabela {table}: {e}")

        conn.close()
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")


if __name__ == "__main__":
    check_database()
