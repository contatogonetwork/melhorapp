#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo ORM para a tabela de membros da equipe.

Este módulo define o modelo SQLAlchemy para a tabela de membros da equipe,
incluindo relações com eventos e outras tabelas.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from database.orm.base import Base


class TeamMember(Base):
    """Modelo SQLAlchemy para tabela de membros da equipe."""

    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    role = Column(String(50), index=True)
    email = Column(String(100), unique=True, index=True)
    contact = Column(String(50))
    bio = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    events = relationship(
        "Event", secondary="event_team_members", back_populates="team_members"
    )
    briefings = relationship("Briefing", back_populates="team_lead")
    timeline_items = relationship("TimelineItem", back_populates="responsible")

    def __repr__(self) -> str:
        """Representação em string do objeto."""
        return f"<TeamMember(id={self.id}, name='{self.name}', role='{self.role}')>"
