# Arquivo de inicialização do pacote database
# Permite que os módulos sejam importados diretamente do pacote
from .BriefingRepository import BriefingRepository
from .Database import Database
from .EventRepository import EventRepository
from .TeamRepository import TeamRepository


# Para facilitar o uso do banco de dados em outros módulos
def get_database():
    """Retorna a instância do banco de dados"""
    return Database()
