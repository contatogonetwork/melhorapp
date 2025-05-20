import os
import sqlite3
from typing import Any, Dict, List, Tuple, Union

import streamlit as st


class Database:
    """
    Classe para gerenciar conexões com o banco de dados e executar consultas.
    Usa caching do Streamlit para otimizar consultas repetitivas.
    """

    @staticmethod
    def get_db_path() -> str:
        """
        Retorna o caminho para o arquivo de banco de dados.
        """
        # Caminho para o banco de dados principal
        main_db_path = os.path.join(
            os.path.dirname(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            ),
            "data",
            "gonetwork.db",
        )

        # Caminho alternativo no diretório de dados do aplicativo web
        alt_db_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "data",
            "gonetwork.db",
        )

        # Verifica qual caminho existe
        if os.path.exists(main_db_path):
            return main_db_path
        elif os.path.exists(alt_db_path):
            return alt_db_path
        else:
            # Se nenhum arquivo for encontrado, usa o caminho principal
            return main_db_path

    @staticmethod
    def connect():
        """
        Estabelece uma conexão com o banco de dados.
        """
        db_path = Database.get_db_path()

        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = (
                sqlite3.Row
            )  # Para retornar os resultados como dicionários
            return conn
        except sqlite3.Error as e:
            st.error(f"Erro ao conectar ao banco de dados: {e}")
            return None

    @staticmethod
    @st.cache_data(ttl=300)  # Cache por 5 minutos
    def execute_query(query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """
        Executa uma consulta SQL e retorna os resultados como uma lista de dicionários.
        Usa caching para consultas de leitura.
        """
        conn = Database.connect()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = [dict(row) for row in cursor.fetchall()]
            conn.close()
            return results
        except sqlite3.Error as e:
            st.error(f"Erro ao executar consulta: {e}")
            conn.close()
            return []

    @staticmethod
    def execute_write_query(query: str, params: Tuple = ()) -> bool:
        """
        Executa uma consulta SQL de escrita (INSERT, UPDATE, DELETE) e retorna True se bem-sucedido.
        """
        conn = Database.connect()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except sqlite3.Error as e:
            st.error(f"Erro ao executar operação de escrita: {e}")
            conn.rollback()
            conn.close()
            return False

    @staticmethod
    @st.cache_data(ttl=600)  # Cache por 10 minutos
    def get_table_names() -> List[str]:
        """
        Retorna a lista de tabelas disponíveis no banco de dados.
        """
        conn = Database.connect()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in cursor.fetchall()]
            conn.close()
            return tables
        except sqlite3.Error as e:
            st.error(f"Erro ao obter tabelas: {e}")
            conn.close()
            return []

    @staticmethod
    @st.cache_data(ttl=600)  # Cache por 10 minutos
    def get_table_columns(table_name: str) -> List[str]:
        """
        Retorna a lista de colunas para uma tabela específica.
        """
        conn = Database.connect()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [row[1] for row in cursor.fetchall()]
            conn.close()
            return columns
        except sqlite3.Error as e:
            st.error(f"Erro ao obter colunas da tabela {table_name}: {e}")
            conn.close()
            return []
