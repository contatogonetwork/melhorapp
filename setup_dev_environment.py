"""
Script de configuração do ambiente de desenvolvimento para o projeto GoNetwork AI.

Este script realiza as seguintes tarefas:
1. Instala pacotes de desenvolvimento necessários
2. Configura formatadores de código e ferramentas de linting
3. Aplica formatação padrão aos arquivos Python do projeto
"""

import os
import subprocess
import sys
import time
from pathlib import Path


def print_header(title):
    """Imprime um cabeçalho formatado."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_step(step_number, description):
    """Imprime o passo atual da instalação."""
    print(f"\n[{step_number}] {description}")
    print("-" * 70)


def run_command(command, description=None):
    """
    Executa um comando do sistema e exibe a saída.

    Args:
        command: Comando a ser executado
        description: Descrição opcional do comando

    Returns:
        bool: True se o comando foi executado com sucesso, False caso contrário
    """
    if description:
        print(f"{description}...")

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True,
        )

        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"ERRO (código {process.returncode}):")
            print(stderr.strip())
            return False

        if stdout.strip():
            print(stdout.strip())

        return True
    except Exception as e:
        print(f"ERRO: {str(e)}")
        return False


def install_development_packages():
    """Instala pacotes de desenvolvimento necessários."""
    packages = [
        "black",
        "isort",
        "pylint",
        "pytest",
    ]

    return run_command(
        f"python -m pip install {' '.join(packages)}",
        "Instalando pacotes de desenvolvimento",
    )


def create_pylintrc():
    """Cria arquivo de configuração para o Pylint."""
    config_content = """[MASTER]
disable=
    C0111, # missing docstring
    C0103, # invalid name
    C0303, # trailing whitespace
    C0330, # bad continuation
    C1801, # len-as-condition
    W0511, # fixme
    R0903, # too-few-public-methods
    R0913, # too-many-arguments

[FORMAT]
max-line-length=79
"""

    try:
        with open(".pylintrc", "w") as f:
            f.write(config_content)
        print("Arquivo .pylintrc criado com sucesso.")
        return True
    except Exception as e:
        print(f"ERRO ao criar .pylintrc: {str(e)}")
        return False


def format_python_files():
    """Aplica formatação a todos os arquivos Python do projeto."""
    print("Aplicando formatação black aos arquivos Python...")

    files_count = 0

    for root, _, files in os.walk("."):
        if "__pycache__" in root or ".venv" in root or "venv" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                result = run_command(f"python -m black {file_path}")

                if result:
                    files_count += 1

    print(f"Total de {files_count} arquivos formatados.")
    return True


def organize_imports():
    """Organiza as importações em todos os arquivos Python do projeto."""
    print("Organizando importações com isort...")

    return run_command("python -m isort .")


def create_vscode_settings():
    """Cria ou atualiza as configurações do VSCode para o projeto."""
    vscode_dir = Path(".vscode")
    if not vscode_dir.exists():
        vscode_dir.mkdir()

    settings_file = vscode_dir / "settings.json"
    extensions_file = vscode_dir / "extensions.json"

    settings_content = """{
    "editor.formatOnSave": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.formatting.blackArgs": [
        "--line-length",
        "79"
    ],
    "editor.codeActionsOnSave": {
        "source.organizeImports": "explicit"
    },
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.rulers": [
            79
        ]
    }
}"""

    extensions_content = """{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "njpwerner.autodocstring",
        "streetsidesoftware.code-spell-checker",
        "eamodio.gitlens",
        "gruntfuggly.todo-tree",
        "esbenp.prettier-vscode"
    ]
}"""

    try:
        with open(settings_file, "w") as f:
            f.write(settings_content)
        with open(extensions_file, "w") as f:
            f.write(extensions_content)
        print("Configurações do VSCode criadas com sucesso.")
        return True
    except Exception as e:
        print(f"ERRO ao criar configurações VSCode: {str(e)}")
        return False


def main():
    """Função principal do script de configuração."""
    print_header("CONFIGURAÇÃO DO AMBIENTE DE DESENVOLVIMENTO - GONETWORK AI")

    start_time = time.time()

    print_step(1, "Verificando ambiente Python")
    run_command("python --version")
    run_command("pip --version")

    print_step(2, "Instalando pacotes de desenvolvimento")
    install_development_packages()

    print_step(3, "Configurando ferramentas de linting e formatação")
    create_pylintrc()
    create_vscode_settings()

    print_step(4, "Formatando código do projeto")
    format_python_files()

    print_step(5, "Organizando importações")
    organize_imports()

    end_time = time.time()
    duration = end_time - start_time

    print_header("CONFIGURAÇÃO CONCLUÍDA")
    print(f"Tempo total: {duration:.1f} segundos")
    print(
        """
O ambiente de desenvolvimento foi configurado com sucesso!
Agora você tem:

- Black para formatação de código
- isort para organização de importações
- Pylint para análise estática
- Configurações do VSCode para desenvolvimento
"""
    )


if __name__ == "__main__":
    main()
