#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Testes para UserRepository
"""

import os
import sqlite3
import tempfile

import pytest

from database.Database import Database
from database.UserRepository import UserRepository
from utils.auth import hash_password, verify_password


class TestUserRepository:
    @pytest.fixture
    def temp_db(self):
        """Cria um banco de dados temporário para testes."""
        # Criar arquivo temporário
        fd, path = tempfile.mkstemp()
        os.close(fd)

        # Criar conexão e tabela
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                last_login TEXT
            )
        """
        )
        conn.commit()

        # Retornar conexão
        yield conn

        # Cleanup
        conn.close()
        os.unlink(path)

    def test_create_user(self, temp_db):
        """Testa a criação de um usuário."""
        # Arrange
        repo = UserRepository(temp_db)
        username = "testuser"
        password = "securepassword123"

        # Act
        user_id = repo.create_user(username, hash_password(password))

        # Assert
        assert user_id > 0

        # Verificar se o usuário existe
        cursor = temp_db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        assert user is not None
        assert user[1] == username  # username é a segunda coluna

    def test_get_user(self, temp_db):
        """Testa a recuperação de um usuário."""
        # Arrange
        repo = UserRepository(temp_db)
        username = "testuser2"
        password = "securepassword456"
        hashed_pw = hash_password(password)

        # Criar usuário primeiro
        repo.create_user(username, hashed_pw)

        # Act
        user = repo.get_user(username)

        # Assert
        assert user is not None
        assert user["username"] == username
        assert verify_password(password, user["password"])
