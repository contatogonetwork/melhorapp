-- Tabela para armazenar os briefings dos eventos
CREATE TABLE IF NOT EXISTS briefings (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    project_name TEXT NOT NULL,
    client_id TEXT NOT NULL,
    delivery_date TEXT NOT NULL,
    team_lead_id TEXT,
    content TEXT,
    style_notes TEXT,
    reference_links TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (client_id) REFERENCES clients(id),
    FOREIGN KEY (team_lead_id) REFERENCES team_members(id)
);

-- Tabela para armazenar os patrocinadores do briefing
CREATE TABLE IF NOT EXISTS sponsors (
    id TEXT PRIMARY KEY,
    briefing_id TEXT NOT NULL,
    name TEXT NOT NULL,
    logo_path TEXT,
    contact_name TEXT,
    contact_email TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (briefing_id) REFERENCES briefings(id)
);

-- Tabela para armazenar as ações dos patrocinadores
CREATE TABLE IF NOT EXISTS sponsor_actions (
    id TEXT PRIMARY KEY,
    sponsor_id TEXT NOT NULL,
    description TEXT NOT NULL,
    visibility_notes TEXT,
    start_time TEXT,
    end_time TEXT,
    location_in_event TEXT,
    importance INTEGER DEFAULT 1, -- 1-5 para prioridade
    created_at TEXT NOT NULL,
    FOREIGN KEY (sponsor_id) REFERENCES sponsors(id)
);

-- Tabela para armazenar os palcos/locais do evento
CREATE TABLE IF NOT EXISTS stages (
    id TEXT PRIMARY KEY,
    briefing_id TEXT NOT NULL,
    name TEXT NOT NULL,
    location TEXT,
    capacity INTEGER,
    created_at TEXT NOT NULL,
    FOREIGN KEY (briefing_id) REFERENCES briefings(id)
);

-- Tabela para armazenar as atrações programadas
CREATE TABLE IF NOT EXISTS attractions (
    id TEXT PRIMARY KEY,
    stage_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    artist_name TEXT,
    tech_requirements TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (stage_id) REFERENCES stages(id)
);

-- Tabela para armazenar entregas em tempo real
CREATE TABLE IF NOT EXISTS realtime_deliveries (
    id TEXT PRIMARY KEY,
    briefing_id TEXT NOT NULL,
    description TEXT NOT NULL,
    platform TEXT NOT NULL, -- Instagram, YouTube, etc.
    delivery_time TEXT,
    responsible_id TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (briefing_id) REFERENCES briefings(id),
    FOREIGN KEY (responsible_id) REFERENCES team_members(id)
);

-- Tabela para armazenar entregas pós-evento
CREATE TABLE IF NOT EXISTS post_deliveries (
    id TEXT PRIMARY KEY,
    briefing_id TEXT NOT NULL,
    description TEXT NOT NULL,
    format TEXT NOT NULL, -- Vídeo, Foto, etc.
    deadline TEXT NOT NULL,
    responsible_id TEXT,
    notes TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (briefing_id) REFERENCES briefings(id),
    FOREIGN KEY (responsible_id) REFERENCES team_members(id)
);
