import base64
import json

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

def save_data_to_db(name, email, password):
    try:
        db = sqlite3.connect('fepo.db')
        sql = db.cursor()

        hashed_password = hash_password(password)

        sql.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))

        db.commit()
    except sqlite3.IntegrityError as e:
        raise ValueError(f"A user with this email already exists")
    finally:
        db.close()

@app.route('/registration', methods=['POST'])
@cross_origin()
def registration_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'Отсутствует имя, адрес электронной почты или пароль'})

    try:
        save_data_to_db(name, email, password)
        return jsonify({'status': True, 'message': 'You have successfully registered.'})
    except ValueError as e:
        return jsonify({'status': False, 'message': str(e)})
    except Exception as e:
        return jsonify({'status': False, 'message': f'Error during registration: {e}'})

@app.route('/login', methods=['POST'])
@cross_origin()
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({
            'starus': False,
            'user': None,
            'message' : 'Missing email address or password'
        })

    with sqlite3.connect('fepo.db') as db:
        sql = db.cursor()
        sql.execute("SELECT name, password FROM users WHERE email = ?", (email,))
        user = sql.fetchone()

        if user:
            name, hashed_password = user
            if check_password(password, hashed_password):
                return jsonify({
                    'status': True,
                    'user': {
                        'email': email,
                        'name': name
                    },
                    'message': 'You have successfully logged in'
                })

        return jsonify({
            'status': False,
            'user': None,
            'message': 'Incorrect email or password'
        })

@app.route('/places', methods=['GET'])
@cross_origin()
def get_places():
    try:
        db = sqlite3.connect('fepo.db')
        sql = db.cursor()

        sql.execute("SELECT category, dates, name, rating, period, image, description, lat, lng, maxPeople FROM placess")
        places = sql.fetchall()

        places_list = []
        for place in places:
            category_json, dates_json, name, rating, period, image_blob, description, lat, lng, maxPeople = place
            category = json.loads(category_json) if category_json else []
            dates = json.loads(dates_json) if dates_json else []
            image_base64 = base64.b64encode(image_blob).decode('utf-8')
            place_data = {
                'coordinates': {
                    'lat': lat,
                    'lng': lng
                },
                'category': category,
                'dates': dates,
                'name': name,
                'rating': rating,
                'period': period,
                'description': description,
                'image': image_base64,
                'maxPeople': maxPeople
                }
            places_list.append(place_data)
        db.close()

        return jsonify({'places': places_list})
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})

@app.route('/people', methods=['GET'])
@cross_origin()
def get_people():
    try:
        db = sqlite3.connect('fepo.db')
        sql = db.cursor()

        sql.execute("SELECT category, name, rating, description, price, image FROM people")
        people = sql.fetchall()

        people_list = []
        for person in people:
            category, name, rating, description, price, image_blob = person
            image_base64 = base64.b64encode(image_blob).decode('utf-8')
            people_data = {
                'category': category,
                'name': name,
                'rating': rating,
                'description': description,
                'price': price,
                'image': image_base64
            }
            people_list.append(people_data)
        db.close()

        return jsonify({'people': people_list})
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})

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