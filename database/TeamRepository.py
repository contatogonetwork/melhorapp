from datetime import datetime

from .Database import Database


class TeamRepository:
    """Operações CRUD para membros da equipe e clientes"""

    def __init__(self):
        self.db = Database()

    # ===== Operações para Membros da Equipe =====

    def create_member(self, member_data):
        """
        Cria um novo membro da equipe

        Args:
            member_data: Dicionário com os dados do membro
                {name, role, email, contact}

        Returns:
            int: ID do membro criado
        """
        query = """
        INSERT INTO team_members (name, role, email, contact)
        VALUES (?, ?, ?, ?)
        """

        params = (
            member_data.get("name"),
            member_data.get("role"),
            member_data.get("email"),
            member_data.get("contact"),
        )

        return self.db.insert(query, params)

    def get_member_by_id(self, member_id):
        """
        Busca um membro da equipe pelo ID

        Args:
            member_id: ID do membro

        Returns:
            dict: Dados do membro ou None se não encontrado
        """
        query = "SELECT * FROM team_members WHERE id = ?"
        result = self.db.fetch_one(query, (member_id,))

        if result:
            return dict(result)
        return None

    def get_all_members(self):
        """
        Busca todos os membros da equipe

        Returns:
            list: Lista de dicionários com dados dos membros
        """
        query = "SELECT * FROM team_members ORDER BY name"
        results = self.db.fetch_all(query)

        members = []
        for row in results:
            members.append(dict(row))

        return members

    def update_member(self, member_id, member_data):
        """
        Atualiza um membro da equipe existente

        Args:
            member_id: ID do membro
            member_data: Dicionário com os dados atualizados

        Returns:
            bool: True se atualizado com sucesso
        """
        set_clause = []
        params = []

        fields = ["name", "role", "email", "contact"]

        for field in fields:
            if field in member_data:
                set_clause.append(f"{field} = ?")
                params.append(member_data[field])

        set_clause.append("updated_at = ?")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        params.append(member_id)

        query = f"""
        UPDATE team_members 
        SET {', '.join(set_clause)} 
        WHERE id = ?
        """

        cursor = self.db.execute_query(query, params)
        return cursor.rowcount > 0

    def delete_member(self, member_id):
        """
        Remove um membro da equipe

        Args:
            member_id: ID do membro

        Returns:
            bool: True se removido com sucesso
        """
        query = "DELETE FROM team_members WHERE id = ?"
        cursor = self.db.execute_query(query, (member_id,))
        return cursor.rowcount > 0

    def search_members(self, keyword):
        """
        Busca membros da equipe por palavra-chave

        Args:
            keyword: Palavra-chave para busca

        Returns:
            list: Lista de membros encontrados
        """
        search_term = f"%{keyword}%"
        query = """
        SELECT * FROM team_members 
        WHERE name LIKE ? 
           OR role LIKE ?
           OR email LIKE ?
           OR contact LIKE ?
        ORDER BY name
        """

        results = self.db.fetch_all(
            query, (search_term, search_term, search_term, search_term)
        )

        members = []
        for row in results:
            members.append(dict(row))

        return members

    def filter_members_by_role(self, role):
        """
        Filtra membros da equipe por função

        Args:
            role: Função dos membros

        Returns:
            list: Lista de membros com a função especificada
        """
        query = "SELECT * FROM team_members WHERE role = ? ORDER BY name"
        results = self.db.fetch_all(query, (role,))

        members = []
        for row in results:
            members.append(dict(row))

        return members

    # ===== Operações para Clientes =====

    def create_client(self, client_data):
        """
        Cria um novo cliente

        Args:
            client_data: Dicionário com os dados do cliente
                {company, contact_person, email, phone}

        Returns:
            int: ID do cliente criado
        """
        query = """
        INSERT INTO clients (company, contact_person, email, phone)
        VALUES (?, ?, ?, ?)
        """

        params = (
            client_data.get("company"),
            client_data.get("contact_person"),
            client_data.get("email"),
            client_data.get("phone"),
        )

        return self.db.insert(query, params)

    def get_client_by_id(self, client_id):
        """
        Busca um cliente pelo ID

        Args:
            client_id: ID do cliente

        Returns:
            dict: Dados do cliente ou None se não encontrado
        """
        query = "SELECT * FROM clients WHERE id = ?"
        result = self.db.fetch_one(query, (client_id,))

        if result:
            return dict(result)
        return None

    def get_all_clients(self):
        """
        Busca todos os clientes

        Returns:
            list: Lista de dicionários com dados dos clientes
        """
        query = "SELECT * FROM clients ORDER BY company"
        results = self.db.fetch_all(query)

        clients = []
        for row in results:
            clients.append(dict(row))

        return clients

    def update_client(self, client_id, client_data):
        """
        Atualiza um cliente existente

        Args:
            client_id: ID do cliente
            client_data: Dicionário com os dados atualizados

        Returns:
            bool: True se atualizado com sucesso
        """
        set_clause = []
        params = []

        fields = ["company", "contact_person", "email", "phone"]

        for field in fields:
            if field in client_data:
                set_clause.append(f"{field} = ?")
                params.append(client_data[field])

        set_clause.append("updated_at = ?")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        params.append(client_id)

        query = f"""
        UPDATE clients 
        SET {', '.join(set_clause)} 
        WHERE id = ?
        """

        cursor = self.db.execute_query(query, params)
        return cursor.rowcount > 0

    def delete_client(self, client_id):
        """
        Remove um cliente

        Args:
            client_id: ID do cliente

        Returns:
            bool: True se removido com sucesso
        """
        query = "DELETE FROM clients WHERE id = ?"
        cursor = self.db.execute_query(query, (client_id,))
        return cursor.rowcount > 0

    def search_clients(self, keyword):
        """
        Busca clientes por palavra-chave

        Args:
            keyword: Palavra-chave para busca

        Returns:
            list: Lista de clientes encontrados
        """
        search_term = f"%{keyword}%"
        query = """
        SELECT * FROM clients 
        WHERE company LIKE ? 
           OR contact_person LIKE ?
           OR email LIKE ?
           OR phone LIKE ?
        ORDER BY company
        """

        results = self.db.fetch_all(
            query, (search_term, search_term, search_term, search_term)
        )

        clients = []
        for row in results:
            clients.append(dict(row))

        return clients

    def get_clients_with_events(self):
        """
        Busca clientes que possuem eventos associados

        Returns:
            list: Lista de clientes com eventos
        """
        query = """
        SELECT DISTINCT c.* 
        FROM clients c
        JOIN events e ON c.id = e.client_id
        ORDER BY c.company
        """

        results = self.db.fetch_all(query)

        clients = []
        for row in results:
            clients.append(dict(row))

        return clients
