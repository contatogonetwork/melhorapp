"""
Script de diagnóstico para testar os componentes da aba "Edições"
"""

import os
import sys
import traceback

from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow

# Configurar saída para mostrar erros completos
sys.stdout.reconfigure(encoding="utf-8")
print("Iniciando diagnóstico da aba Edições...")


def verificar_módulos_aba_edicoes():
    print("=== Verificando módulos da aba 'Edições' ===\n")

    # Lista de módulos para verificar
    módulos = [
        "database.models.comment_model",
        "database.CommentRepository",
        "database.VideoRepository",
        "gui.widgets.player_component",
        "gui.widgets.comment_item",
        "gui.widgets.comment_marker_widget",
        "gui.widgets.version_info_widget",
        "utils.exporters",
    ]

    for módulo in módulos:
        try:
            __import__(módulo)
            print(f"✅ Módulo {módulo} importado com sucesso")
        except Exception as e:
            print(f"❌ Erro ao importar {módulo}: {str(e)}")

    # Verificar classes específicas
    print("\n=== Verificando classes ===\n")

    try:
        from database.models.comment_model import Comment

        print(f"✅ Classe Comment importada com sucesso")
        comment = Comment(
            id="test",
            text="Comentário teste",
            author="Teste",
            video_timestamp=5000,
        )
        print(f"✅ Instância de Comment criada: {comment.to_dict()}")
    except Exception as e:
        print(f"❌ Erro ao usar classe Comment: {str(e)}")

    try:
        from database.CommentRepository import CommentRepository

        print(f"✅ Classe CommentRepository importada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar CommentRepository: {str(e)}")

    try:
        from gui.widgets.player_component import VideoPlayerComponent

        print(f"✅ Classe VideoPlayerComponent importada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar VideoPlayerComponent: {str(e)}")

    try:
        from gui.widgets.comment_item import CommentItem

        print(f"✅ Classe CommentItem importada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar CommentItem: {str(e)}")

    try:
        from utils.exporters import CommentExporter

        print(f"✅ Classe CommentExporter importada com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar CommentExporter: {str(e)}")


def testar_player_component():
    print("\n=== Testando VideoPlayerComponent ===\n")

    try:
        app = QApplication(sys.argv)

        from gui.widgets.player_component import VideoPlayerComponent

        # Criando um player de teste
        player = VideoPlayerComponent()

        # Verificar se os sinais estão configurados
        signals = [attr for attr in dir(player) if attr.endswith("Signal")]
        print(f"Sinais disponíveis: {signals}")

        # Testar método importante
        print("Testando métodos:")
        player.setPlaybackRate(1.0)
        position = player.getCurrentTime()
        print(f"Posição atual: {position}")
        tempo_formatado = player.formatTime(5000)
        print(f"Formatação de tempo (5000ms): {tempo_formatado}")

        print("✅ Player testado com sucesso")

    except Exception as e:
        print(f"❌ Erro ao testar VideoPlayerComponent: {str(e)}")

    # Não executar o event loop do QApplication
    del app


def testar_exportacao_comentarios():
    print("\n=== Testando exportação de comentários ===\n")

    try:
        from database.models.comment_model import Comment
        from utils.exporters import CommentExporter

        # Criar dados de teste
        comment1 = Comment(
            id="1",
            text="Este é um comentário de teste",
            author="Usuário Teste",
            timestamp="2025-05-19 14:00:00",
            video_timestamp=15000,
            is_resolved=False,
        )

        comment2 = Comment(
            id="2",
            text="Este é outro comentário resolvido",
            author="Usuário Teste 2",
            timestamp="2025-05-19 14:05:00",
            video_timestamp=45000,
            is_resolved=True,
        )

        comments = [comment1, comment2]  # Testar exportação para JSON
        try:
            json_file = os.path.join(os.getcwd(), "temp_export_test.json")
            print(f"Tentando exportar para: {json_file}")
            result_json = CommentExporter.export_to_json(comments, json_file)
            if result_json:
                print(f"✅ Exportação para JSON bem-sucedida: {json_file}")
                if os.path.exists(json_file):
                    os.remove(json_file)
                    print("   Arquivo JSON temporário removido.")
            else:
                print("❌ Falha na exportação para JSON")
        except Exception as e:
            print(f"❌ Erro na exportação para JSON: {str(e)}")
        # Testar exportação para PDF se a biblioteca estiver disponível
        # Comentando este bloco para evitar erros
        """
        try:
            import reportlab
            pdf_file = "temp_export_test.pdf"
            result_pdf = CommentExporter.export_to_pdf(comments, pdf_file)
            if result_pdf:
                print(f"✅ Exportação para PDF bem-sucedida: {pdf_file}")
                if os.path.exists(pdf_file):
                    os.remove(pdf_file)
                    print("   Arquivo PDF temporário removido.")
            else:
                print("❌ Falha na exportação para PDF")
        except ImportError:
            print("⚠️ Biblioteca ReportLab não encontrada. Teste de PDF ignorado.")
        """
        print("ℹ️ Teste de exportação PDF desabilitado")

    except Exception as e:
        print(f"❌ Erro ao testar exportação: {str(e)}")


if __name__ == "__main__":
    verificar_módulos_aba_edicoes()
    testar_player_component()
    testar_exportacao_comentarios()
