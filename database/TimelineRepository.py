import sqlite3
import uuid
from datetime import datetime

from .Database import Database
from utils.logger import get_logger


class TimelineRepository:
    """Operações CRUD para itens da timeline"""

    def __init__(self):
        """Inicializa o repositório da timeline com conexão ao banco de dados."""
        self.db = Database()
        self.logger = get_logger("timeline_repository")

    def generate_uuid(self):
        """
        Gera um UUID único para identificar registros

        Returns:
            str: UUID gerado em formato de string
        """
        return str(uuid.uuid4())

    def create_item(self, timeline_data):
        """
        Cria um novo item na timeline

        Args:
            timeline_data: Dicionário com os dados do item
                {event_id, title, description, start_time, end_time,
                 responsible_id, task_type, status, priority, color,
                 dependencies, location}

        Returns:
            str: ID do item criado

        Raises:
            sqlite3.Error: Em caso de erro no banco de dados
        """
        try:
            current_time = datetime.now().isoformat()

            query = """
            INSERT INTO timeline_items (
                id, event_id, title, description, start_time, end_time,
                responsible_id, task_type, status, priority, color,
                dependencies, location, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            item_id = self.generate_uuid()
            params = (
                item_id,
                timeline_data.get("event_id"),
                timeline_data.get("title"),
                timeline_data.get("description"),
                timeline_data.get("start_time"),
                timeline_data.get("end_time"),
                timeline_data.get("responsible_id"),
                timeline_data.get("task_type"),
                timeline_data.get("status", "Pendente"),
                timeline_data.get("priority", 2),
                timeline_data.get("color"),
                timeline_data.get("dependencies"),
                timeline_data.get("location"),
                current_time,
                current_time,
            )

            self.db.insert(query, params)
            return item_id
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao criar item na timeline: {e}")
            raise

    def get_by_id(self, item_id):
        """
        Busca um item da timeline pelo ID

        Args:
            item_id: ID do item

        Returns:
            dict: Dados do item ou None se não encontrado
        """
        try:
            query = "SELECT * FROM timeline_items WHERE id = ?"
            result = self.db.fetch_one(query, (item_id,))

            if result:
                return dict(result)
            return None
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao buscar item por ID: {e}")
            return None

    def get_by_event(self, event_id, filters=None):
        """
        Busca itens da timeline de um evento específico

        Args:
            event_id: ID do evento
            filters: Dicionário com filtros opcionais para refinar a busca
                    {responsible_id, task_type, status}

        Returns:
            list: Lista de dicionários com os dados dos itens
        """
        try:
            query = """
            SELECT
                ti.*,
                tm.name as responsible_name,
                e.name as event_name
            FROM timeline_items ti
            LEFT JOIN team_members tm ON ti.responsible_id = tm.id
            LEFT JOIN events e ON ti.event_id = e.id
            WHERE ti.event_id = ?
            """

            params = [event_id]

            if filters:
                if filters.get("responsible_id"):
                    query += " AND ti.responsible_id = ?"
                    params.append(filters["responsible_id"])

                if filters.get("task_type"):
                    query += " AND ti.task_type = ?"
                    params.append(filters["task_type"])

                if filters.get("status"):
                    query += " AND ti.status = ?"
                    params.append(filters["status"])

            query += " ORDER BY ti.start_time ASC"

            results = self.db.fetch_all(query, tuple(params))

            items = []
            for row in results:
                items.append(dict(row))

            return items
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao buscar itens por evento: {e}")
            return []

    def update(self, item_id, update_data):
        """
        Atualiza um item da timeline

        Args:
            item_id: ID do item
            update_data: Dicionário com os dados a serem atualizados

        Returns:
            bool: True se atualizado com sucesso, False caso contrário
        """
        try:
            set_clause = []
            params = []

            # Campos que podem ser atualizados
            fields = [
                "title",
                "description",
                "start_time",
                "end_time",
                "responsible_id",
                "task_type",
                "status",
                "priority",
                "color",
                "dependencies",
                "location",
            ]

            # Construir cláusula SET dinamicamente
            for field in fields:
                if field in update_data:
                    set_clause.append(f"{field} = ?")
                    params.append(update_data[field])

            # Adicionar updated_at
            set_clause.append("updated_at = ?")
            params.append(datetime.now().isoformat())

            # Adicionar ID ao final dos parâmetros
            params.append(item_id)

            query = f"""
            UPDATE timeline_items
            SET {', '.join(set_clause)}
            WHERE id = ?
            """

            self.db.execute_query(query, tuple(params))
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao atualizar item da timeline: {e}")
            return False

    def delete(self, item_id):
        """
        Exclui um item da timeline

        Args:
            item_id: ID do item

        Returns:
            bool: True se excluído com sucesso, False caso contrário
        """
        try:
            query = "DELETE FROM timeline_items WHERE id = ?"
            self.db.execute_query(query, (item_id,))
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao excluir item da timeline: {e}")
            return False

    def create_milestone(self, milestone_data):
        """
        Cria um novo marco na timeline

        Args:
            milestone_data: Dicionário com os dados do marco
                {event_id, title, description, milestone_time, importance}

        Returns:
            str: ID do marco criado
        """
        try:
            current_time = datetime.now().isoformat()

            query = """
            INSERT INTO timeline_milestones (
                id, event_id, title, description, milestone_time,
                importance, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """

            milestone_id = self.generate_uuid()
            params = (
                milestone_id,
                milestone_data.get("event_id"),
                milestone_data.get("title"),
                milestone_data.get("description"),
                milestone_data.get("milestone_time"),
                milestone_data.get("importance", 3),
                current_time,
            )

            self.db.insert(query, params)
            return milestone_id
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao criar marco na timeline: {e}")
            raise

    def get_milestones_by_event(self, event_id):
        """
        Busca marcos da timeline de um evento específico

        Args:
            event_id: ID do evento

        Returns:
            list: Lista de dicionários com os dados dos marcos
        """
        try:
            query = """
            SELECT
                tm.*,
                e.name as event_name
            FROM timeline_milestones tm
            LEFT JOIN events e ON tm.event_id = e.id
            WHERE tm.event_id = ?
            ORDER BY tm.milestone_time ASC
            """

            results = self.db.fetch_all(query, (event_id,))

            milestones = []
            for row in results:
                milestones.append(dict(row))

            return milestones
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao buscar marcos por evento: {e}")
            return []

    def add_notification(self, notification_data):
        """
        Adiciona uma notificação para um item da timeline

        Args:
            notification_data: Dicionário com os dados da notificação
                {timeline_item_id, notification_time, notification_type, message}

        Returns:
            str: ID da notificação criada
        """
        try:
            current_time = datetime.now().isoformat()

            query = """
            INSERT INTO timeline_notifications (
                id, timeline_item_id, notification_time, notification_type,
                message, sent, read, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """

            notification_id = self.generate_uuid()
            params = (
                notification_id,
                notification_data.get("timeline_item_id"),
                notification_data.get("notification_time"),
                notification_data.get("notification_type"),
                notification_data.get("message"),
                0,  # sent = false
                0,  # read = false
                current_time,
            )

            self.db.insert(query, params)
            return notification_id
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao criar notificação: {e}")
            raise

    def log_timeline_change(self, history_data):
        """
        Registra alteração em um item da timeline

        Args:
            history_data: Dicionário com os dados da alteração
                {timeline_item_id, changed_by, change_description,
                 previous_value, new_value, changed_field}

        Returns:
            str: ID do registro de histórico
        """
        try:
            current_time = datetime.now().isoformat()

            query = """
            INSERT INTO timeline_history (
                id, timeline_item_id, changed_by, change_description,
                previous_value, new_value, changed_field, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """

            history_id = self.generate_uuid()
            params = (
                history_id,
                history_data.get("timeline_item_id"),
                history_data.get("changed_by"),
                history_data.get("change_description"),
                history_data.get("previous_value"),
                history_data.get("new_value"),
                history_data.get("changed_field"),
                current_time,
            )

            self.db.insert(query, params)
            return history_id
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao registrar alteração na timeline: {e}")
            raise
