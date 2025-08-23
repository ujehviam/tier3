import sqlite3

Tier3 = "app.db"

def init_db():
    conn = sqlite3.connect(Tier3
)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect(Tier3
)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_table (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def get_user(username, password):
    conn = sqlite3.connect(Tier3
)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_table WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user

def list_user_table():
    conn = sqlite3.connect(Tier3
)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM user_table")
    user_table = cursor.fetchall()
    conn.close()
    return [u[0] for u in user_table]