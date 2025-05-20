import json
import os
import sqlite3
from datetime import datetime


class DatabaseManager:
    def __init__(self, db_path="./database/gonetwork.db"):
        # Garantir que o diretório existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = (
                sqlite3.Row
            )  # Para obter resultados como dicionários
            self.cursor = self.connection.cursor()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None

    def create_tables(self):
        self.connect()

        try:
            # Usuários
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    full_name TEXT,
                    role TEXT,
                    profile_picture TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Eventos
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    start_date DATETIME,
                    end_date DATETIME,
                    location TEXT,
                    client_id INTEGER,
                    status TEXT,
                    created_by INTEGER,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (client_id) REFERENCES users (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            """
            )

            # Equipe do Evento
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS event_team (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    user_id INTEGER,
                    role TEXT,
                    equipment TEXT,
                    FOREIGN KEY (event_id) REFERENCES events (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """
            )

            # Briefing
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS briefings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    general_info TEXT,
                    style_info TEXT,
                    references_info TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (event_id) REFERENCES events (id)
                )
            """
            )

            # Patrocinadores
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sponsors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    name TEXT NOT NULL,
                    FOREIGN KEY (event_id) REFERENCES events (id)
                )
            """
            )

            # Ações dos Patrocinadores
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sponsor_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sponsor_id INTEGER,
                    action_name TEXT NOT NULL,
                    capture_time TEXT,
                    is_free_time BOOLEAN,
                    responsible_id INTEGER,
                    is_real_time BOOLEAN,
                    delivery_time TEXT,
                    editor_id INTEGER,
                    instructions TEXT,
                    FOREIGN KEY (sponsor_id) REFERENCES sponsors (id),
                    FOREIGN KEY (responsible_id) REFERENCES users (id),
                    FOREIGN KEY (editor_id) REFERENCES users (id)
                )
            """
            )

            # Palcos
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS stages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    name TEXT NOT NULL,
                    FOREIGN KEY (event_id) REFERENCES events (id)
                )
            """
            )

            # Programação/Atrações
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS attractions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stage_id INTEGER,
                    name TEXT NOT NULL,
                    time TEXT,
                    notes TEXT,
                    FOREIGN KEY (stage_id) REFERENCES stages (id)
                )
            """
            )

            # Entregas Real Time
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS realtime_deliveries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    title TEXT NOT NULL,
                    delivery_time TEXT,
                    editor_id INTEGER,
                    platforms TEXT,
                    instructions TEXT,
                    FOREIGN KEY (event_id) REFERENCES events (id),
                    FOREIGN KEY (editor_id) REFERENCES users (id)
                )
            """
            )

            # Entregas Pós-Evento
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS post_deliveries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    deadline INTEGER,
                    deadline_unit TEXT,
                    has_aftermovie BOOLEAN,
                    has_highlights BOOLEAN,
                    has_sponsor_versions BOOLEAN,
                    notes TEXT,
                    FOREIGN KEY (event_id) REFERENCES events (id)
                )
            """
            )

            # Timeline
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS timeline_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    item_type TEXT,
                    reference_id INTEGER,
                    start_time TEXT,
                    end_time TEXT,
                    responsible_id INTEGER,
                    status TEXT,
                    FOREIGN KEY (event_id) REFERENCES events (id),
                    FOREIGN KEY (responsible_id) REFERENCES users (id)
                )
            """
            )

            # Vídeos/Edições
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS videos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    title TEXT NOT NULL,
                    description TEXT,
                    editor_id INTEGER,
                    status TEXT,
                    version TEXT,
                    file_path TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (event_id) REFERENCES events (id),
                    FOREIGN KEY (editor_id) REFERENCES users (id)
                )
            """
            )

            # Comentários em Vídeos
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS video_comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    video_id INTEGER,
                    user_id INTEGER,
                    comment TEXT,
                    timestamp TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (video_id) REFERENCES videos (id),
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            """
            )

            # Assets
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS assets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_id INTEGER,
                    name TEXT NOT NULL,
                    file_path TEXT,
                    asset_type TEXT,
                    category TEXT,
                    uploaded_by INTEGER,
                    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (event_id) REFERENCES events (id),
                    FOREIGN KEY (uploaded_by) REFERENCES users (id)
                )
            """
            )

            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao criar tabelas: {e}")
            return False
        finally:
            self.disconnect()

    # Métodos auxiliares para executar operações no banco de dados

    def execute_query(self, query, params=None):
        try:
            self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Erro ao executar consulta: {e}")
            return False
        finally:
            self.disconnect()

    def fetch_one(self, query, params=None):
        try:
            self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return dict(self.cursor.fetchone()) if self.cursor.fetchone() else None
        except sqlite3.Error as e:
            print(f"Erro ao buscar registro: {e}")
            return None
        finally:
            self.disconnect()

    def fetch_all(self, query, params=None):
        try:
            self.connect()
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Erro ao buscar registros: {e}")
            return []
        finally:
            self.disconnect()

    def insert(self, table, data):
        keys = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({keys}) VALUES ({placeholders})"

        try:
            self.connect()
            self.cursor.execute(query, values)
            last_id = self.cursor.lastrowid
            self.connection.commit()
            return last_id
        except sqlite3.Error as e:
            print(f"Erro ao inserir registro: {e}")
            return None
        finally:
            self.disconnect()

    def update(self, table, data, condition):
        set_values = ", ".join([f"{k} = ?" for k in data.keys()])
        where_clause = " AND ".join([f"{k} = ?" for k in condition.keys()])
        values = tuple(list(data.values()) + list(condition.values()))

        query = f"UPDATE {table} SET {set_values} WHERE {where_clause}"

        try:
            self.connect()
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao atualizar registro: {e}")
            return False
        finally:
            self.disconnect()

    def delete(self, table, condition):
        where_clause = " AND ".join([f"{k} = ?" for k in condition.keys()])
        values = tuple(condition.values())

        query = f"DELETE FROM {table} WHERE {where_clause}"

        try:
            self.connect()
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao deletar registro: {e}")
            return False
        finally:
            self.disconnect()
