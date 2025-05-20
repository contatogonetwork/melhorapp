#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo ORM para a tabela de clientes.

Este módulo define o modelo SQLAlchemy para a tabela de clientes,
incluindo relações com eventos e outras tabelas.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from database.orm.base import Base


class Client(Base):
    """Modelo SQLAlchemy para tabela de clientes."""

    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(100), nullable=False, index=True)
    contact_person = Column(String(100))
    email = Column(String(100), index=True)
    phone = Column(String(20))
    address = Column(String(255))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    events = relationship(
        "Event", back_populates="client", cascade="all, delete-orphan"
    )
    briefings = relationship("Briefing", back_populates="client")

    def __repr__(self) -> str:
        """Representação em string do objeto."""
        return f"<Client(id={self.id}, company='{self.company}')>"
