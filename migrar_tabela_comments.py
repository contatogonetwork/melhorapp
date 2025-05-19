import datetime
import sqlite3


def migrar_video_comments():
    """
    Migra a tabela video_comments para o novo esquema com is_resolved e video_edit_id
    """
    print("Iniciando migração da tabela video_comments...")

    # Conectar ao banco de dados
    conn = sqlite3.connect("database/gonetwork.db")
    cursor = conn.cursor()

    try:
        # 1. Verificar se existe conteúdo na tabela atual
        cursor.execute("SELECT COUNT(*) FROM video_comments")
        count = cursor.fetchone()[0]
        print(f"Número de comentários na tabela antiga: {count}")

        if count > 0:
            # 2. Fazer backup dos dados existentes
            print("Fazendo backup dos dados existentes...")
            cursor.execute("SELECT * FROM video_comments")
            comentarios_existentes = cursor.fetchall()

            # 3. Renomear a tabela atual
            print("Renomeando tabela atual...")
            cursor.execute(
                "ALTER TABLE video_comments RENAME TO video_comments_old"
            )

            # 4. Criar a nova tabela com o esquema correto
            print("Criando nova tabela com esquema atualizado...")
            cursor.execute(
                """
            CREATE TABLE video_comments (
                id TEXT PRIMARY KEY,
                video_edit_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                comment TEXT NOT NULL,
                is_resolved INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (video_edit_id) REFERENCES video_edits(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            )

            # 5. Migrar os dados antigos para o novo formato
            print("Migrando dados para o novo esquema...")
            for comentario in comentarios_existentes:
                (
                    old_id,
                    video_id,
                    user_id,
                    comment_text,
                    timestamp_str,
                    created_at,
                ) = comentario

                # Converter timestamp de formato MM:SS para milissegundos
                try:
                    minutos, segundos = timestamp_str.split(":")
                    timestamp_ms = (int(minutos) * 60 + int(segundos)) * 1000
                except Exception:
                    timestamp_ms = 0

                # Inserir na nova tabela
                cursor.execute(
                    """
                INSERT INTO video_comments (
                    id, video_edit_id, user_id, timestamp, comment, is_resolved, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                    (
                        str(old_id),
                        str(video_id),
                        str(user_id),
                        timestamp_ms,
                        comment_text,
                        0,  # Todos os comentários começam como não resolvidos
                        created_at
                        or datetime.datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),
                    ),
                )

            # 6. Remover tabela antiga
            print("Removendo tabela antiga...")
            cursor.execute("DROP TABLE video_comments_old")

        else:
            # Se não houver dados, apenas recriar a tabela
            print("Nenhum dado existente, recriando tabela...")
            cursor.execute("DROP TABLE video_comments")
            cursor.execute(
                """
            CREATE TABLE video_comments (
                id TEXT PRIMARY KEY,
                video_edit_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                comment TEXT NOT NULL,
                is_resolved INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (video_edit_id) REFERENCES video_edits(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
            )

        # 7. Confirmar alterações
        conn.commit()
        print("Migração concluída com sucesso!")

    except Exception as e:
        conn.rollback()
        print(f"Erro durante a migração: {str(e)}")

    finally:
        conn.close()


if __name__ == "__main__":
    migrar_video_comments()

    # Verificar resultado da migração
    try:
        conn = sqlite3.connect("database/gonetwork.db")
        cursor = conn.cursor()

        # Verificar estrutura
        cursor.execute("PRAGMA table_info(video_comments)")
        columns = cursor.fetchall()

        print("\nNova estrutura da tabela:")
        for col in columns:
            print(
                f"  {col[1]} ({col[2]}){' PRIMARY KEY' if col[5] == 1 else ''}"
            )

        # Verificar dados
        cursor.execute("SELECT COUNT(*) FROM video_comments")
        count = cursor.fetchone()[0]
        print(f"\nTotal de comentários na nova tabela: {count}")

        if count > 0:
            cursor.execute("SELECT * FROM video_comments LIMIT 5")
            rows = cursor.fetchall()
            print("\nPrimeiros registros:")
            for row in rows:
                print(f"  {row}")

        conn.close()

    except Exception as e:
        print(f"Erro ao verificar migração: {str(e)}")
