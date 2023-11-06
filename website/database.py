import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_STRING = "database.db"

db_directory = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(db_directory, DB_STRING)

def setup_database():
    user_table = """ CREATE TABLE IF NOT EXISTS users ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        username TEXT NOT NULL,
        type TEXT
    );"""

    review_table = """ CREATE TABLE IF NOT EXISTS reviews ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        ratings TEXT NOT NULL,
        review TEXT NOT NULL
    );"""

    account1 = """INSERT OR IGNORE INTO users (email, password, username, type)
        VALUES (?, ?, ?, '0');
        """
    account2 = """INSERT OR IGNORE INTO users (email, password, username, type)
        VALUES (?, ?, ?, '0');
        """
    account3 = """INSERT OR IGNORE INTO users (email, password, username, type)
        VALUES (?, ?, ?, '0');
        """
    
    with sqlite3.connect(db_path) as con:
        con.execute(user_table)
        con.execute(review_table)

        con.execute(account1, ('conta1@ua.pt', generate_password_hash('conta12'), 'Jonas'))
        con.execute(account2, ('conta2@ua.pt', generate_password_hash('conta12'), 'Pedro'))
        con.execute(account3, ('conta3@ua.pt', generate_password_hash('conta12'), 'Lima'))


def cleanup_database():
    users_table = "DROP TABLE IF EXISTS users;"
    with sqlite3.connect(db_path) as con:
        con.execute(users_table)

def verify_user(user_email):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("""
            SELECT email FROM users;
        """)
        list_of_emails = cur.fetchall()
        for email in list_of_emails:
            email = email[0]
            if (email == user_email): 
                return True
        return False
    
def get_user_password(email):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("""
        SELECT password FROM users
        WHERE email = ?;
        """, (email,))
        user_password = cur.fetchall()[0]        
        return user_password[0]
    
def update_password(email, new_password):
    with sqlite3.connect(db_path) as con:
        con.execute("""
        UPDATE users
        SET password = ?
        WHERE email = ?;
        """, (generate_password_hash(new_password), email))
    
def get_username(email):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("""
        SELECT username FROM users
        WHERE email = ?;
        """, (email,))
        username = cur.fetchall()[0]
        return username[0]
    
def get_id(email):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute("""
        SELECT id FROM users
        WHERE email = ?;
        """, (email,))
        id = cur.fetchall()[0]
        return id[0]
    
def add_user(email, password, username):
    with sqlite3.connect(db_path) as con:
        con.execute("""
        INSERT INTO users (email, password, username)
        VALUES (?, ?, ?);
        """, (email, generate_password_hash(password), username))

def add_review(email, review, rating):
    with sqlite3.connect(db_path) as con:
        con.execute("""
        INSERT INTO reviews (email, ratings, review)
        VALUES (?, ?, ?);
        """, (email, rating, review))

def get_review(email):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT review, ratings FROM reviews
            WHERE email = '{email}';
            """)
        review = cur.fetchall()
        return review

def get_type(email):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT type FROM users
            WHERE email = '{email}';
            """)
        type = cur.fetchall()[0][0]
        return type

    
def get_admins():
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT email FROM users
            WHERE type = "0";
            """)
        emails = cur.fetchall()
        return emails
        