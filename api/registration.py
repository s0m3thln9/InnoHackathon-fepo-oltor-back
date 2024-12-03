from flask import Flask, request, jsonify
from flask_cors import CORS
from api.db_utils import save_data_to_db

app = Flask(__name__)
CORS(app)CORS(app, resources={r"/*": {"origins": "*"}})
@app.route('/api/registration', methods=['POST'])
def registration_user():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({'message': 'Missing name, email, or password'})

    try:
        save_data_to_db(name, email, password)
        return jsonify({'status': True, 'message': 'You have successfully registered.'})
    except ValueError as e:
        return jsonify({'status': False, 'message': str(e)})
    except Exception as e:
        return jsonify({'status': False, 'message': f'Error during registration: {e}'})

if __name__ == "__main__":
    app.run()