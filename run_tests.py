#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para executar testes com pytest
"""

import os
import sys

import pytest

# Adicionar diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Executar testes com geração de relatório de cobertura
    pytest.main(
        [
            "-v",
            "--cov=database",
            "--cov=gui",
            "--cov=utils",
            "--cov-report=term",
            "--cov-report=html:coverage_report",
        ]
    )
