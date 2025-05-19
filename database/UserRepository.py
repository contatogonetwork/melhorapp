# UserRepository.py
# Implementação do repositório de usuários

import sqlite3

from utils.logger import get_logger


class UserRepository:
    """
    Repositório para gerenciamento de usuários no banco de dados.

    Esta classe encapsula todas as operações de banco de dados relacionadas
    aos usuários, como criação, consulta e remoção.
    """

    def __init__(self, database_connection):
        """
        Inicializa o repositório de usuários.

        Args:
            database_connection: Conexão com o banco de dados SQLite
        """
        self.connection = database_connection
        self.logger = get_logger("user_repository")

    def create_user(self, username, password):
        """
        Cria um novo usuário no banco de dados.

        Args:
            username (str): Nome de usuário único
            password (str): Senha já criptografada

        Returns:
            int: ID do usuário criado

        Raises:
            sqlite3.IntegrityError: Se o nome de usuário já existe
            sqlite3.Error: Para outros erros de banco de dados
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """INSERT INTO users (username, password) VALUES (?, ?)""",
                (username, password),
            )
            self.connection.commit()
            self.logger.info(f"Usuário criado: {username}")
            return cursor.lastrowid
        except sqlite3.IntegrityError as e:
            self.logger.warning(
                f"Tentativa de criar usuário existente: {username}"
            )
            self.connection.rollback()
            raise
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao criar usuário: {str(e)}")
            self.connection.rollback()
            raise

    def get_user(self, username):
        """
        Busca um usuário pelo nome de usuário.

        Args:
            username (str): Nome de usuário a ser buscado

        Returns:
            dict: Dados do usuário ou None se não encontrado

        Raises:
            sqlite3.Error: Em caso de erro no banco de dados
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """SELECT * FROM users WHERE username = ?""", (username,)
            )
            return cursor.fetchone()
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao buscar usuário: {str(e)}")
            raise

    def delete_user(self, username):
        """
        Remove um usuário do banco de dados.

        Args:
            username (str): Nome do usuário a ser removido

        Returns:
            bool: True se o usuário foi removido, False se não existia

        Raises:
            sqlite3.Error: Em caso de erro no banco de dados
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """DELETE FROM users WHERE username = ?""", (username,)
            )
            self.connection.commit()

            if cursor.rowcount > 0:
                self.logger.info(f"Usuário removido: {username}")
                return True
            else:
                self.logger.warning(
                    f"Tentativa de remover usuário inexistente: {username}"
                )
                return False
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao remover usuário: {str(e)}")
            self.connection.rollback()
            raise

    def update_user_password(self, username, new_password):
        """
        Atualiza a senha de um usuário.

        Args:
            username (str): Nome do usuário
            new_password (str): Nova senha já criptografada

        Returns:
            bool: True se a senha foi atualizada, False se o usuário não existe

        Raises:
            sqlite3.Error: Em caso de erro no banco de dados
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                """UPDATE users SET password = ? WHERE username = ?""",
                (new_password, username),
            )
            self.connection.commit()

            if cursor.rowcount > 0:
                self.logger.info(f"Senha atualizada: {username}")
                return True
            else:
                self.logger.warning(
                    f"Usuário não encontrado para atualização: {username}"
                )
                return False
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao atualizar senha: {str(e)}")
            self.connection.rollback()
            raise
