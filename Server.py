from flask import Flask, jsonify, request     # Фреймворк для создания веь-приложений и API
from flask_cors import CORS, cross_origin     # Решает проблему ограничения доступа к серверу из других доменов
import socket     # Библиотека используется для работы с сетевыми адресами и хостами
import sqlite3     # Библиотпка для работы с БД SQLite
import bcrypt     # Для хеширования и проверки паролей

# Cоздание экземпляра приложения Flask
# Creating a Flask Application Instance
app = Flask(__name__)

# Настройка CORS, чтобы разрешить доступ к API с определенных доменов
# Configure CORS to allow API access from specific domains
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})


# Функция для хеширования пароля
# Function for hashing a password
def hash_password(password):
    """
    Генерирует хеш для переданного пароля
    Generates a hash for the passed password

    :param password: Пароль в текстовом формате
    Password in text format

    :return: Хешированный пароль в строковом формате
    Hashed password in string format
    """
    # Генерация и хеширование пароля
    # Generating and hashing a password
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password.decode('utf-8')


# Функция для проверки пароля
# Function for checking password
def check_password(password, hashed_password):
    """
    Проверяет соответствие пароля и его хеша
    Checks if a password matches its hash

    :param password: Пароль в тестовом формате
    Password in test format

    :param hashed_password: Хеш пароля
    Password hash

    :return: True, если пароль корректный, иноче False
    True if the password is correct, otherwise False
    """
    # Приведение хеша к байтовому формату и сравнение его с паролем
    # Converting the hash to byte format and comparing it with the password
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


# Функция для сохранения данных в БД
# Function for saving data to the database
def save_data_to_db(name, email, password):
    """
    Сохраняет данные пользователя (имя, email и хеш пароля) в БД SQLite
    Stores user data (name, email and password hash) in a SQLite database

    :param name: Имя пользователя
    Username

    :param email: Email пользователя
    User email

    :param password: Пароль пользователя
    User password

    :return: Пользователь в БД
    User in DB
    """
    # Подключение к БД
    # Connecting to the DB
    db = sqlite3.connect('fepo.db')
    sql = db.cursor()

    # Хеширование пароля
    # Password Hashing
    hashed_password = hash_password(password)

    # Добавление данных пользователя в таблицу users
    # Adding user data to the users table
    sql.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))

    # Сохранение изменений и закрытие подключения к БД
    # Saving changes and closing the connection to the database
    db.commit()
    db.close()


# Маршрут для регистрации пользователя
# Route for user registration
@app.route('/registration', methods=['POST'])
@cross_origin()
def registration_user():
    """
    Обрабатывает запрос на регистрацию пользователя
    Processes a user registration request

    Ожидается JSON с полями:
    - name: Имя пользователя
    - email: Emaol пользователя
    - password: Пароль пользователя
    Expected JSON with fields:
    - name: Username
    - email: User's email
    - password: User's password

    :return: Сообщение о результации регистрации
    Registration result message
    """
    # Получение данных из тела запроса
    # Getting data from the request body
    data = request.json

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    # Проверка на наличие полей
    # Check for presence of fields
    if not name or not email or not password:
        return jsonify({'message': 'Отсутствует имя, адрес электронной почты или пароль'})

    # Сохранение данных в БД
    # Saving data to the database
    save_data_to_db(name, email, password)
    return jsonify({'message:': 'Вы успешно зарегистрировались'})


# Маршрут для входа пользователя
# User login route
@app.route('/login', methods=['POST'])
@cross_origin()
def login_user():
    """
    Обрабатывает запрос на вход пользователя
    Processes a user login request

    Ожидается JSON с полями:
    - email: Email пользователя
    - password: Пароль пользователя
    Expected JSON with fields:
    - email: User's email
    - password: User's password

    :return: Статус авторизации (True/False)
    Authorization status (True/False)
    """
    # Получение данных из тела запроса
    # Getting data from the request body
    data = request.json

    email = data.get('email')
    password = data.get('password')

    # Проверка на наличие всех полей
    # Checking if all fields are present
    if not email or not password:
        return jsonify({'message': 'Отсутствует адрес электронной почты или пароль'})

    with sqlite3.connect('fepo.db') as db:
        sql = db.cursor()

        # Поиск пользователя по email
        # Search user by email
        sql.execute("SELECT password FROM users WHERE email = ?", (email,))
        user = sql.fetchone()

        # Проверка пароля и возврат результата
        # Check password and return result
        if user and check_password(password, user[0]):
            return jsonify({'status': True})
        else:
            return jsonify({'status': False})


# Точка запуска
# Launch point
if __name__ == '__main__':
    """
    Запуск сервера Flask на локальном хосте
    Running Flask Server on Localhost
    """
    # Получение имени и IP хоста
    # Getting host name and IP
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print(f"Сервер работает на http://{ip_address}:4000")

    # Запуск сервера
    # Starting the server
    app.run(host='localhost', port=4000, debug=True)
