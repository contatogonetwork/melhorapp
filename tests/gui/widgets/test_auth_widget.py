#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes para o widget de autenticação
"""

from unittest.mock import MagicMock, patch

import pytest
from PySide6.QtCore import Qt

from gui.widgets.auth_widget import AuthWidget


class TestAuthWidget:
    @pytest.fixture
    def auth_widget(self, qtbot):
        """Cria o widget de autenticação para testes."""
        widget = AuthWidget()
        qtbot.addWidget(widget)
        return widget

    def test_initial_state(self, auth_widget):
        """Verifica o estado inicial do widget."""
        # Email e senha devem estar vazios no início
        assert auth_widget.email_input.text() == ""
        assert auth_widget.password_input.text() == ""

        # Botão de login deve estar habilitado
        assert auth_widget.login_button.isEnabled()

        # Widget de abas deve ter duas abas: login e cadastro
        assert auth_widget.tab_widget.count() == 2
        assert auth_widget.tab_widget.tabText(0) == "Login"
        assert auth_widget.tab_widget.tabText(1) == "Cadastro"

    def test_empty_fields_warning(self, auth_widget, qtbot, monkeypatch):
        """Testa se o aviso é mostrado quando os campos estão vazios."""
        # Mock para o QMessageBox.warning
        mock_warning = MagicMock()
        monkeypatch.setattr(
            "PySide6.QtWidgets.QMessageBox.warning", mock_warning
        )

        # Clicar no botão de login sem preencher campos
        qtbot.mouseClick(auth_widget.login_button, Qt.LeftButton)

        # Verificar se o warning foi chamado
        mock_warning.assert_called_once()

    @patch("database.UserRepository.UserRepository")
    @patch("database.Database.Database")
    @patch("utils.auth.verify_password")
    def test_successful_login(
        self, mock_verify, mock_db, mock_repo, auth_widget, qtbot, monkeypatch
    ):
        """Testa login bem-sucedido."""
        # Configurar mocks
        mock_instance = mock_repo.return_value
        mock_instance.get_user.return_value = {
            "username": "test@example.com",
            "password": "hashedpw",
        }
        mock_verify.return_value = True

        # Mock para o QMessageBox.information
        mock_info = MagicMock()
        monkeypatch.setattr(
            "PySide6.QtWidgets.QMessageBox.information", mock_info
        )

        # Espionar o sinal login_successful
        spy = qtbot.waitSignal(auth_widget.login_successful)

        # Preencher formulário
        auth_widget.email_input.setText("test@example.com")
        auth_widget.password_input.setText("password123")

        # Clicar no botão de login
        qtbot.mouseClick(auth_widget.login_button, Qt.LeftButton)

        # Verificar se o login foi bem-sucedido
        assert spy.signal_triggered
        mock_info.assert_called_once()
