"""
Script para verificar o status da configuração do GoNetwork Web
Verifica dependências, configurações e banco de dados
"""

import importlib
import os
import sqlite3
import sys
from datetime import datetime

# Define cores para saída no terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_status(message, status):
    """Imprime mensagem de status colorida"""
    if status == "OK":
        status_color = f"{GREEN}[OK]{RESET}"
    elif status == "AVISO":
        status_color = f"{YELLOW}[AVISO]{RESET}"
    elif status == "ERRO":
        status_color = f"{RED}[ERRO]{RESET}"
    else:
        status_color = f"{BLUE}[INFO]{RESET}"

    print(f"{status_color} {message}")


def main():
    print(
        f"\n{BOLD}Verificação do GoNetwork Web - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}{RESET}\n"
    )

    # Verificar Python e versão
    python_version = sys.version
    print_status(f"Python: {python_version.split()[0]}", "OK")

    # Verificar dependências principais
    dependencies = {
        "streamlit": "Interface web",
        "streamlit_authenticator": "Sistema de autenticação",
        "pandas": "Manipulação de dados",
        "matplotlib": "Gráficos",
        "requests": "Requisições HTTP",
        "streamlit_extras": "Componentes adicionais",
        "streamlit_option_menu": "Menu de navegação",
        "streamlit_card": "Cards interativos",
        "streamlit_keyup": "Eventos de teclado",
    }

    print(f"\n{BOLD}Verificando dependências principais:{RESET}")
    for package, description in dependencies.items():
        try:
            mod = importlib.import_module(package)
            version = getattr(mod, "__version__", "Desconhecida")
            print_status(f"{package} (v{version}) - {description}", "OK")
        except ImportError:
            print_status(f"{package} - {description} - Não instalado", "ERRO")

    # Verificar configuração do Streamlit
    print(f"\n{BOLD}Verificando configuração do Streamlit:{RESET}")
    streamlit_config_path = os.path.join(
        os.path.abspath("."), ".streamlit", "config.toml"
    )
    if os.path.exists(streamlit_config_path):
        print_status(
            f"Arquivo de configuração do Streamlit encontrado em {streamlit_config_path}",
            "OK",
        )
    else:
        print_status("Arquivo de configuração do Streamlit não encontrado", "AVISO")

    # Verificar banco de dados
    print(f"\n{BOLD}Verificando banco de dados:{RESET}")
    db_path = os.path.join("c:\\melhor", "data", "gonetwork.db")

    if os.path.exists(db_path):
        print_status(f"Banco de dados encontrado em {db_path}", "OK")

        # Verificar tabelas e dados
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            # Verificar tabelas essenciais
            tables = [
                "users",
                "clients",
                "events",
                "briefings",
                "timeline_items",
                "deliverables",
                "team_members",
            ]

            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    if count > 0:
                        print_status(f"Tabela {table}: {count} registros", "OK")
                    else:
                        print_status(f"Tabela {table}: Vazia", "AVISO")
                except sqlite3.OperationalError:
                    print_status(f"Tabela {table}: Não encontrada", "ERRO")

            conn.close()
        except Exception as e:
            print_status(f"Erro ao verificar tabelas: {str(e)}", "ERRO")
    else:
        print_status(f"Banco de dados não encontrado em {db_path}", "ERRO")

    # Verificar estrutura de diretórios
    print(f"\n{BOLD}Verificando estrutura de diretórios:{RESET}")
    directories = {
        "pages": "Páginas da aplicação",
        "components": "Componentes reutilizáveis",
        "styles": "Estilos CSS",
        "utils": "Funções utilitárias",
        "assets": "Recursos visuais",
        "config": "Arquivos de configuração",
    }

    for directory, description in directories.items():
        dir_path = os.path.join(os.path.abspath("."), directory)
        if os.path.isdir(dir_path):
            file_count = len(
                [
                    f
                    for f in os.listdir(dir_path)
                    if os.path.isfile(os.path.join(dir_path, f))
                ]
            )
            print_status(f"{directory} - {description}: {file_count} arquivos", "OK")
        else:
            print_status(
                f"{directory} - {description}: Diretório não encontrado", "AVISO"
            )

    # Verificar arquivo principal
    if os.path.exists("app.py"):
        print_status("Arquivo principal app.py encontrado", "OK")
    else:
        print_status("Arquivo principal app.py não encontrado", "ERRO")

    print(f"\n{BOLD}Verificação concluída!{RESET}")
    print("\nPara iniciar o aplicativo, execute: streamlit run app.py")


if __name__ == "__main__":
    main()
