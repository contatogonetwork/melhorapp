#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo ORM para a tabela de briefings.

Este módulo define o modelo SQLAlchemy para a tabela de briefings,
incluindo relações com eventos, clientes e membros da equipe.
"""

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database.orm.base import Base


class Briefing(Base):
    """Modelo SQLAlchemy para tabela de briefings."""

    __tablename__ = "briefings"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), index=True)
    project_name = Column(String(100), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), index=True)
    delivery_date = Column(DateTime)
    team_lead_id = Column(Integer, ForeignKey("team_members.id"), index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    event = relationship("Event", back_populates="briefings")
    client = relationship("Client", back_populates="briefings")
    team_lead = relationship("TeamMember", back_populates="briefings")
    sponsors = relationship(
        "Sponsor", back_populates="briefing", cascade="all, delete-orphan"
    )
    stages = relationship(
        "Stage", back_populates="briefing", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Representação em string do objeto."""
        return f"<Briefing(id={self.id}, project_name='{self.project_name}')>"
