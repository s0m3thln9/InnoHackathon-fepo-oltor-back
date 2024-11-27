import sqlite3     # Модуль для работы с БД SQLite

def create_bd():
    """
    Создает БД SQLite и таблицу users, если она не существует
    Creates the SQLite database and the users table if it does not exist

    Таблица users имеет следующие поля:
    - id: Уникальный индентификатор пользователя
    - name: Имя пользователя (обязательное поле)
    - email: Email пользователя (уникальное и обязательное поле)
    - password: Хешированный пароль пользователя (обязательное поле)
    The users table has the following fields:
    - id: Unique user identifier
    - name: User name (required)
    - email: User email (unique and required)
    - password: Hashed password of the user (required)

    :return: Подключение к БД, Создание курсора для выполнения запросов, Выполнение запросов, Сохранение изменения в БД, Закрытие соединения с БД
    Connecting to a DB, Creating a Cursor to Run Queries, Running Queries, Saving Changes to a DB, Closing a DB Connection
    """
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

    db.commit()
    db.close()


# Точка запуска
# Launch point
if __name__ == '__main__':
    """
    Запускает функцию
    Runs the function
    """
    # Создание БД
    # Creating a DB
    create_bd()
    print("Таблица users успешно создана.")