#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar e diagnósticar a implementação da aba Timeline
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.Database import Database
from database.TimelineRepository import TimelineRepository


def check_timeline_tables():
    """Verifica se as tabelas da timeline existem no banco de dados"""
    db = Database()

    print("\n[1] Verificando tabelas da timeline...")

    tables = [
        "timeline_items",
        "timeline_milestones",
        "timeline_notifications",
        "timeline_history",
    ]

    for table in tables:
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = db.fetch_one(query, (table,))

        if result:
            print(f"  ✓ Tabela '{table}' encontrada")
        else:
            print(f"  ✗ Tabela '{table}' NÃO encontrada")


def test_timeline_repository():
    """Testa as operações básicas do repositório da timeline"""
    timeline_repo = TimelineRepository()

    print("\n[2] Testando operações do TimelineRepository...")

    # Verificar se existe ao menos um evento para criar um item de timeline de teste
    db = Database()
    query = "SELECT id FROM events LIMIT 1"
    result = db.fetch_one(query)

    if not result:
        print("  ✗ Não foi possível testar a criação de item: nenhum evento encontrado")
        return

    event_id = result["id"]

    # Testar criação de item na timeline
    try:
        # Horários para o item de teste
        now = datetime.now()
        start_time = now.replace(hour=10, minute=0, second=0).isoformat()
        end_time = now.replace(hour=12, minute=0, second=0).isoformat()

        item_data = {
            "event_id": event_id,
            "title": "Item de Teste",
            "description": "Descrição do item de teste",
            "start_time": start_time,
            "end_time": end_time,
            "responsible_id": None,
            "task_type": "Teste",
            "status": "Pendente",
            "priority": 3,
            "color": "#4682B4",
            "dependencies": "[]",
            "location": "Local de teste",
        }

        item_id = timeline_repo.create_item(item_data)

        if item_id:
            print(f"  ✓ Método create_item funcionando. Item ID: {item_id}")

            # Testar get_by_id
            item = timeline_repo.get_by_id(item_id)

            if item and item["title"] == "Item de Teste":
                print("  ✓ Método get_by_id funcionando")
            else:
                print("  ✗ Erro no método get_by_id")

            # Testar get_by_event
            items = timeline_repo.get_by_event(event_id)

            if items and any(i["id"] == item_id for i in items):
                print("  ✓ Método get_by_event funcionando")
            else:
                print("  ✗ Erro no método get_by_event")

            # Testar update
            update_result = timeline_repo.update(item_id, {"title": "Item Atualizado"})

            if update_result:
                item = timeline_repo.get_by_id(item_id)

                if item and item["title"] == "Item Atualizado":
                    print("  ✓ Método update funcionando")
                else:
                    print("  ✗ Erro no método update")
            else:
                print("  ✗ Falha ao atualizar item")

            # Testar criação de marco
            milestone_data = {
                "event_id": event_id,
                "title": "Marco de Teste",
                "description": "Descrição do marco de teste",
                "milestone_time": now.replace(hour=14, minute=0, second=0).isoformat(),
                "importance": 4,
            }

            milestone_id = timeline_repo.create_milestone(milestone_data)

            if milestone_id:
                print(
                    f"  ✓ Método create_milestone funcionando. Milestone ID: {milestone_id}"
                )

                # Testar get_milestones_by_event
                milestones = timeline_repo.get_milestones_by_event(event_id)

                if milestones and any(m["id"] == milestone_id for m in milestones):
                    print("  ✓ Método get_milestones_by_event funcionando")
                else:
                    print("  ✗ Erro no método get_milestones_by_event")
            else:
                print("  ✗ Falha ao criar marco")

            # Testar criação de notificação
            notification_data = {
                "timeline_item_id": item_id,
                "notification_time": now.replace(
                    hour=9, minute=0, second=0
                ).isoformat(),
                "notification_type": "Lembrete",
                "message": "Lembrete de teste",
            }

            notification_id = timeline_repo.add_notification(notification_data)

            if notification_id:
                print(f"  ✓ Método add_notification funcionando")
            else:
                print("  ✗ Falha ao criar notificação")

            # Testar registro de histórico
            history_data = {
                "timeline_item_id": item_id,
                "changed_by": "user_test",  # Usar ID válido em ambiente real
                "change_description": "Alteração de teste",
                "previous_value": "Item de Teste",
                "new_value": "Item Atualizado",
                "changed_field": "title",
            }

            history_id = timeline_repo.log_timeline_change(history_data)

            if history_id:
                print(f"  ✓ Método log_timeline_change funcionando")
            else:
                print("  ✗ Falha ao registrar alteração")

            # Testar delete
            delete_result = timeline_repo.delete(item_id)

            if delete_result:
                item = timeline_repo.get_by_id(item_id)

                if item is None:
                    print("  ✓ Método delete funcionando")
                else:
                    print("  ✗ Erro no método delete")
            else:
                print("  ✗ Falha ao deletar item")

    except Exception as e:
        print(f"  ✗ Erro ao testar operações do repositório: {str(e)}")


def check_timeline_widget():
    """Verifica a implementação do widget de timeline"""
    print("\n[3] Verificando implementação do widget de timeline...")

    try:
        # Verificar apenas se o arquivo do widget existe
        if os.path.exists("gui/widgets/timeline_widget.py"):
            print("  ✓ Arquivo timeline_widget.py encontrado")

            # Verifica a presença de elementos importantes no código
            with open("gui/widgets/timeline_widget.py", "r", encoding="utf-8") as f:
                content = f.read()

                if "class TimelineWidget" in content:
                    print("  ✓ Classe TimelineWidget implementada")
                else:
                    print("  ✗ Classe TimelineWidget não encontrada")

                if "class TimelineView" in content:
                    print("  ✓ Classe TimelineView implementada")
                else:
                    print("  ✗ Classe TimelineView não encontrada")

                if "self.filter_layout" in content:
                    print("  ✓ Sistema de filtros implementado")
                else:
                    print("  ✗ Sistema de filtros não encontrado")
        else:
            print("  ✗ Arquivo timeline_widget.py não encontrado")

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

            if "from gui.widgets.timeline_widget import TimelineWidget" in content:
                print("  ✓ Importação do TimelineWidget encontrada")
            else:
                print("  ✗ Importação do TimelineWidget não encontrada")

            if "self.timeline_widget" in content or "self.timeline_page" in content:
                print("  ✓ Instância do TimelineWidget criada")
            else:
                print("  ✗ Instância do TimelineWidget não encontrada")

            if (
                "self.add_widget(self.timeline_widget" in content
                or "self.stacked_widget.addWidget(self.timeline_widget" in content
                or "self.pages.addWidget(self.timeline_page)" in content
                or "pages.addWidget(self.timeline_page)" in content
            ):
                print("  ✓ TimelineWidget adicionado ao layout")
            else:
                print("  ✗ TimelineWidget não adicionado ao layout")

    except Exception as e:
        print(f"  ✗ Erro ao verificar integração com a janela principal: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("DIAGNÓSTICO DE IMPLEMENTAÇÃO DA ABA TIMELINE")
    print("=" * 60)

    check_timeline_tables()
    test_timeline_repository()
    check_timeline_widget()
    check_main_window_integration()

    print("\n" + "=" * 60)
    print("DIAGNÓSTICO CONCLUÍDO")
    print("=" * 60)
