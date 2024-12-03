import sqlite3
import json
import bcrypt

DATABASE = 'fepo.db'

def create_connection():
    return sqlite3.connect('fepo.db')

def initialize_db():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS placess (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                dates TEXT NOT NULL,
                name TEXT NOT NULL,
                rating INTEGER NOT NULL,
                period TEXT NOT NULL,
                image BLOB,
                description TEXT NOT NULL,
                lat REAL NOT NULL,
                lng REAL NOT NULL,
                maxPeople INTEGER NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                name TEXT NOT NULL,
                rating INTEGER NOT NULL,
                description TEXT NOT NULL,
                price INTEGER NOT NULL,
                image BLOB
            )
        """)
        conn.commit()

def save_data_to_db(name, email, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            raise ValueError("User with this email already exists")

def check_user_credentials(email, password):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, password FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return {'email': email, 'name': user['name']}
        return None

def get_all_places():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM placess")
        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]
        places = [dict(zip(columns, row)) for row in rows]
        return places

def get_all_people():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
