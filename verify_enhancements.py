# verify_enhancements.py - Script para verificar melhorias aplicadas
import importlib
import inspect
import os
import re
import sys


def check_docstrings():
    """Verifica se as funções possuem docstrings."""
    files_checked = 0
    functions_checked = 0
    functions_with_docstrings = 0

    for root, _, files in os.walk("."):
        if "__pycache__" in root or ".venv" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                files_checked += 1
                module_path = (
                    os.path.join(root, file)[2:-3].replace("/", ".").replace("\\", ".")
                )

                try:
                    # Tentativa de importar o módulo
                    spec = importlib.util.find_spec(module_path)
                    if spec:
                        module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(module)

                        # Verificar funções e métodos
                        for name, obj in inspect.getmembers(module):
                            if inspect.isfunction(obj) or inspect.ismethod(obj):
                                functions_checked += 1
                                if obj.__doc__:
                                    functions_with_docstrings += 1
                except:
                    # Ignorar erros de importação
                    pass

    docstring_rate = (
        functions_with_docstrings / functions_checked if functions_checked else 0
    )
    print(f"Arquivos verificados: {files_checked}")
    print(
        f"Funções com docstrings: {functions_with_docstrings}/{functions_checked} ({docstring_rate:.1%})"
    )
    return docstring_rate >= 0.7  # Sucesso se 70% ou mais das funções têm docstrings


def check_error_handling():
    """Verifica aprimoramentos no tratamento de erros."""
    files_checked = 0
    files_with_good_error_handling = 0

    for root, _, files in os.walk("."):
        if "__pycache__" in root or ".venv" in root:
            continue

        for file in files:
            if file.endswith(".py"):
                files_checked += 1
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()

                    # Procurar padrões de bom tratamento de erros
                    has_try_except = re.search(
                        r"try:.*?except\s+\w+(\s+as\s+\w+)?:",
                        content,
                        re.DOTALL,
                    )
                    has_specific_catches = re.search(
                        r"except\s+(?!Exception)[A-Za-z]+Error", content
                    )
                    has_logging = re.search(
                        r"logging\.(error|warning|critical|exception)", content
                    )

                    if has_try_except and (has_specific_catches or has_logging):
                        files_with_good_error_handling += 1

                except:
                    pass

    error_handling_rate = (
        files_with_good_error_handling / files_checked if files_checked else 0
    )
    print(
        f"Arquivos com tratamento de erros robusto: {files_with_good_error_handling}/{files_checked} ({error_handling_rate:.1%})"
    )
    return (
        error_handling_rate >= 0.5
    )  # Sucesso se 50% ou mais dos arquivos têm bom tratamento de erros


if __name__ == "__main__":
    print("Verificando melhorias no projeto...\n")

    docstrings_ok = check_docstrings()
    error_handling_ok = check_error_handling()

    print("\nResultados:")
    print(f"- Documentação: {'✓ BOM' if docstrings_ok else '✗ PRECISA MELHORAR'}")
    print(
        f"- Tratamento de Erros: {'✓ BOM' if error_handling_ok else '✗ PRECISA MELHORAR'}"
    )

    if docstrings_ok and error_handling_ok:
        print("\nO projeto está com boa qualidade de código!")
    else:
        print("\nAinda há melhorias a serem implementadas.")
