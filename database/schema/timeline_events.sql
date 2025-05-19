-- Tabela para armazenar eventos de timeline
CREATE TABLE IF NOT EXISTS timeline_items (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    responsible_id TEXT,
    task_type TEXT NOT NULL, -- Captação, Edição, Entrega, Aprovação, etc.
    status TEXT NOT NULL DEFAULT 'Pendente', -- Pendente, Em andamento, Concluído, Atrasado
    priority INTEGER DEFAULT 2, -- 1-5 para prioridade
    color TEXT, -- Código de cor hex para representação visual
    dependencies TEXT, -- IDs de outros itens dos quais este depende, em formato JSON
    location TEXT, -- Local onde a tarefa será realizada
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id),
    FOREIGN KEY (responsible_id) REFERENCES team_members(id)
);

-- Tabela para armazenar marcos importantes na timeline
CREATE TABLE IF NOT EXISTS timeline_milestones (
    id TEXT PRIMARY KEY,
    event_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    milestone_time TEXT NOT NULL,
    importance INTEGER DEFAULT 3, -- 1-5 para importância
    created_at TEXT NOT NULL,
    FOREIGN KEY (event_id) REFERENCES events(id)
);

-- Tabela para armazenar notificações da timeline
CREATE TABLE IF NOT EXISTS timeline_notifications (
    id TEXT PRIMARY KEY,
    timeline_item_id TEXT NOT NULL,
    notification_time TEXT NOT NULL,
    notification_type TEXT NOT NULL, -- Lembrete, Alerta, Emergência
    message TEXT NOT NULL,
    sent INTEGER DEFAULT 0, -- 0=não, 1=sim
    read INTEGER DEFAULT 0, -- 0=não, 1=sim
    created_at TEXT NOT NULL,
    FOREIGN KEY (timeline_item_id) REFERENCES timeline_items(id)
);

-- Tabela para armazenar histórico de alterações na timeline
CREATE TABLE IF NOT EXISTS timeline_history (
    id TEXT PRIMARY KEY,
    timeline_item_id TEXT NOT NULL,
    changed_by TEXT NOT NULL,
    change_description TEXT NOT NULL,
    previous_value TEXT,
    new_value TEXT,
    changed_field TEXT NOT NULL, -- Campo que foi alterado
    created_at TEXT NOT NULL,
    FOREIGN KEY (timeline_item_id) REFERENCES timeline_items(id),
    FOREIGN KEY (changed_by) REFERENCES users(id)
);
