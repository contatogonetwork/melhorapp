#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utilitários para autenticação e segurança
"""

import bcrypt

from utils.logger import get_logger

logger = get_logger("auth")


def hash_password(password: str) -> str:
    """
    Gera um hash seguro para a senha usando bcrypt

    Args:
        password: Senha em texto plano

    Returns:
        str: Hash da senha em formato string
    """
    if not password:
        logger.error("Tentativa de hash de senha vazia")
        raise ValueError("A senha não pode ser vazia")

    # Gera um salt e hasheia a senha
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)

    # Retorna o hash como string
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha em texto plano corresponde ao hash armazenado

    Args:
        plain_password: Senha em texto plano para verificar
        hashed_password: Hash da senha armazenado

    Returns:
        bool: True se a senha for válida, False caso contrário
    """
    if not plain_password or not hashed_password:
        logger.warning("Tentativa de validação com senha ou hash vazios")
        return False

    try:
        # Converte as strings para bytes
        plain_password_bytes = plain_password.encode("utf-8")
        hashed_password_bytes = hashed_password.encode("utf-8")

        # Verifica se as senhas correspondem
        return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)
    except Exception as e:
        logger.error(f"Erro ao verificar senha: {str(e)}")
        return False


def sanitize_input(input_str: str) -> str:
    """
    Sanitiza entrada de texto para evitar injeção SQL e outros ataques

    Args:
        input_str: String a ser sanitizada

    Returns:
        str: String sanitizada
    """
    if input_str is None:
        return ""

    # Remove caracteres perigosos
    sanitized = input_str.replace("'", "''")  # Escape SQL single quotes

    # Outras sanitizações podem ser adicionadas conforme necessário

    return sanitized
