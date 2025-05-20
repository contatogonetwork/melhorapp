import os
import sqlite3
import sys


def verificar_tabelas_edicoes():
    try:
        # Verificar ambos os caminhos possíveis para o banco de dados
        db_paths = [
            os.path.join("database", "gonetwork.db"),
            os.path.join("data", "gonetwork.db"),
        ]

        conn = None

        # Tentar conectar a qualquer um dos bancos de dados
        for db_path in db_paths:
            if os.path.exists(db_path):
                print(f"Conectando ao banco de dados: {db_path}")
                conn = sqlite3.connect(db_path)
                break

        if conn is None:
            print("ERRO: Nenhum banco de dados encontrado!")
            return

        cursor = conn.cursor()

        # Verificar as tabelas da aba de edições
        tabelas = ["video_edits", "video_comments", "editor_deliveries"]

        print("\n=== Verificação das tabelas de edição ===")
        for tabela in tabelas:
            # Verificar se a tabela existe
            cursor.execute(
                f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{tabela}';"
            )
            existe = cursor.fetchone()[0] > 0

            if existe:
                print(f"\n✅ Tabela '{tabela}' ENCONTRADA")

                # Listar estrutura da tabela
                cursor.execute(f"PRAGMA table_info({tabela});")
                colunas = cursor.fetchall()
                print(f"  Estrutura da tabela '{tabela}':")
                for col in colunas:
                    print(
                        f"    - {col[1]} ({col[2]}){' PRIMARY KEY' if col[5] == 1 else ''}"
                    )

                # Contar registros
                cursor.execute(f"SELECT count(*) FROM {tabela}")
                count = cursor.fetchone()[0]
                print(f"  Número de registros: {count}")

                # Mostrar amostra de dados se houver registros
                if count > 0:
                    cursor.execute(f"SELECT * FROM {tabela} LIMIT 5")
                    rows = cursor.fetchall()
                    print(f"  Amostra de dados (até 5 registros):")
                    for row in rows:
                        print(f"    {row}")
            else:
                print(f"\n❌ Tabela '{tabela}' NÃO ENCONTRADA")

        conn.close()

    except Exception as e:
        print(f"Erro ao verificar tabelas de edição: {str(e)}")
        if conn:
            conn.close()


if __name__ == "__main__":
    print("Verificando tabelas relacionadas à aba de Edições...")
    verificar_tabelas_edicoes()
