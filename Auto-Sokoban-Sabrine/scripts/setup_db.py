import sqlite3

def setup_db():
    conn = sqlite3.connect('sokoban_scores.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_id INTEGER,
            level INTEGER,
            moves INTEGER,
            time REAL,
            player_name TEXT
        )
    ''')
    conn.commit()
    conn.close()

setup_db()
