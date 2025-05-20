#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Repositório para operações com usuários usando SQLAlchemy ORM.

Esta classe fornece uma camada de abstração para operações de banco de dados
relacionadas a usuários, usando o SQLAlchemy ORM.
"""

from typing import Dict, List, Optional, Union

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.orm.base import get_db_session
from database.orm.models.user import User
from database.orm.repositories.base_repository import BaseRepository
from utils.logger import get_logger


class UserRepository(BaseRepository):
    """Repositório para operações com usuários usando SQLAlchemy ORM."""

    def __init__(self):
        """Inicializa o repositório."""
        super().__init__(User)

    def get_all(self) -> List[Dict]:
        """
        Obtém todos os usuários.

        Returns:
            List[Dict]: Lista de usuários como dicionários
        """
        try:
            with get_db_session() as session:
                result = session.execute(select(User))
                users = result.scalars().all()
                return [self._user_to_dict(user) for user in users]
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao obter usuários: {e}")
            return []

    def get_by_id(self, user_id: int) -> Optional[Dict]:
        """
        Obtém um usuário pelo ID.

        Args:
            user_id (int): ID do usuário

        Returns:
            Optional[Dict]: Usuário como dicionário ou None se não encontrado
        """
        try:
            with get_db_session() as session:
                result = session.execute(select(User).where(User.id == user_id))
                user = result.scalars().first()
                return self._user_to_dict(user) if user else None
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao obter usuário por ID {user_id}: {e}")
            return None

    def get_by_username(self, username: str) -> Optional[Dict]:
        """
        Obtém um usuário pelo nome de usuário.

        Args:
            username (str): Nome de usuário

        Returns:
            Optional[Dict]: Usuário como dicionário ou None se não encontrado
        """
        try:
            with get_db_session() as session:
                result = session.execute(select(User).where(User.username == username))
                user = result.scalars().first()
                return self._user_to_dict(user) if user else None
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao obter usuário por username {username}: {e}")
            return None

    def get_by_email(self, email: str) -> Optional[Dict]:
        """
        Obtém um usuário pelo email.

        Args:
            email (str): Email do usuário

        Returns:
            Optional[Dict]: Usuário como dicionário ou None se não encontrado
        """
        try:
            with get_db_session() as session:
                result = session.execute(select(User).where(User.email == email))
                user = result.scalars().first()
                return self._user_to_dict(user) if user else None
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao obter usuário por email {email}: {e}")
            return None

    def create(self, data: Dict) -> Optional[Dict]:
        """
        Cria um novo usuário.

        Args:
            data (Dict): Dados do usuário
                - username: Nome de usuário (obrigatório)
                - email: Email (obrigatório)
                - full_name: Nome completo (obrigatório)
                - password: Senha em texto puro (obrigatório)
                - role: Papel/cargo (opcional)
                - profile_picture: Caminho da foto de perfil (opcional)

        Returns:
            Optional[Dict]: Usuário criado como dicionário ou None se falhar
        """
        try:
            # Verificar dados obrigatórios
            if not all(
                key in data for key in ["username", "email", "full_name", "password"]
            ):
                self.logger.error("Dados incompletos para criar usuário")
                return None

            # Gerar hash da senha
            password_hash, salt = User.hash_password(data["password"])

            # Criar objeto usuário
            user = User(
                username=data["username"],
                email=data["email"],
                full_name=data["full_name"],
                password_hash=password_hash,
                salt=salt,
                role=data.get("role", "user"),
                profile_picture=data.get("profile_picture"),
            )

            # Salvar no banco de dados
            with get_db_session() as session:
                session.add(user)
                session.commit()
                session.refresh(user)
                return self._user_to_dict(user)
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao criar usuário: {e}")
            return None

    def update(self, user_id: int, data: Dict) -> Optional[Dict]:
        """
        Atualiza um usuário existente.

        Args:
            user_id (int): ID do usuário
            data (Dict): Dados a atualizar

        Returns:
            Optional[Dict]: Usuário atualizado como dicionário ou None se falhar
        """
        try:
            with get_db_session() as session:
                # Obter usuário
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    self.logger.warning(
                        f"Usuário com ID {user_id} não encontrado para atualização"
                    )
                    return None

                # Atualizar campos
                if "username" in data:
                    user.username = data["username"]
                if "email" in data:
                    user.email = data["email"]
                if "full_name" in data:
                    user.full_name = data["full_name"]
                if "role" in data:
                    user.role = data["role"]
                if "profile_picture" in data:
                    user.profile_picture = data["profile_picture"]
                if "is_active" in data:
                    user.is_active = data["is_active"]
                if "password" in data:
                    user.password_hash, user.salt = User.hash_password(data["password"])

                session.commit()
                session.refresh(user)
                return self._user_to_dict(user)
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao atualizar usuário {user_id}: {e}")
            return None

    def delete(self, user_id: int) -> bool:
        """
        Exclui um usuário pelo ID.

        Args:
            user_id (int): ID do usuário

        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        try:
            with get_db_session() as session:
                user = session.query(User).filter(User.id == user_id).first()
                if not user:
                    self.logger.warning(
                        f"Usuário com ID {user_id} não encontrado para exclusão"
                    )
                    return False

                session.delete(user)
                session.commit()
                self.logger.info(f"Usuário {user_id} excluído com sucesso")
                return True
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao excluir usuário {user_id}: {e}")
            return False

    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """
        Autentica um usuário.

        Args:
            username (str): Nome de usuário
            password (str): Senha em texto puro

        Returns:
            Optional[Dict]: Usuário autenticado como dicionário ou None se falhar
        """
        try:
            with get_db_session() as session:
                user = User.authenticate(session, username, password)
                return self._user_to_dict(user) if user else None
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao autenticar usuário {username}: {e}")
            return None

    def _user_to_dict(self, user: User) -> Dict:
        """Converte um objeto User para dicionário."""
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "profile_picture": user.profile_picture,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }
