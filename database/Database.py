import logging
import os
import sqlite3
import threading
from pathlib import Path

from utils.logger import get_logger


class Database:
    """
    Singleton para gerenciar a conexão com o banco de dados SQLite
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Database, cls).__new__(cls)
                cls._instance._initialize()
            return cls._instance

    def _initialize(self):
        """
        Inicializa o banco de dados

        Configura o logger, cria o diretório de dados, estabelece a conexão
        e cria as tabelas necessárias.
        """
        # Configurar logger
        self.logger = get_logger("database")

        try:
            # Garantir que o diretório de dados exista
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)

            # Caminho do banco de dados
            self.db_path = data_dir / "gonetwork.db"

            # Conectar ao banco de dados
            self.connection = None
            self.connect()

            # Criar tabelas se não existirem
            self._create_tables()

            self.logger.info(
                f"Banco de dados inicializado com sucesso: {self.db_path}"
            )
        except Exception as e:
            self.logger.error(f"Erro ao inicializar banco de dados: {str(e)}")
            raise

    def connect(self):
        """
        Estabelece conexão com o banco de dados

        Returns:
            sqlite3.Connection: Conexão com o banco de dados
        """
        try:
            if self.connection is None:
                self.connection = sqlite3.connect(
                    self.db_path, check_same_thread=False
                )
                self.connection.row_factory = (
                    sqlite3.Row
                )  # Para acessar colunas pelo nome
                self.logger.debug("Conexão com banco de dados estabelecida")
            return self.connection
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
            raise

    def get_connection(self):
        """
        Retorna a conexão atual ou cria uma nova

        Returns:
            sqlite3.Connection: Conexão com o banco de dados
        """
        if self.connection is None:
            self.connect()
        return self.connection

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.logger.debug("Conexão com banco de dados fechada")

    def begin_transaction(self):
        """
        Inicia uma transação no banco de dados

        Returns:
            sqlite3.Connection: Conexão com o banco de dados em modo transação
        """
        conn = self.get_connection()
        conn.execute("BEGIN TRANSACTION")
        self.logger.debug("Transação iniciada")
        return conn

    def commit(self):
        """Confirma uma transação no banco de dados"""
        try:
            if self.connection:
                self.connection.commit()
                self.logger.debug("Transação confirmada (commit)")
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao confirmar transação: {str(e)}")
            raise

    def rollback(self):
        """Reverte uma transação no banco de dados"""
        try:
            if self.connection:
                self.connection.rollback()
                self.logger.debug("Transação revertida (rollback)")
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao reverter transação: {str(e)}")
            raise

    def _create_tables(self):
        """Cria as tabelas necessárias no banco de dados"""
        cursor = self.connection.cursor()

        # Tabela de eventos
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT,
            client_id INTEGER,
            type TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        """
        )

        # Tabela de membros da equipe
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS team_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            role TEXT,
            email TEXT,
            contact TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        # Tabela de clientes
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        )

        # Tabela de briefings
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS briefings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id INTEGER,
            project_name TEXT NOT NULL,
            client_id INTEGER,
            delivery_date TEXT,
            team_lead_id INTEGER,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (client_id) REFERENCES clients(id),
            FOREIGN KEY (team_lead_id) REFERENCES team_members(id)
        )
        """
        )

        # Tabela para entregas
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS deliverables (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            event_id INTEGER,
            client_id INTEGER,
            deadline TEXT,
            status TEXT,
            progress INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
        """
        )

        # Tabela para associar membros da equipe aos eventos
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS event_team_members (
            event_id INTEGER,
            team_member_id INTEGER,
            role TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (event_id, team_member_id),
            FOREIGN KEY (event_id) REFERENCES events(id),
            FOREIGN KEY (team_member_id) REFERENCES team_members(id)
        )
        """
        )

        # Tabela para assets/arquivos
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS assets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            path TEXT NOT NULL,
            type TEXT,
            event_id INTEGER,
            folder_path TEXT,
            size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (event_id) REFERENCES events(id)
        )
        """
        )

        self.connection.commit()

    def execute_query(self, query, parameters=()):
        """Executa uma consulta SQL e retorna os resultados"""
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        self.connection.commit()
        return cursor

    def fetch_all(self, query, parameters=()):
        """Executa uma consulta e retorna todos os resultados"""
        cursor = self.execute_query(query, parameters)
        return cursor.fetchall()

    def fetch_one(self, query, parameters=()):
        """Executa uma consulta e retorna um único resultado"""
        cursor = self.execute_query(query, parameters)
        return cursor.fetchone()

    def insert(self, query, parameters=()):
        """Insere dados e retorna o ID do novo registro"""
        cursor = self.execute_query(query, parameters)
        return cursor.lastrowid
