#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Módulo de validação de entrada.

Este módulo fornece funções para validar diferentes tipos de entrada
para melhorar a segurança e integridade dos dados do aplicativo.
"""

import re
from typing import Any, Dict, List, Optional, Pattern, Union, cast


class InputValidator:
    """Classe para validação de entradas do usuário."""

    # Padrões regex comuns
    EMAIL_PATTERN: Pattern[str] = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )
    USERNAME_PATTERN: Pattern[str] = re.compile(r"^[a-zA-Z0-9_]{3,30}$")
    NAME_PATTERN: Pattern[str] = re.compile(r"^[a-zA-ZÀ-ÿ\s]{2,100}$")
    PHONE_PATTERN: Pattern[str] = re.compile(r"^\+?[0-9]{10,15}$")
    DATE_PATTERN: Pattern[str] = re.compile(
        r"^([0-9]{4})-([0-9]{2})-([0-9]{2})$"
    )  # YYYY-MM-DD
    TIME_PATTERN: Pattern[str] = re.compile(
        r"^([01]?[0-9]|2[0-3]):([0-5][0-9])$"
    )  # HH:MM
    FILENAME_PATTERN: Pattern[str] = re.compile(r"^[a-zA-Z0-9_.-]{1,255}$")

    @staticmethod
    def sanitize_string(value: str) -> str:
        """
        Sanitiza uma string removendo caracteres potencialmente perigosos.

        Args:
            value: String a ser sanitizada

        Returns:
            String sanitizada
        """
        if not value:
            return ""
        # Remove HTML tags e caracteres especiais
        value = re.sub(r"<[^>]*>", "", value)
        # Remove outros caracteres potencialmente perigosos
        value = re.sub(r"[^\w\s.,;:!?@#$%^&*()-=+\[\]{}|'\"<>/\\~`]", "", value)
        return value.strip()

    @classmethod
    def validate_email(cls, email: str) -> bool:
        """
        Valida se uma string é um endereço de email válido.

        Args:
            email: String do email para validar

        Returns:
            True se o email for válido, False caso contrário
        """
        if not email:
            return False
        return bool(cls.EMAIL_PATTERN.match(email))

    @classmethod
    def validate_username(cls, username: str) -> bool:
        """
        Valida se uma string é um nome de usuário válido.

        Apenas letras, números e underscore são permitidos,
        com tamanho entre 3 e 30 caracteres.

        Args:
            username: String do nome de usuário para validar

        Returns:
            True se o nome de usuário for válido, False caso contrário
        """
        if not username:
            return False
        return bool(cls.USERNAME_PATTERN.match(username))

    @classmethod
    def validate_name(cls, name: str) -> bool:
        """
        Valida se uma string é um nome válido.

        Apenas letras e espaços são permitidos, com tamanho entre 2 e 100 caracteres.

        Args:
            name: String do nome para validar

        Returns:
            True se o nome for válido, False caso contrário
        """
        if not name:
            return False
        return bool(cls.NAME_PATTERN.match(name))

    @staticmethod
    def validate_password_strength(password: str) -> Dict[str, Union[bool, str]]:
        """
        Valida a força de uma senha.

        Verifica o comprimento, presença de letras maiúsculas, minúsculas,
        números e caracteres especiais.

        Args:
            password: Senha para validar

        Returns:
            Dicionário contendo:
                - valid: True se a senha for válida, False caso contrário
                - message: Mensagem de erro (se houver)
                - strength: Força da senha (weak, medium, strong)
        """
        result = {"valid": True, "message": "", "strength": "weak"}

        # Verifica comprimento
        if len(password) < 8:
            result["valid"] = False
            result["message"] = "A senha deve ter pelo menos 8 caracteres"
            return cast(Dict[str, Union[bool, str]], result)

        # Verifica complexidade
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        # Calcula força
        strength_score = sum([has_upper, has_lower, has_digit, has_special])

        if strength_score == 4:
            result["strength"] = "strong"
        elif strength_score >= 2:
            result["strength"] = "medium"

        if strength_score < 2:
            result["valid"] = False
            result["message"] = (
                "A senha deve conter pelo menos dois tipos de caracteres diferentes"
            )

        return cast(Dict[str, Union[bool, str]], result)

    @staticmethod
    def validate_sql_input(value: str) -> bool:
        """
        Verifica se uma string contém possíveis ataques de SQL injection.

        Args:
            value: String para validar

        Returns:
            True se a string NÃO contiver padrões suspeitos, False caso contrário
        """
        if not value:
            return True

        suspicious_patterns = [
            r";\s*--",  # Comentários SQL
            r";\s*#",  # Comentários MySQL
            r"--",  # Comentário SQL
            r"/\*.*\*/",  # Comentário multi-linha
            r"DROP\s+TABLE",  # DROP TABLE
            r"ALTER\s+TABLE",  # ALTER TABLE
            r"DELETE\s+FROM",  # DELETE FROM
            r"INSERT\s+INTO",  # INSERT INTO
            r"UPDATE\s+.+\s+SET",  # UPDATE ... SET
            r"UNION\s+(ALL\s+)?SELECT",  # UNION SELECT
        ]

        for pattern in suspicious_patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return False

        return True
