from datetime import datetime

from .Database import Database


class BriefingRepository:
    """Operações CRUD para briefings"""

    def __init__(self):
        self.db = Database()

    def create(self, briefing_data):
        """
        Cria um novo briefing

        Args:
            briefing_data: Dicionário com os dados do briefing
                {event_id, project_name, client_id, delivery_date, team_lead_id, content}

        Returns:
            int: ID do briefing criado
        """
        query = """
        INSERT INTO briefings (
            event_id, project_name, client_id, delivery_date, team_lead_id, content
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """

        params = (
            briefing_data.get("event_id"),
            briefing_data.get("project_name"),
            briefing_data.get("client_id"),
            briefing_data.get("delivery_date"),
            briefing_data.get("team_lead_id"),
            briefing_data.get("content"),
        )

        return self.db.insert(query, params)

    def get_by_id(self, briefing_id):
        """
        Busca um briefing pelo ID

        Args:
            briefing_id: ID do briefing

        Returns:
            dict: Dados do briefing ou None se não encontrado
        """
        query = "SELECT * FROM briefings WHERE id = ?"
        result = self.db.fetch_one(query, (briefing_id,))

        if result:
            return dict(result)
        return None

    def get_all(self):
        """
        Busca todos os briefings

        Returns:
            list: Lista de dicionários com dados dos briefings
        """
        query = """
        SELECT 
            b.*,
            e.name as event_name,
            c.company as client_name,
            tm.name as team_lead_name
        FROM briefings b
        LEFT JOIN events e ON b.event_id = e.id
        LEFT JOIN clients c ON b.client_id = c.id
        LEFT JOIN team_members tm ON b.team_lead_id = tm.id
        ORDER BY b.created_at DESC
        """
        results = self.db.fetch_all(query)

        briefings = []
        for row in results:
            briefings.append(dict(row))

        return briefings

    def update(self, briefing_id, briefing_data):
        """
        Atualiza um briefing existente

        Args:
            briefing_id: ID do briefing
            briefing_data: Dicionário com os dados atualizados

        Returns:
            bool: True se atualizado com sucesso
        """
        set_clause = []
        params = []

        fields = [
            "event_id",
            "project_name",
            "client_id",
            "delivery_date",
            "team_lead_id",
            "content",
        ]

        for field in fields:
            if field in briefing_data:
                set_clause.append(f"{field} = ?")
                params.append(briefing_data[field])

        set_clause.append("updated_at = ?")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        params.append(briefing_id)

        query = f"""
        UPDATE briefings 
        SET {', '.join(set_clause)} 
        WHERE id = ?
        """

        cursor = self.db.execute_query(query, params)
        return cursor.rowcount > 0

    def delete(self, briefing_id):
        """
        Remove um briefing

        Args:
            briefing_id: ID do briefing

        Returns:
            bool: True se removido com sucesso
        """
        query = "DELETE FROM briefings WHERE id = ?"
        cursor = self.db.execute_query(query, (briefing_id,))
        return cursor.rowcount > 0

    def get_by_event_id(self, event_id):
        """
        Busca briefings associados a um evento

        Args:
            event_id: ID do evento

        Returns:
            list: Lista de briefings do evento
        """
        query = """
        SELECT 
            b.*,
            e.name as event_name,
            c.company as client_name,
            tm.name as team_lead_name
        FROM briefings b
        LEFT JOIN events e ON b.event_id = e.id
        LEFT JOIN clients c ON b.client_id = c.id
        LEFT JOIN team_members tm ON b.team_lead_id = tm.id
        WHERE b.event_id = ?
        ORDER BY b.created_at DESC
        """

        results = self.db.fetch_all(query, (event_id,))

        briefings = []
        for row in results:
            briefings.append(dict(row))

        return briefings

    def get_by_client_id(self, client_id):
        """
        Busca briefings associados a um cliente

        Args:
            client_id: ID do cliente

        Returns:
            list: Lista de briefings do cliente
        """
        query = """
        SELECT 
            b.*,
            e.name as event_name,
            c.company as client_name,
            tm.name as team_lead_name
        FROM briefings b
        LEFT JOIN events e ON b.event_id = e.id
        LEFT JOIN clients c ON b.client_id = c.id
        LEFT JOIN team_members tm ON b.team_lead_id = tm.id
        WHERE b.client_id = ?
        ORDER BY b.created_at DESC
        """

        results = self.db.fetch_all(query, (client_id,))

        briefings = []
        for row in results:
            briefings.append(dict(row))

        return briefings

    def get_recent_briefings(self, limit=5):
        """
        Busca os briefings mais recentes

        Args:
            limit: Número máximo de briefings a retornar

        Returns:
            list: Lista dos briefings mais recentes
        """
        query = """
        SELECT 
            b.*,
            e.name as event_name,
            c.company as client_name,
            tm.name as team_lead_name
        FROM briefings b
        LEFT JOIN events e ON b.event_id = e.id
        LEFT JOIN clients c ON b.client_id = c.id
        LEFT JOIN team_members tm ON b.team_lead_id = tm.id
        ORDER BY b.created_at DESC
        LIMIT ?
        """

        results = self.db.fetch_all(query, (limit,))

        briefings = []
        for row in results:
            briefings.append(dict(row))

        return briefings

    def search(self, keyword):
        """
        Busca briefings por palavra-chave

        Args:
            keyword: Palavra-chave para busca

        Returns:
            list: Lista de briefings encontrados
        """
        search_term = f"%{keyword}%"
        query = """
        SELECT 
            b.*,
            e.name as event_name,
            c.company as client_name,
            tm.name as team_lead_name
        FROM briefings b
        LEFT JOIN events e ON b.event_id = e.id
        LEFT JOIN clients c ON b.client_id = c.id
        LEFT JOIN team_members tm ON b.team_lead_id = tm.id
        WHERE b.project_name LIKE ? 
           OR b.content LIKE ?
           OR e.name LIKE ?
           OR c.company LIKE ?
        ORDER BY b.created_at DESC
        """

        results = self.db.fetch_all(
            query, (search_term, search_term, search_term, search_term)
        )

        briefings = []
        for row in results:
            briefings.append(dict(row))

        return briefings
