#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar e diagnóisticar a implementação da aba Briefing
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.BriefingRepository import BriefingRepository
from database.Database import Database


def check_briefing_tables():
    """Verifica se as tabelas do briefing existem no banco de dados"""
    db = Database()

    print("\n[1] Verificando tabelas do briefing...")

    tables = [
        "briefings",
        "sponsors",
        "sponsor_actions",
        "stages",
        "attractions",
        "realtime_deliveries",
        "post_deliveries",
    ]

    for table in tables:
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = db.fetch_one(query, (table,))

        if result:
            print(f"  ✓ Tabela '{table}' encontrada")
        else:
            print(f"  ✗ Tabela '{table}' NÃO encontrada")


def test_briefing_repository():
    """Testa as operações básicas do repositório de briefings"""
    briefing_repo = BriefingRepository()

    print("\n[2] Testando operações do BriefingRepository...")

    # Verificar método get_all
    try:
        briefings = briefing_repo.get_all()
        print(
            f"  ✓ Método get_all funcionando. {len(briefings)} briefings encontrados"
        )
    except Exception as e:
        print(f"  ✗ Erro ao chamar get_all: {str(e)}")

    # Verificar se existe ao menos um evento para criar um briefing de teste
    db = Database()
    query = "SELECT id FROM events LIMIT 1"
    result = db.fetch_one(query)

    if not result:
        print(
            "  ✗ Não foi possível testar a criação de briefing: nenhum evento encontrado"
        )
        return

    event_id = result["id"]

    # Testar criação de briefing
    try:
        briefing_data = {
            "event_id": event_id,
            "project_name": "Briefing de Teste",
            "client_id": "client_test",  # Usar ID válido em um ambiente real
            "delivery_date": datetime.now().isoformat(),
            "team_lead_id": None,
            "content": "Conteúdo de teste para o briefing",
        }

        briefing_id = briefing_repo.create(briefing_data)

        if briefing_id:
            print(f"  ✓ Método create funcionando. Briefing ID: {briefing_id}")

            # Testar get_by_id
            briefing = briefing_repo.get_by_id(briefing_id)

            if briefing and briefing["project_name"] == "Briefing de Teste":
                print("  ✓ Método get_by_id funcionando")
            else:
                print("  ✗ Erro no método get_by_id")

            # Testar update
            update_result = briefing_repo.update(
                briefing_id, {"project_name": "Briefing Atualizado"}
            )

            if update_result:
                briefing = briefing_repo.get_by_id(briefing_id)

                if (
                    briefing
                    and briefing["project_name"] == "Briefing Atualizado"
                ):
                    print("  ✓ Método update funcionando")
                else:
                    print("  ✗ Erro no método update")
            else:
                print("  ✗ Falha ao atualizar briefing")

            # Testar delete
            delete_result = briefing_repo.delete(briefing_id)

            if delete_result:
                briefing = briefing_repo.get_by_id(briefing_id)

                if briefing is None:
                    print("  ✓ Método delete funcionando")
                else:
                    print("  ✗ Erro no método delete")
            else:
                print("  ✗ Falha ao deletar briefing")

    except Exception as e:
        print(f"  ✗ Erro ao testar operações do repositório: {str(e)}")


def check_briefing_widget():
    """Verifica a implementação do widget de briefing"""
    print("\n[3] Verificando implementação do widget de briefing...")

    try:
        # Verificar apenas se o arquivo do widget existe
        if os.path.exists("gui/widgets/briefing_widget.py"):
            print("  ✓ Arquivo briefing_widget.py encontrado")

            # Verifica a presença de elementos importantes no código
            with open(
                "gui/widgets/briefing_widget.py", "r", encoding="utf-8"
            ) as f:
                content = f.read()

                if "class BriefingWidget" in content:
                    print("  ✓ Classe BriefingWidget implementada")
                else:
                    print("  ✗ Classe BriefingWidget não encontrada")

                if "def create_info_tab" in content:
                    print("  ✓ Método create_info_tab implementado")
                else:
                    print("  ✗ Método create_info_tab não encontrado")

                if "self.tabs.addTab" in content:
                    print("  ✓ Sistema de abas implementado")
                else:
                    print("  ✗ Sistema de abas não encontrado")
        else:
            print("  ✗ Arquivo briefing_widget.py não encontrado")

    except Exception as e:
        print(f"  ✗ Erro ao verificar widget: {str(e)}")


def check_main_window_integration():
    """Verifica a integração do widget com a janela principal"""
    print("\n[4] Verificando integração do widget com a janela principal...")

    try:
        if not os.path.exists("gui/main_window.py"):
            print("  ✗ Arquivo main_window.py não encontrado")
            return

        with open("gui/main_window.py", "r", encoding="utf-8") as f:
            content = f.read()

            if (
                "from gui.widgets.briefing_widget import BriefingWidget"
                in content
            ):
                print("  ✓ Importação do BriefingWidget encontrada")
            else:
                print("  ✗ Importação do BriefingWidget não encontrada")            if "self.briefing_widget" in content or "self.briefing_page" in content:
                print("  ✓ Instância do BriefingWidget criada")
            else:
                print("  ✗ Instância do BriefingWidget não encontrada")

            if (
                "self.add_widget(self.briefing_widget" in content
                or "self.stacked_widget.addWidget(self.briefing_widget" in content
                or "self.pages.addWidget(self.briefing_page)" in content
            ):
                print("  ✓ BriefingWidget adicionado ao layout")
            else:
                print("  ✗ BriefingWidget não adicionado ao layout")

    except Exception as e:
        print(
            f"  ✗ Erro ao verificar integração com a janela principal: {str(e)}"
        )


if __name__ == "__main__":
    print("=" * 60)
    print("DIAGNÓSTICO DE IMPLEMENTAÇÃO DA ABA BRIEFING")
    print("=" * 60)

    check_briefing_tables()
    test_briefing_repository()
    check_briefing_widget()
    check_main_window_integration()

    print("\n" + "=" * 60)
    print("DIAGNÓSTICO CONCLUÍDO")
    print("=" * 60)
