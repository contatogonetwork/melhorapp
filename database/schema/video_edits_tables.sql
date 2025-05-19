-- Tabela para armazenar as edições de vídeo
CREATE TABLE IF NOT EXISTS video_edits (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    editor_id TEXT NOT NULL,
    title TEXT NOT NULL,
    deadline TEXT NOT NULL,
    style TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'Em edição',
    video_path TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (editor_id) REFERENCES team_members(id)
);

-- Tabela para armazenar os comentários nos vídeos
CREATE TABLE IF NOT EXISTS video_comments (
    id TEXT PRIMARY KEY,
    video_edit_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    timestamp INTEGER NOT NULL,  -- Em segundos
    comment TEXT NOT NULL,
    is_resolved INTEGER NOT NULL DEFAULT 0,  -- 0=pendente, 1=resolvido
    created_at TEXT NOT NULL,
    FOREIGN KEY (video_edit_id) REFERENCES video_edits(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabela para armazenar as entregas dos editores
CREATE TABLE IF NOT EXISTS editor_deliveries (
    id TEXT PRIMARY KEY,
    video_edit_id TEXT NOT NULL,
    asset_refs TEXT,  -- Referências ou links para os assets
    is_submitted INTEGER NOT NULL DEFAULT 0,  -- 0=não, 1=sim
    submitted_at TEXT,
    approval_status TEXT NOT NULL DEFAULT 'Pendente',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (video_edit_id) REFERENCES video_edits(id)
);
