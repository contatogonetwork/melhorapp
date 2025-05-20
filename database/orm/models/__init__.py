"""
Pacote de modelos SQLAlchemy para GoNetwork AI.

Este pacote contém todos os modelos SQLAlchemy que representam as tabelas do banco de dados,
com suas relações e funcionalidades específicas.
"""

from database.orm.models.briefing import Briefing
from database.orm.models.client import Client
from database.orm.models.event import Event
from database.orm.models.event_team_members import event_team_members
from database.orm.models.team_member import TeamMember
from database.orm.models.user import User

__all__ = ["User", "Event", "TeamMember", "Client", "Briefing", "event_team_members"]
