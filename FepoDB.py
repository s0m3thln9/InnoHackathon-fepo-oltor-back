import sqlite3
import json

def create_bd():
    db = sqlite3.connect('fepo.db')
    sql = db.cursor()

    sql.execute("""CREATE TABLE IF NOT EXISTS users (
    id_user INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT
    )""")
