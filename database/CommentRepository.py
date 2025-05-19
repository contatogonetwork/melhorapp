import uuid
import datetime
from database.Database import Database
from database.models.comment_model import Comment

class CommentRepository:
    """Repositório para operações com comentários de vídeo"""
    
    def __init__(self):
        """Inicializa o repositório com uma conexão ao banco de dados"""
        self.db = Database()
        
    def add_comment(self, comment, video_edit_id):
        """
        Adiciona um novo comentário para uma edição de vídeo
        
        Parâmetros:
        - comment: objeto Comment
        - video_edit_id: ID da edição de vídeo
        
        Retorna:
        - ID do comentário criado
        """
        # Gerar ID único se não fornecido
        if not comment.id:
            comment.id = str(uuid.uuid4())
        
        # Timestamp atual se não fornecido
        if not comment.timestamp:
            comment.timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Executar inserção
        self.db.execute(
            '''
            INSERT INTO video_comments (
                id, video_edit_id, user_id, timestamp, comment, is_resolved, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                comment.id,
                video_edit_id,
                comment.author,
                comment.video_timestamp,
                comment.text,
                1 if comment.is_resolved else 0,
                comment.timestamp
            )
        )
        
        # Salvar alterações
        self.db.commit()
        
        return comment.id
        
    def get_comments_by_editing(self, video_edit_id):
        """
        Busca todos os comentários de uma edição de vídeo específica
        
        Parâmetros:
        - video_edit_id: ID da edição de vídeo
        
        Retorna:
        - Lista de objetos Comment
        """
        results = self.db.fetch_all(
            '''
            SELECT c.*, u.name AS user_name
            FROM video_comments c
            LEFT JOIN team_members u ON c.user_id = u.id
            WHERE c.video_edit_id = ?
            ORDER BY c.timestamp ASC
            ''',
            (video_edit_id,)
        )
        
        comments = []
        for row in results:
            comment = Comment(
                id=row['id'],
                text=row['comment'],
                author=row.get('user_name', row['user_id']),
                timestamp=row['created_at'],
                video_timestamp=row['timestamp'],
                is_resolved=bool(row['is_resolved'])
            )
            comments.append(comment)
        
        return comments
        
    def resolve_comment(self, comment_id):
        """
        Marca um comentário como resolvido
        
        Parâmetros:
        - comment_id: ID do comentário
        
        Retorna:
        - True se atualizado com sucesso, False caso contrário
        """
        # Verificar se o comentário existe
        comment = self.db.fetch_one(
            'SELECT * FROM video_comments WHERE id = ?',
            (comment_id,)
        )
        
        if not comment:
            return False
        
        # Executar atualização
        self.db.execute(
            'UPDATE video_comments SET is_resolved = ? WHERE id = ?',
            (1, comment_id)
        )
        
        # Salvar alterações
        self.db.commit()
        
        return True
