#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe base para repositórios usando SQLAlchemy ORM.

Esta classe fornece funcionalidades comuns a todos os repositórios
para evitar duplicação de código.
"""

from typing import Any, Dict, List, Optional, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.orm.base import Base, get_db_session
from utils.logger import get_logger

# Tipo genérico para modelos
T = TypeVar("T", bound=Base)


class BaseRepository:
    """Classe base para repositórios usando SQLAlchemy ORM."""

    def __init__(self, model_class: Type[T]):
        """
        Inicializa o repositório com a classe do modelo.

        Args:
            model_class: Classe do modelo SQLAlchemy
        """
        self.model_class = model_class
        self.logger = get_logger(
            f"database.repositories.{model_class.__name__.lower()}"
        )

    def get_all(self) -> List[T]:
        """
        Obtém todos os registros.

        Returns:
            List[T]: Lista de todos os registros
        """
        try:
            with get_db_session() as session:
                result = session.execute(select(self.model_class))
                items = result.scalars().all()
                return list(items)
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao obter todos os registros: {e}")
            return []

    def get_by_id(self, id: int) -> Optional[T]:
        """
        Obtém um registro pelo ID.

        Args:
            id: ID do registro

        Returns:
            Optional[T]: Registro encontrado ou None se não existir
        """
        try:
            with get_db_session() as session:
                return session.get(self.model_class, id)
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao obter registro com ID {id}: {e}")
            return None

    def create(self, data: Dict[str, Any]) -> Optional[T]:
        """
        Cria um novo registro.

        Args:
            data: Dados para criar o registro

        Returns:
            Optional[T]: Registro criado ou None se falhar
        """
        try:
            with get_db_session() as session:
                # Criar nova instância do modelo
                instance = self.model_class(**data)
                session.add(instance)
                session.commit()
                session.refresh(instance)
                return instance
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao criar registro: {e}")
            return None

    def update(self, id: int, data: Dict[str, Any]) -> Optional[T]:
        """
        Atualiza um registro existente.

        Args:
            id: ID do registro
            data: Dados para atualizar

        Returns:
            Optional[T]: Registro atualizado ou None se não encontrado/falhar
        """
        try:
            with get_db_session() as session:
                instance = session.get(self.model_class, id)
                if not instance:
                    self.logger.warning(
                        f"Registro com ID {id} não encontrado para atualização"
                    )
                    return None

                # Atualizar atributos
                for key, value in data.items():
                    if hasattr(instance, key):
                        setattr(instance, key, value)

                session.commit()
                session.refresh(instance)
                return instance
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao atualizar registro com ID {id}: {e}")
            return None

    def delete(self, id: int) -> bool:
        """
        Exclui um registro pelo ID.

        Args:
            id: ID do registro

        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        try:
            with get_db_session() as session:
                instance = session.get(self.model_class, id)
                if not instance:
                    self.logger.warning(
                        f"Registro com ID {id} não encontrado para exclusão"
                    )
                    return False

                session.delete(instance)
                session.commit()
                self.logger.info(f"Registro com ID {id} excluído com sucesso")
                return True
        except SQLAlchemyError as e:
            self.logger.error(f"Erro ao excluir registro com ID {id}: {e}")
            return False
