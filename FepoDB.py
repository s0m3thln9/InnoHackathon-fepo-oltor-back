import sqlite3

def create_bd():
    db = sqlite3.connect('fepo.db')
    sql = db.cursor()

    sql.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    """)

    sql.execute("""
    CREATE TABLE IF NOT EXISTS placess (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rating INTEGER NOT NULL,
    period TEXT NOT NULL,
    image BLOB,
    description TEXT NOT NULL,
    lat REAL NOT NULL,
    lng REAL NOT NULL
    )""")

    sql.execute("""
    CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    rating INTEGER NOT NULL,
    description TEXT NOT NULL,
    image BLOB
    )""")

    db.commit()
    db.close()

if __name__ == '__main__':
    create_bd()
    print("Таблица users успешно создана.")


