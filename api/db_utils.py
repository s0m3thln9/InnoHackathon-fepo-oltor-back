import base64
import sqlite3
import json
import bcrypt

DATABASE = 'fepo.db'

def create_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

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
        
        places = []
        for row in rows:
            place = dict(zip(columns, row))
            if 'image' in place and place['image']:
                place['image'] = base64.b64encode(place['image']).decode('utf-8')
            places.append(place)

        return places


def get_all_people():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM people")
        rows = cursor.fetchall()
        
        people = []
        for row in rows:
            person = dict(zip([description[0] for description in cursor.description], row))
            # Преобразуем BLOB в Base64 для столбца с изображением
            if 'image' in person and person['image']:
                person['image'] = base64.b64encode(person['image']).decode('utf-8')
            people.append(person)

        return people

