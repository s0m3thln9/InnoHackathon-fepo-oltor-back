from flask import Flask, request, jsonify
from flask_cors import CORS
from db_utils import check_user_credentials

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': False, 'user': None, 'message': 'Missing email or password'})

    user = check_user_credentials(email, password)
    if user:
        return jsonify({'status': True, 'user': user, 'message': 'Login successful'})
    return jsonify({'status': False, 'user': None, 'message': 'Invalid email or password'})
