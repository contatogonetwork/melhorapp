"""
Script para criar dados de exemplo para testar a aba "Edições"
"""

import os
import sqlite3
import uuid
from datetime import datetime, timedelta


def criar_dados_edicoes():
    """Cria dados de exemplo para a aba de edições"""
    print("Criando dados de exemplo para a aba 'Edições'...")

    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect("database/gonetwork.db")
        cursor = conn.cursor()

        # 1. Verificar se já existem dados
        cursor.execute("SELECT COUNT(*) FROM video_edits")
        count = cursor.fetchone()[0]
        if count > 0:
            print(f"Já existem {count} edições no banco de dados.")
            return

        # 2. Usar IDs fixos para eventos e editores
        # Criar eventos se necessário
        evento_id1 = "1"  # Usaremos um ID fixo para o primeiro evento
        evento_id2 = "2"  # Usaremos um ID fixo para o segundo evento
        editor_id1 = "1"  # Usaremos um ID fixo para o primeiro editor
        editor_id2 = "2"  # Usaremos um ID fixo para o segundo editor

        # Verificar se os eventos existem
        cursor.execute("SELECT COUNT(*) FROM events WHERE id = ?", (evento_id1,))
        if cursor.fetchone()[0] == 0:
            # Criar evento 1
            cursor.execute(
                """
            INSERT INTO events (id, name, start_date, end_date, location, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    evento_id1,
                    "Festival de Música",
                    datetime.now().strftime("%Y-%m-%d"),
                    (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                    "São Paulo, SP",
                    "Confirmado",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            print("Evento 1 de teste criado.")

        cursor.execute("SELECT COUNT(*) FROM events WHERE id = ?", (evento_id2,))
        if cursor.fetchone()[0] == 0:
            # Criar evento 2
            cursor.execute(
                """
            INSERT INTO events (id, name, start_date, end_date, location, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    evento_id2,
                    "Conferência de Negócios",
                    (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                    (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
                    "Rio de Janeiro, RJ",
                    "Concluído",
                    (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            print("Evento 2 de teste criado.")

        # Verificar se os editores existem
        cursor.execute("SELECT COUNT(*) FROM users WHERE id = ?", (editor_id1,))
        if cursor.fetchone()[0] == 0:
            # Criar editor 1
            cursor.execute(
                """
            INSERT INTO users (id, username, email, password, full_name, role, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    editor_id1,
                    "editor_teste1",
                    "editor1@teste.com",
                    "senha123",
                    "Editor de Teste 1",
                    "editor",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            print("Editor 1 de teste criado.")

        cursor.execute("SELECT COUNT(*) FROM users WHERE id = ?", (editor_id2,))
        if cursor.fetchone()[0] == 0:
            # Criar editor 2
            cursor.execute(
                """
            INSERT INTO users (id, username, email, password, full_name, role, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    editor_id2,
                    "editor_teste2",
                    "editor2@teste.com",
                    "senha123",
                    "Editor de Teste 2",
                    "editor",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            print("Editor 2 de teste criado.")

        # 3. Criar edições de exemplo
        agora = datetime.now()

        # Edição 1 - Em andamento
        edicao1_id = str(uuid.uuid4())
        cursor.execute(
            """
        INSERT INTO video_edits (
            id, event_id, editor_id, title, deadline, style, status, video_path, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                edicao1_id,
                evento_id1,
                editor_id1,
                "Festival de Música - Highlights",
                (agora + timedelta(days=3)).strftime("%Y-%m-%d"),
                "Dinâmico",
                "Em edição",
                "uploads/20250513_2343_Sleek Riviera Logo_simple_compose_01jv6at3t1e0g80czm73q5m66a.mp4",
                agora.strftime("%Y-%m-%d %H:%M:%S"),
                agora.strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        # Adicionar comentários para esta edição
        comentarios = [
            (
                str(uuid.uuid4()),
                edicao1_id,
                editor_id1,
                15000,
                "A transição aqui precisa ser mais suave",
                0,
                agora.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            (
                str(uuid.uuid4()),
                edicao1_id,
                evento_id1,
                45000,
                "Poderia destacar mais o logotipo nesta parte",
                0,
                agora.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            (
                str(uuid.uuid4()),
                edicao1_id,
                editor_id1,
                90000,
                "Aumentar volume da música de fundo",
                1,
                agora.strftime("%Y-%m-%d %H:%M:%S"),
            ),
        ]

        cursor.executemany(
            """
        INSERT INTO video_comments (
            id, video_edit_id, user_id, timestamp, comment, is_resolved, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            comentarios,
        )

        # Edição 2 - Concluída
        edicao2_id = str(uuid.uuid4())
        cursor.execute(
            """
        INSERT INTO video_edits (
            id, event_id, editor_id, title, deadline, style, status, video_path, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                edicao2_id,
                evento_id2,
                editor_id2,
                "Conferência de Negócios - Resumo",
                (agora - timedelta(days=1)).strftime("%Y-%m-%d"),
                "Corporativo",
                "Concluído",
                "uploads/20250513_2343_Sleek Riviera Logo_simple_compose_01jv6at3t1e0g80czm73q5m66a.mp4",
                (agora - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S"),
                agora.strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        # Adicionar entrega para esta edição
        entrega_id = str(uuid.uuid4())
        cursor.execute(
            """
        INSERT INTO editor_deliveries (
            id, video_edit_id, asset_refs, is_submitted, submitted_at, approval_status, created_at, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                entrega_id,
                edicao2_id,
                "uploads/20250513_2343_Sleek Riviera Logo_simple_compose_01jv6at3t1e0g80czm73q5m66a.mp4",
                1,
                agora.strftime("%Y-%m-%d %H:%M:%S"),
                "Aprovado",
                (agora - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S"),
                agora.strftime("%Y-%m-%d %H:%M:%S"),
            ),
        )

        # Confirmar alterações no banco de dados
        conn.commit()
        conn.close()

        print("Dados de exemplo criados com sucesso!")
        print(f"- 2 edições de vídeo")
        print(f"- {len(comentarios)} comentários")
        print(f"- 1 entrega")

    except Exception as e:
        print(f"Erro ao criar dados de exemplo: {str(e)}")
        if conn:
            conn.rollback()
            conn.close()


if __name__ == "__main__":
    criar_dados_edicoes()
