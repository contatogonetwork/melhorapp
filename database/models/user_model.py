import hashlib
import sqlite3

from database.Database import Database


class User:
    """Modelo de usuário com autenticação segura"""

    def __init__(self):
        self.id = None
        self.username = None
        self.email = None
        self.full_name = None
        self.role = None
        self.profile_picture = None

    def authenticate(self, username: str, password: str) -> bool:
        """
        Autentica o usuário verificando nome e senha com hash + salt.
        Retorna True se autenticado com sucesso, False caso contrário.
        """
        if not username or not password:
            return False

        try:
            db = Database()

            # Busca o salt do usuário
            query_salt = "SELECT salt FROM users WHERE username = ?"
            salt_result = db.fetch_one(query_salt, (username,))
            if not salt_result:
                return False

            salt = salt_result[0]
            hashed_password = self._hash_password(password, salt)

            # Verifica credenciais com hash calculado
            query = """
                SELECT id, username, email, full_name, role, profile_picture
                FROM users
                WHERE username = ? AND password_hash = ?
            """
            result = db.fetch_one(query, (username, hashed_password))

            if result:
                (
                    self.id,
                    self.username,
                    self.email,
                    self.full_name,
                    self.role,
                    self.profile_picture,
                ) = result
                return True
            return False

        except sqlite3.Error as e:
            print(f"[ERRO] Autenticação falhou: {e}")
            return False

        finally:
            if "db" in locals():
                db.close()

    def _hash_password(self, password: str, salt: str) -> str:
        """
        Cria um hash SHA-256 da senha combinada com o salt.
        """
        password_salt = password + salt
        return hashlib.sha256(password_salt.encode("utf-8")).hexdigest()

    def __repr__(self):
        return f"<User {self.username} - {self.role}>"
