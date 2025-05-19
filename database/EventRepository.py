from datetime import datetime
from .Database import Database

class EventRepository:
    """Operações CRUD para eventos"""
    
    def __init__(self):
        self.db = Database()
    
    def create(self, event_data):
        """
        Cria um novo evento
        
        Args:
            event_data: Dicionário com os dados do evento
                {name, date, location, client_id, type, status}
        
        Returns:
            int: ID do evento criado
        """
        query = '''
        INSERT INTO events (name, date, location, client_id, type, status)
        VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        params = (
            event_data.get('name'),
            event_data.get('date'),
            event_data.get('location'),
            event_data.get('client_id'),
            event_data.get('type'),
            event_data.get('status')
        )
        
        return self.db.insert(query, params)
    
    def get_by_id(self, event_id):
        """
        Busca um evento pelo ID
        
        Args:
            event_id: ID do evento
        
        Returns:
            dict: Dados do evento ou None se não encontrado
        """
        query = 'SELECT * FROM events WHERE id = ?'
        result = self.db.fetch_one(query, (event_id,))
        
        if result:
            return dict(result)
        return None
    
    def get_all(self):
        """
        Busca todos os eventos
        
        Returns:
            list: Lista de dicionários com dados dos eventos
        """
        query = 'SELECT * FROM events ORDER BY date DESC'
        results = self.db.fetch_all(query)
        
        events = []
        for row in results:
            events.append(dict(row))
        
        return events
    
    def update(self, event_id, event_data):
        """
        Atualiza um evento existente
        
        Args:
            event_id: ID do evento
            event_data: Dicionário com os dados atualizados
        
        Returns:
            bool: True se atualizado com sucesso
        """
        # Construir a consulta dinamicamente com base nos campos fornecidos
        set_clause = []
        params = []
        
        fields = ['name', 'date', 'location', 'client_id', 'type', 'status']
        
        for field in fields:
            if field in event_data:
                set_clause.append(f"{field} = ?")
                params.append(event_data[field])
        
        # Adicionar updated_at
        set_clause.append("updated_at = ?")
        params.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # Adicionar id ao final dos parâmetros
        params.append(event_id)
        
        query = f'''
        UPDATE events 
        SET {', '.join(set_clause)} 
        WHERE id = ?
        '''
        
        cursor = self.db.execute_query(query, params)
        return cursor.rowcount > 0
    
    def delete(self, event_id):
        """
        Remove um evento
        
        Args:
            event_id: ID do evento
        
        Returns:
            bool: True se removido com sucesso
        """
        query = 'DELETE FROM events WHERE id = ?'
        cursor = self.db.execute_query(query, (event_id,))
        return cursor.rowcount > 0
    
    def filter_by_status(self, status):
        """
        Filtra eventos por status
        
        Args:
            status: Status do evento
        
        Returns:
            list: Lista de eventos com o status especificado
        """
        query = 'SELECT * FROM events WHERE status = ? ORDER BY date DESC'
        results = self.db.fetch_all(query, (status,))
        
        events = []
        for row in results:
            events.append(dict(row))
        
        return events
    
    def filter_by_client(self, client_id):
        """
        Filtra eventos por cliente
        
        Args:
            client_id: ID do cliente
        
        Returns:
            list: Lista de eventos do cliente
        """
        query = 'SELECT * FROM events WHERE client_id = ? ORDER BY date DESC'
        results = self.db.fetch_all(query, (client_id,))
        
        events = []
        for row in results:
            events.append(dict(row))
        
        return events
    
    def find_upcoming_events(self, limit=5):
        """
        Busca os próximos eventos
        
        Args:
            limit: Número máximo de eventos a retornar
        
        Returns:
            list: Lista dos próximos eventos
        """
        today = datetime.now().strftime("%Y-%m-%d")
        query = f'''
        SELECT * FROM events 
        WHERE date >= ? 
        ORDER BY date ASC 
        LIMIT ?
        '''
        
        results = self.db.fetch_all(query, (today, limit))
        
        events = []
        for row in results:
            events.append(dict(row))
        
        return events
    
    def search(self, keyword):
        """
        Busca eventos por palavra-chave
        
        Args:
            keyword: Palavra-chave para busca
        
        Returns:
            list: Lista de eventos encontrados
        """
        search_term = f"%{keyword}%"
        query = '''
        SELECT * FROM events 
        WHERE name LIKE ? 
           OR location LIKE ?
           OR status LIKE ?
           OR type LIKE ?
        ORDER BY date DESC
        '''
        
        results = self.db.fetch_all(query, (search_term, search_term, search_term, search_term))
        
        events = []
        for row in results:
            events.append(dict(row))
        
        return events