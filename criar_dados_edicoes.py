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

        # 2. Buscar IDs de eventos e editores existentes
        cursor.execute("SELECT id FROM events LIMIT 3")
        eventos = cursor.fetchall()

        cursor.execute("SELECT id FROM users WHERE role = 'editor' LIMIT 2")
        editores = cursor.fetchall()

        if not eventos or not editores:
            print("Não foram encontrados eventos ou editores no banco de dados.")
            print(
                "Execute primeiro o script setup_database.py para criar dados básicos."
            )
            return

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
                eventos[0][0],
                editores[0][0],
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
                editores[0][0],
                15000,
                "A transição aqui precisa ser mais suave",
                0,
                agora.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            (
                str(uuid.uuid4()),
                edicao1_id,
                eventos[0][0],
                45000,
                "Poderia destacar mais o logotipo nesta parte",
                0,
                agora.strftime("%Y-%m-%d %H:%M:%S"),
            ),
            (
                str(uuid.uuid4()),
                edicao1_id,
                editores[0][0],
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
                eventos[1][0],
                editores[1][0],
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
        print(f"- {count+2} edições de vídeo")
        print(f"- {len(comentarios)} comentários")
        print(f"- 1 entrega")

    except Exception as e:
        print(f"Erro ao criar dados de exemplo: {str(e)}")
        conn.rollback()
        conn.close()


if __name__ == "__main__":
    criar_dados_edicoes()
