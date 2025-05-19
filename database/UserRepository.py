# UserRepository.py
# Implementação do repositório de usuários

class UserRepository:
    def __init__(self, database_connection):
        self.connection = database_connection

    def create_user(self, username, password):
        cursor = self.connection.cursor()
        cursor.execute(
            """INSERT INTO users (username, password) VALUES (?, ?)""",
            (username, password)
        )
        self.connection.commit()

    def get_user(self, username):
        cursor = self.connection.cursor()
        cursor.execute(
            """SELECT * FROM users WHERE username = ?""",
            (username,)
        )
        return cursor.fetchone()

    def delete_user(self, username):
        cursor = self.connection.cursor()
        cursor.execute(
            """DELETE FROM users WHERE username = ?""",
            (username,)
        )
        self.connection.commit()
