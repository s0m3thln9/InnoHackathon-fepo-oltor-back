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

    db.commit()
    db.close()

if __name__ == '__main__':
    create_bd()
    print("Таблица users успешно создана.")