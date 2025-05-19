#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar a aba Briefing
"""

import os
import sys

from PySide6.QtWidgets import QApplication

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.widgets.briefing_widget import BriefingWidget

if __name__ == "__main__":
    # Inicializar aplicação
    app = QApplication([])

    # Criar widget
    widget = BriefingWidget()
    widget.resize(1200, 800)
    widget.show()

    print("Testando aba Briefing...")
    print("Verifique se todas as funcionalidades estão operando corretamente:")
    print("1. Seleção de evento funciona")
    print(
        "2. Todas as sub-abas estão presentes: Info, Estilo, Referências, etc."
    )
    print("3. Os formulários estão sendo exibidos corretamente")
    print("4. Os botões de salvar e gerar timeline funcionam")

    # Executar loop de eventos
    sys.exit(app.exec())
