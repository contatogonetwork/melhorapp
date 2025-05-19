from database.Database import Database

db = Database()
tables = db.fetch_all("""
    SELECT name FROM sqlite_master 
    WHERE type='table' AND (
        name='editor_deliveries' OR
        name='video_comments' OR
        name='editing_feedback' OR
        name='video_edits'
    )
""")

print('Tabelas de edição encontradas:', [t[0] for t in tables])
print('Status: ' + ('OK' if len(tables) >= 2 else 'INCOMPLETO'))
