#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a aba Timeline
"""

import os
import sys

from PySide6.QtWidgets import QApplication

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.widgets.timeline_widget import TimelineWidget

if __name__ == "__main__":
    # Inicializar aplicação
    app = QApplication([])

    # Criar widget
    widget = TimelineWidget()
    widget.resize(1200, 800)
    widget.show()

    print("Testando aba Timeline...")
    print("Verifique se todas as funcionalidades estão operando corretamente:")
    print("1. Seleção de evento funciona")
    print("2. Os filtros de membro, atividade e status funcionam")
    print("3. A visualização da timeline é exibida corretamente")
    print("4. Os botões de atualizar e exportar funcionam")

    # Executar loop de eventos
    sys.exit(app.exec())
