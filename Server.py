import base64

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
        return jsonify({'status': False, 'message' : 'Missing name, email or password'})

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

        sql.execute("SELECT name, rating, period, image, description, lat, lng FROM placess")
        places = sql.fetchall()

        places_list = []
        for place in places:
            name, rating, period, image_blob, description, lat, lng = place
            place_data = {
                'coordinates': {
                    'lat': lat,
                    'lng': lng
                },
                'title':{
                    'name': name,
                    'rating': rating,
                    'period': period,
                    'description': description,
                    'image': None
                }
            }
            if image_blob:
                place_data['title']['image'] = image_blob.decode('utf-8')

            places_list.append(place_data)
        db.close()

        return jsonify({'places': places_list})
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})


if __name__ == '__main__':
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print(f"Сервер работает на http://{ip_address}:4000")

    app.run(host='localhost', port=4000, debug=True)
