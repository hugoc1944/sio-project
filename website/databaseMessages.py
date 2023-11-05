import sqlite3
import os

DB_STRING = "databaseChat.db"

db_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_directory, DB_STRING)

def setup_databaseMessages():
    user_table = """ CREATE TABLE IF NOT EXISTS messages ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversationId TEXT NOT NULL,
        sender TEXT NOT NULL,
        message TEXT NOT NULL,
        data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );"""

    with sqlite3.connect(db_path) as con:
        con.execute(user_table)

def cleanup_databaseMessages():
    users_table = "DROP TABLE IF EXISTS messages;"
    with sqlite3.connect(db_path) as con:
        con.execute(users_table)

def get_messages(conversation_id):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT sender, message FROM messages
        WHERE conversationID = '{conversation_id}'
        """)
        messages = cur.fetchall()
        return messages
    
def add_message(conversation_id, sender, message):
    with sqlite3.connect(db_path) as con:
        con.execute("""
        INSERT INTO messages (conversationID, sender, message)
        VALUES (?, ?, ?);
        """, (conversation_id, sender, message))