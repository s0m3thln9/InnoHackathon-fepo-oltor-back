from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import socket
import sqlite3
import bcrypt

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def hash_password(password):
    salt = bcrypt.gensalt()
    hash_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hash_password.decode('utf-8')

def check_password(password, hashed_password):
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def save_data_to_db(name, email, password):
    db = sqlite3.connect('fepo.db')
    sql = db.cursor()

    hashed_password = hash_password(password)

    sql.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, hashed_password))

    db.commit()
    db.close()

@app.route('/registration', methods=['POST'])
@cross_origin()
def registration_user():
    data = request.json
    print(data)
    name = data.get('name')
    print(name)
    print(type(name))
    email = data.get('email')
    print(type(email))
    password = data.get('password')
    print(type(password))

    if not name or not email or not password:
        return jsonify({'message': 'Отсутствует имя, адрес электронной почты или пароль'})

    save_data_to_db(name, email, password)
    return jsonify({'message:': 'Вы успешно зарегистрировались'})

@app.route('/login', methods=['POST'])
@cross_origin()
def login_user():
    data = request.json
    print(data)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Отсутствует адрес электронной почты или пароль'})

    with sqlite3.connect('fepo.db') as db:
        sql = db.cursor()
        sql.execute("SELECT password FROM users WHERE email = ?", (email,))
        user = sql.fetchone()

        if user and check_password(password, user[0]):
            return jsonify({'status': True})
        else:
            return jsonify({'status': False})



if __name__ == '__main__':
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print(f"Сервер работает на http://{ip_address}:4000")

    app.run(host='localhost', port=4000, debug=True)
