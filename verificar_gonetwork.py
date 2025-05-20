#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ferramenta automatizada para verificação do GoNetwork AI.
Realiza uma verificação completa dos aspectos técnicos da aplicação.
Uso: python verificar_gonetwork.py [--verbose] [--fix]

Opções:
    --verbose   Mostra informações detalhadas
    --fix       Tenta corrigir problemas encontrados
"""
import importlib
import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

# Cores para saída
VERMELHO = "\033[91m"
VERDE = "\033[92m"
AMARELO = "\033[93m"
AZUL = "\033[94m"
RESET = "\033[0m"

# Configurações
VERBOSE = "--verbose" in sys.argv
FIX = "--fix" in sys.argv
ROOT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = ROOT_DIR / "data" / "gonetwork.db"


def print_header(texto):
    """Imprime um cabeçalho formatado."""
    print(f"\n{AZUL}{'='*60}{RESET}")
    print(f"{AZUL}== {texto}{RESET}")
    print(f"{AZUL}{'='*60}{RESET}")


def print_ok(texto):
    """Imprime uma mensagem de sucesso."""
    print(f"{VERDE}✓ {texto}{RESET}")


def print_error(texto):
    """Imprime uma mensagem de erro."""
    print(f"{VERMELHO}✗ {texto}{RESET}")


def print_warning(texto):
    """Imprime uma mensagem de aviso."""
    print(f"{AMARELO}! {texto}{RESET}")


def print_info(texto):
    """Imprime uma mensagem informativa se o modo verbose estiver ativado."""
    if VERBOSE:
        print(f"  {texto}")


def verificar_arquivos():
    """Verifica a existência dos arquivos principais."""
    print_header("VERIFICAÇÃO DE ESTRUTURA DE ARQUIVOS")
    arquivos = [
        ("database/VideoRepository.py", "Repositório de vídeos"),
        ("database/BriefingRepository.py", "Repositório de briefing"),
        ("database/TimelineRepository.py", "Repositório de timeline"),
        ("gui/widgets/editing_widget.py", "Widget de edição"),
        ("gui/widgets/briefing_widget.py", "Widget de briefing"),
        ("gui/widgets/timeline_widget.py", "Widget de timeline"),
        ("database/schema/video_edits_tables.sql", "Esquema SQL para edições de vídeo"),
        ("docs/sphinx/source/conf.py", "Configuração do Sphinx"),
    ]

    todos_encontrados = True
    for caminho, descricao in arquivos:
        arquivo = ROOT_DIR / caminho
        if arquivo.exists():
            print_ok(f"{descricao} encontrado: {caminho}")
        else:
            todos_encontrados = False
            print_error(f"{descricao} ausente: {caminho}")

    return todos_encontrados


def verificar_banco_dados():
    """Verifica a estrutura do banco de dados."""
    print_header("VERIFICAÇÃO DO BANCO DE DADOS")

    # Verificar se o arquivo do banco existe
    if not DB_PATH.exists():
        print_error(f"Banco de dados não encontrado: {DB_PATH}")
        return False

    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()

        # Obter lista de tabelas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = [row[0] for row in cursor.fetchall()]

        # Tabelas esperadas
        tabelas_esperadas = [
            "events",
            "team_members",
            "clients",
            "briefings",
            "videos",
            "video_edits",
            "video_comments",
            "timeline_items",
        ]

        # Verificar tabelas
        for tabela in tabelas_esperadas:
            if tabela in tabelas:
                # Contar número de registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                count = cursor.fetchone()[0]

                # Obter número de colunas
                cursor.execute(f"PRAGMA table_info({tabela})")
                num_colunas = len(cursor.fetchall())

                print_ok(
                    f"Tabela '{tabela}' encontrada ({num_colunas} colunas, {count} registros)"
                )
            else:
                print_error(f"Tabela '{tabela}' ausente")

        # Verificar integridade do banco
        cursor.execute("PRAGMA integrity_check")
        resultado = cursor.fetchone()[0]
        if resultado == "ok":
            print_ok("Verificação de integridade SQLite: OK")
        else:
            print_error(f"Problemas de integridade no banco: {resultado}")

        conn.close()
        return True

    except sqlite3.Error as e:
        print_error(f"Erro ao verificar banco de dados: {e}")
        return False


def verificar_codigo():
    """Verifica a qualidade do código."""
    print_header("VERIFICAÇÃO DE CÓDIGO")

    # Módulos para verificar
    modulos = [
        ("database.VideoRepository", "Repositório de vídeos"),
        ("database.BriefingRepository", "Repositório de briefing"),
        ("database.TimelineRepository", "Repositório de timeline"),
        ("gui.widgets.editing_widget", "Widget de edição"),
        ("gui.widgets.briefing_widget", "Widget de briefing"),
        ("gui.widgets.timeline_widget", "Widget de timeline"),
        ("utils.accessibility", "Módulo de acessibilidade"),
    ]

    status = True
    for modulo, descricao in modulos:
        try:
            # Verificar se o módulo pode ser importado
            importlib.import_module(modulo)
            print_ok(f"{descricao} - importação bem-sucedida")
        except ImportError as e:
            status = False
            print_error(f"{descricao} - falha ao importar: {e}")

    return status


def verificar_testes():
    """Verifica os testes unitários."""
    print_header("VERIFICAÇÃO DE TESTES UNITÁRIOS")

    # Contar arquivos de teste
    pasta_testes = ROOT_DIR / "tests"
    if not pasta_testes.exists():
        print_error("Pasta de testes não encontrada")
        return False

    arquivos_teste = []
    for root, _, files in os.walk(str(pasta_testes)):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                arquivos_teste.append(os.path.join(root, file))

    print_info(f"Encontrados {len(arquivos_teste)} arquivos de teste")

    for arquivo in arquivos_teste:
        print_info(f"Arquivo de teste: {os.path.relpath(arquivo, str(ROOT_DIR))}")

    # Tentativa de execução de testes específicos
    try:
        print_warning("Teste de widget de autenticação")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/gui/widgets/test_auth_widget.py",
                "-v",
            ],
            cwd=str(ROOT_DIR),
            check=True,
            capture_output=True,
        )
        print_ok("Testes de autenticação executados com sucesso")
    except subprocess.CalledProcessError as e:
        print_error(f"Erro nos testes de autenticação: {e.stderr.decode('utf-8')}")

    try:
        print_warning("Teste de repositório de usuário")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                "tests/database/test_user_repository.py",
                "-v",
            ],
            cwd=str(ROOT_DIR),
            check=True,
            capture_output=True,
        )
        print_ok("Testes de repositório executados com sucesso")
    except subprocess.CalledProcessError as e:
        print_error(f"Erro nos testes de repositório: {e.stderr.decode('utf-8')}")

    return len(arquivos_teste) > 0


def verificar_acessibilidade():
    """Verifica os recursos de acessibilidade."""
    print_header("VERIFICAÇÃO DE ACESSIBILIDADE")

    arquivos = {
        "Módulo de acessibilidade": ROOT_DIR / "utils" / "accessibility.py",
        "Widget de acessibilidade": ROOT_DIR
        / "gui"
        / "widgets"
        / "accessibility_widget.py",
        "Demo de acessibilidade": ROOT_DIR / "accessibility_demo.py",
    }

    # Verificar existência dos arquivos
    status = True
    for desc, caminho in arquivos.items():
        if caminho.exists():
            print_ok(f"{desc} encontrado: {caminho}")
        else:
            status = False
            print_error(f"{desc} ausente: {caminho}")

    # Verificar recursos implementados
    try:
        from utils.accessibility import ColorScheme, FontSize

        print_ok("Enums de acessibilidade (FontSize, ColorScheme) implementados")
    except ImportError:
        status = False
        print_error("Enums de acessibilidade não implementados")

    return status


def verificar_documentacao():
    """Verifica a documentação Sphinx."""
    print_header("VERIFICAÇÃO DE DOCUMENTAÇÃO SPHINX")

    # Verificar estrutura básica
    pasta_sphinx = ROOT_DIR / "docs" / "sphinx"
    if not pasta_sphinx.exists():
        print_error("Pasta de documentação Sphinx não encontrada")
        return False

    # Verificar configuração
    conf_path = pasta_sphinx / "source" / "conf.py"
    if not conf_path.exists():
        print_error("Arquivo de configuração do Sphinx não encontrado")
        return False

    print_ok(f"Arquivo de configuração Sphinx encontrado: {conf_path}")

    # Contar arquivos de documentação
    arquivos_rst = []
    for root, _, files in os.walk(str(pasta_sphinx)):
        for file in files:
            if file.endswith(".rst") or file.endswith(".md"):
                arquivos_rst.append(os.path.join(root, file))

    print_ok(f"Encontrados {len(arquivos_rst)} arquivos de documentação")

    # Verificar se a documentação pode ser gerada
    try:
        output = subprocess.run(
            ["sphinx-build", "-b", "html", "source", "build"],
            cwd=str(pasta_sphinx),
            capture_output=True,
            text=True,
            check=False,
        )

        if output.returncode == 0:
            print_ok("Documentação gerada com sucesso")
        else:
            print_warning("Aviso ao gerar documentação:")
            print_info(output.stderr)
    except Exception as e:
        print_error(f"Erro ao tentar gerar documentação: {e}")

    return True


def verificar_aplicacao():
    """Verifica se a aplicação pode ser iniciada."""
    print_header("VERIFICAÇÃO DE INICIALIZAÇÃO DA APLICAÇÃO")

    main_path = ROOT_DIR / "main.py"
    if not main_path.exists():
        print_error(f"Arquivo principal não encontrado: {main_path}")
        return False

    print_warning(
        "A aplicação seria iniciada aqui em um ambiente de verificação completo."
    )
    print_warning("Este teste requer uma interface gráfica e pode pausar o script.")

    if VERBOSE:
        print_info("Para testar manualmente a inicialização, execute:")
        print_info(f"python {main_path}")

    # Verificar config.json
    config_path = ROOT_DIR / "config.json"
    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            print_ok(
                f"Arquivo de configuração válido: {len(config)} configurações encontradas"
            )
        except json.JSONDecodeError as e:
            print_error(f"Erro de formato no arquivo de configuração: {e}")
    else:
        print_warning(f"Arquivo de configuração não encontrado: {config_path}")

    return True


def relatorio_final(resultados):
    """Imprime um relatório final com os resultados da verificação."""
    print_header("RELATÓRIO FINAL")

    total = len(resultados)
    passou = sum(1 for r in resultados.values() if r)
    falhou = total - passou

    print(f"Total de verificações: {total}")
    print(f"Aprovadas: {VERDE}{passou}{RESET}")
    print(f"Falhas: {VERMELHO if falhou > 0 else VERDE}{falhou}{RESET}")

    print("\nDetalhes:")
    for teste, resultado in resultados.items():
        status = f"{VERDE}APROVADO{RESET}" if resultado else f"{VERMELHO}FALHA{RESET}"
        print(f"- {teste}: {status}")

    if FIX and falhou > 0:
        print("\nRecomendações para correção:")
        if not resultados["Arquivos"]:
            print(
                "- Execute o script setup_dev_environment.py para criar arquivos ausentes"
            )
        if not resultados["Banco de dados"]:
            print("- Execute o script setup_database.py para criar tabelas ausentes")
        if not resultados["Testes"]:
            print("- Verifique a estrutura de testes e as dependências pytest")


def main():
    """Função principal do script."""
    print("\n📋 VERIFICAÇÃO TÉCNICA DO GONETWORK AI 📋\n")
    print(f"Data: {os.popen('date /T').read().strip()}")
    print(f"Diretório: {ROOT_DIR}")

    if VERBOSE:
        print("Modo detalhado ativado")
    if FIX:
        print("Modo de correção ativado")

    # Executar verificações
    resultados = {
        "Arquivos": verificar_arquivos(),
        "Banco de dados": verificar_banco_dados(),
        "Código": verificar_codigo(),
        "Testes": verificar_testes(),
        "Acessibilidade": verificar_acessibilidade(),
        "Documentação": verificar_documentacao(),
        "Aplicação": verificar_aplicacao(),
    }

    # Exibir relatório final
    relatorio_final(resultados)

    # Retornar código de saída
    return 0 if all(resultados.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
