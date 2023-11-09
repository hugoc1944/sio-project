import sqlite3
import os
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

    products_table = """ CREATE TABLE IF NOT EXISTS products ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quantity TEXT NOT NULL,
        stock BOOLEAN,
        description TEXT NOT NULL,
        name TEXT NOT NULL UNIQUE,
        file_path VARCHAR(255) NOT NULL,
        price TEXT NOT NULL,
        categories TEXT NOT NULL
    );"""

    carts_table = """CREATE TABLE IF NOT EXISTS carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        quantity TEXT NOT NULL,
        price TEXT NOT NULL,
        name TEXT NOT NULL,
        user TEXT NOT NULL
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
        con.execute(products_table)
        con.execute(carts_table)

        con.execute(account1, ('conta1@ua.pt', 'conta12', 'Jonas'))
        con.execute(account2, ('conta2@ua.pt', 'conta12', 'Pedro'))
        con.execute(account3, ('conta3@ua.pt', 'conta12', 'Lima'))


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
        cur.execute(f"""
        SELECT password FROM users
        WHERE email = '{email}';
        """)
        user_password = cur.fetchall()[0]        
        return user_password[0]

def check_password(email, password):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT 1 FROM users
        WHERE email = '{email}' AND password = '{password}';
        """)
        result = cur.fetchone()

        return result is not None
    
def update_password(email, new_password):
    with sqlite3.connect(db_path) as con:
        con.execute("""
        UPDATE users
        SET password = ?
        WHERE email = ?;
        """, (new_password, email))
    
def get_username(email):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT username FROM users
        WHERE email = '{email}';
        """)
        username = cur.fetchall()[0]
        return username[0]
    
def get_id(email):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
        SELECT id FROM users
        WHERE email = '{email}';
        """)
        id = cur.fetchall()[0]
        return id[0]
    
def add_user(email, password, username):
    with sqlite3.connect(db_path) as con:
        con.execute("""
        INSERT INTO users (email, password, username)
        VALUES (?, ?, ?);
        """, (email,password, username))

def add_review(email, review, rating):
    with sqlite3.connect(db_path) as con:
        con.execute("""
        INSERT INTO reviews (email, ratings, review)
        VALUES (?, ?, ?);
        """, (email, rating, review))

def get_review():
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT review, ratings FROM reviews
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

def get_products():
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT quantity, stock, description, name, file_path, price, categories FROM products;
            """)
        products = cur.fetchall()
        return products
    
def get_specific_products(categories):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT id, categories FROM products;
            """)
        products = cur.fetchall()
        ids = set()
        
        # Find products that match the specified categories
        for product in products:
            product_cat = product[1].upper().split(" ")
            for category in categories:
                if category in product_cat:
                    ids.add(product[0])
        if ids:
            # Create a comma-separated string of IDs
            ids_str = ",".join(map(str, ids))
            
            # Execute the query to retrieve products with matching IDs
            cur.execute(f"""
                SELECT quantity, stock, description, name, file_path, price, categories FROM products
                WHERE id IN ({ids_str});
            """)
            products = cur.fetchall()
            return products
        else:
            return []  # No matching products found
    
def add_products(quantity, stock, description, name, file_path, price, categories):
    with sqlite3.connect(db_path) as con:
        con.execute("""
        INSERT INTO products (quantity, stock, description, name, file_path, price, categories)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (quantity, stock, description, name, file_path, price, categories))

def get_products_by_name(name):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT quantity, stock, description, name, file_path, price, categories FROM products
            WHERE name = '{name}';
            """)
        products = cur.fetchone()
        return products
    
def get_product_quantity(name):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT quantity FROM products
            WHERE name = '{name}';
            """)
        quantity = cur.fetchone()[0]
        return quantity
    
def get_product_price(name):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT price FROM products
            WHERE name = '{name}';
            """)
        price = cur.fetchone()[0]
        return price
    
def update_quantity(name, quantity):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        beforeQ = get_product_quantity(name)
        quantity = int(beforeQ) - int(quantity)
        if quantity == 0:
            stock = 0
        else:
            stock = 1
        cur.execute(f"""
            UPDATE products
            SET quantity = '{quantity}', stock = '{stock}'
            WHERE name = '{name}'
            """)
        
def add_to_cart(name, quantity, user):
    with sqlite3.connect(db_path) as con:

        price = int(get_product_price(name)) * int(quantity)

        con.execute("""
        INSERT INTO carts (quantity, price, name, user)
        VALUES (?, ?, ?, ?);
        """, (quantity, price, name, user))

def get_cart(user):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            SELECT quantity, price, name FROM carts
            WHERE user = '{user}';
            """)
        cart = cur.fetchall()
        return cart
    
def remove_cart(quantity, name, user):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""
            DELETE FROM carts
            WHERE quantity = ? AND name = ? AND user = ?
            AND id = (SELECT id FROM carts WHERE quantity = ? AND name = ? AND user = ? LIMIT 1)
        """, (quantity, name, user, quantity, name, user))

def add_quantity(name, quantity):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        beforeQ = get_product_quantity(name)
        quantity = int(beforeQ) + int(quantity)
        stock = 1
        cur.execute(f"""
            UPDATE products
            SET quantity = '{quantity}', stock = '{stock}'
            WHERE name = '{name}'
            """)
        
def pay_cart(user):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(f"""DELETE FROM carts
            WHERE user = '{user}'
            """)