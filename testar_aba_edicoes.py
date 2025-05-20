"""
Script para testar a aba de Edições no aplicativo GoNetwork AI
"""

import datetime
import os
import sqlite3
import sys


def verificar_ambiente():
    """Verifica se o ambiente está pronto para testes"""
    print("=== VERIFICANDO AMBIENTE ===")

    # Verificar banco de dados
    if not os.path.exists("database/gonetwork.db"):
        print("❌ Banco de dados não encontrado!")
        return False

    # Verificar tabelas necessárias
    try:
        conn = sqlite3.connect("database/gonetwork.db")
        cursor = conn.cursor()

        tabelas = ["video_edits", "video_comments", "editor_deliveries"]
        for tabela in tabelas:
            cursor.execute(
                f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{tabela}'"
            )
            if cursor.fetchone()[0] == 0:
                print(f"❌ Tabela {tabela} não encontrada!")
                return False

        # Verificar dados de teste
        cursor.execute("SELECT COUNT(*) FROM video_edits")
        if cursor.fetchone()[0] == 0:
            print("❌ Não há dados de edições para teste!")
            return False

    except Exception as e:
        print(f"❌ Erro ao verificar banco de dados: {str(e)}")
        return False

    print("✅ Ambiente verificado com sucesso!")
    return True


def iniciar_aplicacao():
    """Inicia a aplicação em modo de teste para a aba Edições"""
    if not verificar_ambiente():
        print("\nPrepare o ambiente de teste primeiro.")
        return False

    # Adicionar diretório atual ao path
    sys.path.append(os.getcwd())

    # Criar usuário de teste
    from database.UserRepository import UserRepository

    user_repo = UserRepository()
    user_id = None

    try:
        # Verificar se já existe usuário de teste
        users = user_repo.get_by_email("teste@gonetwork.ai")
        if users:
            user_id = users[0]["id"]
            print(f"✅ Usuário de teste encontrado: {users[0]['name']}")
        else:
            # Criar usuário de teste
            import uuid

            user_id = str(uuid.uuid4())
            cursor = sqlite3.connect("database/gonetwork.db").cursor()
            cursor.execute(
                """
                INSERT INTO users (id, name, email, password, role, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    "Usuário de Teste",
                    "teste@gonetwork.ai",
                    "senha123",
                    "admin",
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                ),
            )
            cursor.connection.commit()
            print("✅ Usuário de teste criado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao configurar usuário de teste: {str(e)}")
        return False

    if not user_id:
        print("❌ Não foi possível obter um usuário para teste!")
        return False

    # Configurar ambiente para iniciar na aba de Edições
    os.environ["GONETWORK_TEST_MODE"] = "1"
    os.environ["GONETWORK_TEST_USER"] = user_id
    os.environ["GONETWORK_INITIAL_TAB"] = "editing"  # Ir direto para a aba de edições

    print("\n=== INICIANDO APLICAÇÃO EM MODO DE TESTE ===")
    print("A aplicação será iniciada diretamente na aba de Edições")
    print("Usuário: teste@gonetwork.ai")
    print("Função: admin (acesso total)")

    try:
        # Importar e iniciar a aplicação
        import main

        sys.exit(main.main())
    except Exception as e:
        print(f"\n❌ Erro ao iniciar aplicação: {str(e)}")
        return False

    return True


if __name__ == "__main__":
    iniciar_aplicacao()
