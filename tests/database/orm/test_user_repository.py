#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes para o repositório ORM de usuários.

Este módulo contém testes unitários para a classe UserRepository
que usa SQLAlchemy ORM.
"""

import os
import sys
import unittest
from datetime import datetime
from unittest import mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

# Adicionar diretório raiz ao path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from database.orm.base import Base
from database.orm.models.user import User
from database.orm.repositories.user_repository import UserRepository


class TestUserRepository(unittest.TestCase):
    """Testes para UserRepository."""

    @classmethod
    def setUpClass(cls):
        """Configuração inicial para todos os testes."""
        # Criar engine SQLite em memória
        cls.engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        # Criar tabelas
        Base.metadata.create_all(cls.engine)
        # Criar sessão
        cls.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=cls.engine
        )

    def setUp(self):
        """Configuração para cada teste."""
        # Criar sessão de teste
        self.session = self.SessionLocal()
        self.addCleanup(self.session.close)

        # Mock para get_db_session para usar a sessão de teste
        self.session_context = mock.patch(
            "database.orm.repositories.base_repository.get_db_session"
        )
        self.mock_get_db_session = self.session_context.start()
        self.mock_get_db_session.return_value.__enter__.return_value = self.session
        self.addCleanup(self.session_context.stop)

        # Criar repositório
        self.repo = UserRepository()

        # Adicionar alguns dados de teste
        self.test_user = User(
            username="teste",
            email="teste@example.com",
            full_name="Usuário Teste",
            password_hash="hash_teste",
            salt="salt_teste",
            role="user",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        self.session.add(self.test_user)
        self.session.commit()
        self.session.refresh(self.test_user)

    def tearDown(self):
        """Limpeza após cada teste."""
        self.session.query(User).delete()
        self.session.commit()

    def test_get_by_id(self):
        """Testa o método get_by_id."""
        user = self.repo.get_by_id(self.test_user.id)
        assert user is not None
        assert user.username == "teste"
        assert user.email == "teste@example.com"

        # Testar ID inexistente
        user = self.repo.get_by_id(999)
        assert user is None

    def test_get_by_username(self):
        """Testa o método get_by_username."""
        user = self.repo.get_by_username("teste")
        assert user is not None
        assert user.id == self.test_user.id

        # Testar username inexistente
        user = self.repo.get_by_username("naoexiste")
        assert user is None

    def test_create(self):
        """Testa o método create."""
        # Mock para hash_password
        original_hash_password = User.hash_password
        User.hash_password = mock.MagicMock(return_value=("hash_novo", "salt_novo"))

        try:
            new_user = {
                "username": "novo",
                "email": "novo@example.com",
                "full_name": "Novo Usuário",
                "password": "senha123",
                "role": "admin",
            }

            created = self.repo.create(new_user)
            assert created is not None
            assert created.username == "novo"
            assert created.email == "novo@example.com"
            assert created.role == "admin"

            # Verificar se foi persistido
            user = self.session.query(User).filter(User.username == "novo").first()
            assert user is not None
        finally:
            # Restaurar método original
            User.hash_password = original_hash_password

    def test_update(self):
        """Testa o método update."""
        update_data = {"full_name": "Nome Atualizado", "role": "editor"}

        updated = self.repo.update(self.test_user.id, update_data)
        assert updated is not None
        assert updated.full_name == "Nome Atualizado"
        assert updated.role == "editor"

        # Verificar se foi persistido
        user = self.session.query(User).get(self.test_user.id)
        assert user.full_name == "Nome Atualizado"
        assert user.role == "editor"

        # Testar ID inexistente
        updated = self.repo.update(999, update_data)
        assert updated is None

    def test_delete(self):
        """Testa o método delete."""
        result = self.repo.delete(self.test_user.id)
        assert result is True

        # Verificar se foi realmente excluído
        user = self.session.query(User).get(self.test_user.id)
        assert user is None

        # Testar ID inexistente
        result = self.repo.delete(999)
        assert result is False

    def test_authenticate(self):
        """Testa o método authenticate."""
        # Mock para authenticate
        original_authenticate = User.authenticate
        User.authenticate = mock.MagicMock(return_value=self.test_user)

        try:
            user = self.repo.authenticate("teste", "senha123")
            assert user is not None
            User.authenticate.assert_called_with(self.session, "teste", "senha123")

            # Testar autenticação inválida
            User.authenticate.return_value = None
            user = self.repo.authenticate("teste", "senha_errada")
            assert user is None
        finally:
            # Restaurar método original
            User.authenticate = original_authenticate
