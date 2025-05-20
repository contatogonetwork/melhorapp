#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo ORM para a tabela de eventos.

Este módulo define o modelo SQLAlchemy para a tabela de eventos,
incluindo relações com outras tabelas.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from database.orm.base import Base


class Event(Base):
    """Modelo SQLAlchemy para tabela de eventos."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    date = Column(DateTime, nullable=False, index=True)
    location = Column(String(255))
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    type = Column(String(50))
    status = Column(String(50), default="planejamento")
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    client = relationship("Client", back_populates="events")
    briefings = relationship(
        "Briefing", back_populates="event", cascade="all, delete-orphan"
    )
    team_members = relationship(
        "TeamMember", secondary="event_team_members", back_populates="events"
    )
    timeline_items = relationship(
        "TimelineItem", back_populates="event", cascade="all, delete-orphan"
    )
    assets = relationship("Asset", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        """Representação em string do objeto."""
        return f"<Event(id={self.id}, name='{self.name}', date='{self.date}')>"
