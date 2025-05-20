#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exemplo de uso dos novos repositórios ORM SQLAlchemy.

Este script demonstra como usar os repositórios ORM em substituição
aos acessos diretos ao banco de dados.
"""

import sys
from pathlib import Path

# Adicionar diretório raiz ao path
sys.path.append(str(Path(__file__).parent.resolve()))

from database.orm.repositories.user_repository import UserRepository


def exemplo_crud_usuario():
    """Demonstra operações CRUD com o repositório de usuários."""
    repo = UserRepository()

    # Listar todos os usuários
    print("\n=== Listando todos os usuários ===")
    usuarios = repo.get_all()
    for usuario in usuarios:
        print(f"ID: {usuario.id}, Nome: {usuario.full_name}, Email: {usuario.email}")

    # Buscar usuário por ID
    print("\n=== Buscando usuário por ID ===")
    id_para_buscar = 1  # Altere conforme necessário
    usuario = repo.get_by_id(id_para_buscar)
    if usuario:
        print(f"Encontrado: ID: {usuario.id}, Nome: {usuario.full_name}")
    else:
        print(f"Usuário com ID {id_para_buscar} não encontrado")

    # Criar novo usuário
    print("\n=== Criando novo usuário ===")
    novo_usuario = {
        "username": "novo_usuario",
        "email": "novo@exemplo.com",
        "full_name": "Novo Usuário",
        "password": "senha_segura",
        "role": "editor",
    }

    # Verifique se o usuário já existe
    if not repo.get_by_username(novo_usuario["username"]):
        usuario_criado = repo.create(novo_usuario)
        if usuario_criado:
            print(
                f"Usuário criado: ID: {usuario_criado.id}, Username: {usuario_criado.username}"
            )
        else:
            print("Falha ao criar usuário")
    else:
        print(f"Usuário {novo_usuario['username']} já existe")

    # Atualizar usuário
    print("\n=== Atualizando usuário ===")
    dados_atualizacao = {"full_name": "Nome Atualizado", "role": "admin"}

    # Use o ID do usuário criado ou outro existente
    id_para_atualizar = usuario_criado.id if locals().get("usuario_criado") else 1
    usuario_atualizado = repo.update(id_para_atualizar, dados_atualizacao)

    if usuario_atualizado:
        print(
            f"Usuário atualizado: ID: {usuario_atualizado.id}, Nome: {usuario_atualizado.full_name}, Cargo: {usuario_atualizado.role}"
        )
    else:
        print(f"Falha ao atualizar usuário com ID {id_para_atualizar}")

    # Autenticar usuário
    print("\n=== Autenticando usuário ===")
    username = "novo_usuario"
    password = "senha_segura"
    usuario_autenticado = repo.authenticate(username, password)

    if usuario_autenticado:
        print(f"Autenticação bem-sucedida: {usuario_autenticado['username']}")
    else:
        print("Falha na autenticação")


if __name__ == "__main__":
    exemplo_crud_usuario()
