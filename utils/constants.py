# Status para eventos
EVENT_STATUS = {
    "SCHEDULED": "Agendado",
    "IN_PROGRESS": "Em andamento",
    "COMPLETED": "Finalizado",
    "ARCHIVED": "Arquivado",
    "CANCELED": "Cancelado"
}

# Status para entregas/vídeos
DELIVERY_STATUS = {
    "PENDING": "Pendente",
    "IN_PROGRESS": "Em andamento",
    "SUBMITTED": "Entregue para revisão",
    "IN_REVIEW": "Em revisão",
    "APPROVED": "Aprovada",
    "IN_REVISION": "Em alteração",
    "COMPLETED": "Concluída",
    "LATE": "Atrasada"
}

# Tipos de assets
ASSET_TYPES = {
    "IMAGE": "Imagem",
    "VIDEO": "Vídeo",
    "AUDIO": "Áudio",
    "LOGO": "Logo",
    "DOCUMENT": "Documento",
    "OTHER": "Outro"
}

# Categorias de assets
ASSET_CATEGORIES = {
    "SPONSOR": "Patrocinadores",
    "ARTIST": "Artistas",
    "MEDIA": "Mídia",
    "TEMPLATE": "Templates",
    "SOUNDTRACK": "Trilhas Sonoras",
    "EFFECT": "Efeitos",
    "OTHER": "Outros"
}

# Funções de equipe
TEAM_ROLES = {
    "COORDINATOR": "Coordenador",
    "CAMERAMAN": "Cinegrafista",
    "EDITOR": "Editor",
    "DRONE_OPERATOR": "Operador de Drone",
    "ASSISTANT": "Assistente",
    "PHOTOGRAPHER": "Fotógrafo",
    "AUDIO": "Áudio"
}

# Plataformas de mídia social
SOCIAL_PLATFORMS = {
    "REELS": "Reels",
    "STORIES": "Stories",
    "FEED": "Feed",
    "YOUTUBE": "YouTube",
    "TIKTOK": "TikTok",
    "OTHER": "Outros"
}

# Mensagens do sistema
MESSAGES = {
    "SUCCESS": {
        "EVENT_CREATED": "Evento criado com sucesso!",
        "EVENT_UPDATED": "Evento atualizado com sucesso!",
        "TEAM_UPDATED": "Equipe atualizada com sucesso!",
        "BRIEFING_SAVED": "Briefing salvo com sucesso!",
        "TIMELINE_GENERATED": "Timeline gerada com sucesso!",
        "VIDEO_UPLOADED": "Vídeo enviado com sucesso!",
        "COMMENT_ADDED": "Comentário adicionado com sucesso!",
        "ASSET_UPLOADED": "Asset enviado com sucesso!"
    },
    "ERROR": {
        "LOGIN_FAILED": "Falha no login. Verifique suas credenciais.",
        "EVENT_ERROR": "Erro ao processar o evento.",
        "UPLOAD_ERROR": "Erro ao fazer upload do arquivo.",
        "DATABASE_ERROR": "Erro ao acessar o banco de dados.",
        "PERMISSION_ERROR": "Você não tem permissão para esta ação.",
        "VALIDATION_ERROR": "Por favor, verifique os dados informados."
    },
    "INFO": {
        "SESSION_EXPIRED": "Sua sessão expirou. Por favor, faça login novamente.",
        "CONFIRM_DELETE": "Tem certeza que deseja excluir este item?",
        "TIMELINE_INFO": "A timeline é gerada com base nas informações do briefing."
    }
}