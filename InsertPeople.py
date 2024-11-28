import sqlite3

def insert_people():
    category = input("Введите категорию человека (ведущий/фотограф): ")
    name = input("Введите имя человека: ")
    rating = input("Введите рейтинг (целое число): ")
    description = input("Введите описание данного человека: ")
    price = int(input("Введите цену услуги за час работы (целое число): "))
    image_path = input("Введите путь к изображению (например, image/example.jpg): ")

    try:
        with open(image_path, "rb") as file:
            image_blob = file.read()
    except FileNotFoundError:
        print("Ошибка: Файл изображения не найден. Проверьте путь и попробуйте снова")
        return

    db = sqlite3.connect("fepo.db")
    sql = db.cursor()

    sql.execute("""
    INSERT INTO people (category, name, rating, description, price, image)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (category, name, rating, description, price, image_blob))

    db.commit()
    db.close()

while True:
    insert_people()
    another = input("Хотите добавить еще 1 человека (да/нет)? ").strip()
    if another != "да":
        print("Пока")
        break