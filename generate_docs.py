#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar a documentação usando Sphinx.
Este script executa os comandos necessários para gerar a documentação HTML completa.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path

# Diretório raiz do projeto
ROOT_DIR = Path(__file__).parent.resolve()
# Diretório onde a documentação Sphinx está localizada
SPHINX_DIR = ROOT_DIR / "docs" / "sphinx"
# Diretório de saída para a documentação HTML
BUILD_DIR = SPHINX_DIR / "build" / "html"


def create_dirs():
    """Cria os diretórios necessários caso não existam."""
    if not SPHINX_DIR.exists():
        print(f"Criando diretório Sphinx: {SPHINX_DIR}")
        SPHINX_DIR.mkdir(parents=True, exist_ok=True)

    # Garantir que o diretório _static existe para imagens
    static_dir = SPHINX_DIR / "source" / "_static" / "images"
    static_dir.mkdir(parents=True, exist_ok=True)


def generate_module_docs():
    """Gera a documentação automática para os módulos."""
    print("Gerando documentação de módulos...")

    # Cria o diretório para documentação de módulos
    modules_dir = SPHINX_DIR / "source" / "modulos"
    modules_dir.mkdir(parents=True, exist_ok=True)

    # Documentação para database, gui e utils
    for module in ["database", "gui", "utils"]:
        cmd = [
            "sphinx-apidoc",
            "-o",
            str(modules_dir),
            "-f",  # Força a sobrescrita de arquivos existentes
            "--implicit-namespaces",
            str(ROOT_DIR / module),
        ]
        try:
            subprocess.run(cmd, check=True)
            print(f"Documentação gerada para o módulo {module}")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao gerar documentação para {module}: {e}")
            return False

    return True


def build_docs():
    """Constrói a documentação HTML."""
    print("Construindo documentação HTML...")

    # Muda para o diretório da documentação
    os.chdir(SPHINX_DIR)

    # Executa o comando make html
    if os.name == "nt":  # Windows
        cmd = ["make.bat", "html"]
    else:  # Unix/Linux/Mac
        cmd = ["make", "html"]

    try:
        subprocess.run(cmd, check=True)
        print(f"Documentação HTML gerada com sucesso em {BUILD_DIR}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao construir a documentação: {e}")
        return False


def main():
    """Função principal para gerar a documentação."""
    print("Iniciando geração da documentação...")

    # Cria os diretórios necessários
    create_dirs()

    # Gera a documentação de módulos
    if not generate_module_docs():
        sys.exit(1)

    # Constrói a documentação HTML
    if not build_docs():
        sys.exit(1)

    print("Processo de geração de documentação concluído com sucesso!")
    print(
        f"Você pode visualizar a documentação abrindo o arquivo: {BUILD_DIR / 'index.html'}"
    )


if __name__ == "__main__":
    main()
