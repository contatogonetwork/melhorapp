"""
Script para verificar os dados da aba Edições no banco de dados
"""

import sqlite3


def verificar_dados_edicoes():
    """Verifica os dados da aba Edições no banco de dados"""
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect("database/gonetwork.db")
        cursor = conn.cursor()

        # Verificar edições
        print("\n=== EDIÇÕES ===")
        cursor.execute(
            "SELECT id, event_id, editor_id, title, status, video_path FROM video_edits"
        )
        edicoes = cursor.fetchall()
        if edicoes:
            for edicao in edicoes:
                print(f"ID: {edicao[0]}")
                print(f"Evento: {edicao[1]}")
                print(f"Editor: {edicao[2]}")
                print(f"Título: {edicao[3]}")
                print(f"Status: {edicao[4]}")
                print(f"Vídeo: {edicao[5]}")
                print("-" * 50)
        else:
            print("Nenhuma edição encontrada.")

        # Verificar comentários
        print("\n=== COMENTÁRIOS ===")
        cursor.execute(
            "SELECT id, video_edit_id, user_id, timestamp, comment, is_resolved FROM video_comments"
        )
        comentarios = cursor.fetchall()
        if comentarios:
            for comentario in comentarios:
                print(f"ID: {comentario[0]}")
                print(f"Edição: {comentario[1]}")
                print(f"Usuário: {comentario[2]}")
                print(f"Timestamp: {comentario[3]} ms")
                print(f"Comentário: {comentario[4]}")
                print(f"Resolvido: {'Sim' if comentario[5] else 'Não'}")
                print("-" * 50)
        else:
            print("Nenhum comentário encontrado.")

        # Verificar entregas
        print("\n=== ENTREGAS ===")
        cursor.execute(
            "SELECT id, video_edit_id, asset_refs, is_submitted, approval_status FROM editor_deliveries"
        )
        entregas = cursor.fetchall()
        if entregas:
            for entrega in entregas:
                print(f"ID: {entrega[0]}")
                print(f"Edição: {entrega[1]}")
                print(f"Assets: {entrega[2]}")
                print(f"Submetido: {'Sim' if entrega[3] else 'Não'}")
                print(f"Status: {entrega[4]}")
                print("-" * 50)
        else:
            print("Nenhuma entrega encontrada.")

        conn.close()

    except Exception as e:
        print(f"Erro ao verificar dados: {str(e)}")
        if conn:
            conn.close()


if __name__ == "__main__":
    verificar_dados_edicoes()
