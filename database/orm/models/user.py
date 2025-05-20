#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo ORM para a tabela de usuários.

Este módulo define o modelo SQLAlchemy para a tabela de usuários,
incluindo métodos para autenticação e gerenciamento de senhas.
"""

from datetime import datetime
from typing import Optional

import bcrypt
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import Session

from database.orm.base import Base


class User(Base):
    """Modelo SQLAlchemy para tabela de usuários."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")
    profile_picture = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def hash_password(password: str) -> tuple[str, str]:
        """
        Gera um hash seguro para a senha do usuário usando bcrypt.

        Args:
            password: Senha em texto puro

        Returns:
            tuple: (hash_da_senha, salt)
        """
        # Gerar salt
        salt = bcrypt.gensalt()

        # Criar hash da senha com o salt
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        return password_hash.decode("utf-8"), salt.decode("utf-8")

    @staticmethod
    def verify_password(password: str, hashed_password: str, salt: str) -> bool:
        """
        Verifica se a senha fornecida corresponde ao hash armazenado.

        Args:
            password: Senha em texto puro a ser verificada
            hashed_password: Hash armazenado da senha
            salt: Salt usado para gerar o hash original

        Returns:
            bool: True se a senha for válida
        """
        password_bytes = password.encode("utf-8")
        salt_bytes = salt.encode("utf-8")
        hashed = bcrypt.hashpw(password_bytes, salt_bytes)
        return hashed.decode("utf-8") == hashed_password

    @classmethod
    def authenticate(
        cls, db: Session, username: str, password: str
    ) -> Optional["User"]:
        """
        Autentica um usuário verificando nome de usuário e senha.

        Args:
            db: Sessão do SQLAlchemy
            username: Nome de usuário
            password: Senha em texto puro

        Returns:
            Optional[User]: Objeto User se autenticado com sucesso, None caso contrário
        """
        user = db.query(cls).filter(cls.username == username).first()

        if not user:
            return None

        if cls.verify_password(password, user.password_hash, user.salt):
            return user

        return None

    def __repr__(self) -> str:
        """Representação em string do objeto."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
