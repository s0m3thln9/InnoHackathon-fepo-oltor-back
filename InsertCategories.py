import sqlite3

def insert_categories():
    name = input("Введите название категории: ")

    db = sqlite3.connect('fepo.db')
    sql = db.cursor()

    sql.execute("""
    INSERT INTO categories (name)
    VALUES (?)
    """, (name,))

    db.commit()
    db.close()

while True:
    insert_categories()
    another = input("Хотите добавить еще 1 категорию (да/нет)? ").strip()
    if another != "да":
        print("Пока")
        break