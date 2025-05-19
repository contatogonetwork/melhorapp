-- Tabela para relacionamento muitos-para-muitos entre eventos e membros da equipe
CREATE TABLE IF NOT EXISTS event_team (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT NOT NULL,
    team_member_id TEXT NOT NULL,
    role TEXT,  -- Papel específico no evento (opcional)
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (team_member_id) REFERENCES team_members(id),
    UNIQUE(event_id, team_member_id)
);
