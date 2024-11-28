import json
import sqlite3

def insert_place():
    category_id = input("Введите категории (id категории через запятую): ")
    category_list = [int(cat_id.strip()) for cat_id in category_id.split(',')]
    dates = input("Введите даты работы (через запятую, гггг-мм-дд: ")
    dates_list = [dates.strip() for dates in dates.split(',')]
    name = input("Введите название места: ")
    rating = int(input("Введите рейтинг места (целое число): "))
    period = input("Введите период работы места (например, 08:00-22:00): ")
    image_path = input("Введите путь к изображению (например, image/example.jpg): ")
    description = input("Введите описание места: ")
    lat = float(input("Введите широту места (lat): "))
    lng = float(input("Введите долготу места (lng): "))
    maxPeople = int(input("Введите вместимость места (целое число): "))

    try:
        with open(image_path, 'rb') as file:
            image_blob = file.read()
    except FileNotFoundError:
        print("Ошибка: Файл изображения не найден. Проверьте путь и попробуйте снова")
        return

    db = sqlite3.connect('fepo.db')
    sql = db.cursor()

    category_names = []
    for cat_id in category_list:
        sql.execute("SELECT name FROM categories WHERE id = ?", (cat_id,))
        category_name = sql.fetchone()
        if category_name:
            category_names.append(category_name[0])
        else:
            print(f"Категория с id {cat_id} не найден")


    sql.execute("""
    INSERT INTO placess (category, dates, name, rating, period, image, description, lat, lng, maxPeople)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (json.dumps(category_names), json.dumps(dates_list), name, rating, period, image_blob, description, lat, lng, maxPeople))

    db.commit()
    db.close()

while True:
    insert_place()
    another = input("Хотите добавить еще 1 место (да/нет)? ").strip()
    if another != "да":
        print("Пока")
        break




