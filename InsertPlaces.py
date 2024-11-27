import sqlite3

def insert_place():
    name = input("Введите название места: ")
    rating = int(input("Введите рейтинг места (целое число): "))
    period = input("Введите период работы места (например, 08:00-22:00): ")
    image_path = input("Введите путь к изображению (например, image/example.jpg): ")
    description = input("Введите описание места: ")
    lat = float(input("Введите широту места (lat): "))
    lng = float(input("Введите долготу места (lng): "))

    try:
        with open(image_path, 'rb') as file:
            image_blob = file.read()
    except FileNotFoundError:
        print("Ошибка: Файл изображения не найден. Проверьте путь и попробуйте снова")
        return

    db = sqlite3.connect('fepo.db')
    sql = db.cursor()

    sql.execute("""
    INSERT INTO placess (name, rating, period, image, description, lat, lng)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, rating, period, image_blob, description, lat, lng))

    db.commit()
    db.close()

while True:
    insert_place()
    another = input("Хотите добавить еще 1 место (да/нет)? ").strip()
    if another != "да":
        print("Пока")
        break

