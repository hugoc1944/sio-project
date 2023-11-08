import sqlite3
import os

DB_STRING = "databaseChat.db"

db_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_directory, DB_STRING)

def setup_databaseChat():
    user_table = """ CREATE TABLE IF NOT EXISTS conversations ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversationId TEXT NOT NULL,
        email TEXT NOT NULL,
        data TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );"""

    with sqlite3.connect(db_path) as con:
        con.execute(user_table)

def cleanup_databaseChat():
    users_table = "DROP TABLE IF EXISTS conversations;"
    with sqlite3.connect(db_path) as con:
        con.execute(users_table)

def get_chat_id(email):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT conversationID FROM conversations
        WHERE email = '{email}'
        """)
        conversation = cur.fetchall()
        return conversation
    
def add_conversation(conversation_id, email):
    with sqlite3.connect(db_path) as con:
        con.execute(f"""
        INSERT INTO conversations (conversationID, email)
        VALUES ('{conversation_id}','{email}');
        """)

def conversation_exists(conversation_id):
    
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT EXISTS(
            SELECT 1
            FROM conversations
            WHERE conversationId = '{conversation_id}'
        )
        """)
        result = cur.fetchone()[0]
        return bool(result)
    

def get_duplicate_key(user1, user2):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # SQL query to retrieve the duplicated key
    query = '''
    SELECT conversationID FROM conversations
    WHERE (email = ? OR email = ?) 
    GROUP BY conversationID HAVING COUNT(*) > 1;
    '''

    cursor.execute(query, (user1, user2))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    if result:
        return result[0]  # Return the duplicated key
    else:
        return None  # No duplicated key found
    
def get_users(conversation_id):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT email FROM conversations
        WHERE conversationID = '{conversation_id}'
        """)
        result = cur.fetchall()
        return result