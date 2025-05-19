import sqlite3


def verificar_tabela(tabela):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect("database/gonetwork.db")
        cursor = conn.cursor()

        # Verificar estrutura da tabela
        cursor.execute(f"PRAGMA table_info({tabela})")
        columns = cursor.fetchall()

        print(f"\nEstrutura da tabela '{tabela}':")
        for col in columns:
            print(
                f"  {col[0]}: {col[1]} ({col[2]}){' PRIMARY KEY' if col[5] == 1 else ''}"
            )

        # Verificar conteúdo da tabela
        cursor.execute(f"SELECT * FROM {tabela} LIMIT 10")
        rows = cursor.fetchall()

        print(f"\nConteúdo da tabela '{tabela}' (até 10 registros):")
        for row in rows:
            print(f"  {row}")

        conn.close()

    except Exception as e:
        print(f"Erro: {str(e)}")


if __name__ == "__main__":
    tabela = input("Digite o nome da tabela a verificar: ")
    verificar_tabela(tabela)
