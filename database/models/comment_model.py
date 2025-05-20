class Comment:
    """Modelo para comentários em edições de vídeo"""

    def __init__(
        self,
        id=None,
        text="",
        author="",
        timestamp=None,
        video_timestamp=0,
        is_resolved=False,
    ):
        self.id = id
        self.text = text
        self.author = author
        self.timestamp = timestamp  # Quando foi postado
        self.video_timestamp = video_timestamp  # Posição do vídeo em ms
        self.is_resolved = is_resolved

    def to_dict(self):
        """Converte o objeto para um dicionário"""
        return {
            "id": self.id,
            "text": self.text,
            "author": self.author,
            "timestamp": self.timestamp,
            "video_timestamp": self.video_timestamp,
            "is_resolved": self.is_resolved,
        }

    @classmethod
    def from_dict(cls, data):
        """Cria um objeto Comment a partir de um dicionário"""
        return cls(
            id=data.get("id"),
            text=data.get("text", ""),
            author=data.get("author", ""),
            timestamp=data.get("timestamp"),
            video_timestamp=data.get("video_timestamp", 0),
            is_resolved=data.get("is_resolved", False),
        )
