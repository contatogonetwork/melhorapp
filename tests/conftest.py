#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações globais para testes pytest
"""

import os
import sys

import pytest
from PySide6.QtWidgets import QApplication

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Fixture para ter um app Qt disponível para todos os testes
@pytest.fixture(scope="session")
def qt_app():
    """Cria uma instância do aplicativo Qt para os testes."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
