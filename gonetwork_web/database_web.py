import os
import sqlite3


def conectar_db():
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "gonetwork.db",
    )
    return sqlite3.connect(db_path)


def carregar_briefings():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT b.project_name, e.date, e.location FROM briefings b JOIN events e ON b.event_id = e.id"
    )
    resultados = cursor.fetchall()
    conn.close()
    return [{"nome_evento": r[0], "data": r[1], "local": r[2]} for r in resultados]


def carregar_timeline():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT ti.start_time, ti.end_time, ti.title,
               COALESCE(tm.name, 'Não atribuído') as responsible
        FROM timeline_items ti
        LEFT JOIN team_members tm ON ti.responsible_id = tm.id
        ORDER BY ti.start_time
        """
    )
    resultados = cursor.fetchall()
    conn.close()
    return [
        {"inicio": r[0], "fim": r[1], "titulo": r[2], "responsavel": r[3]}
        for r in resultados
    ]


def carregar_edicoes():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT tm.name, d.title, d.updated_at
        FROM deliverables d
        LEFT JOIN team_members tm ON d.id % (SELECT COUNT(*) FROM team_members) + 1 = tm.id
        WHERE d.title LIKE '%vídeo%' OR d.title LIKE '%video%'
        ORDER BY d.updated_at DESC
    """
    )
    resultados = cursor.fetchall()
    conn.close()
    return [{"editor": r[0], "video": r[1], "hora": r[2]} for r in resultados]
