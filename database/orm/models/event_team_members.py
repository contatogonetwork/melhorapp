#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Modelo ORM para a tabela de associação entre eventos e membros da equipe.

Este módulo define o modelo SQLAlchemy para a tabela de associação
entre eventos e membros da equipe.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table

from database.orm.base import Base

# Tabela de associação para relacionamento muitos-para-muitos entre Event e TeamMember
event_team_members = Table(
    "event_team_members",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("team_member_id", Integer, ForeignKey("team_members.id"), primary_key=True),
    Column("role", String(50)),
    Column("created_at", DateTime, default=datetime.utcnow),
)
