from flask import Flask, request, jsonify
from flask_cors import CORS
from api.db_utils import check_user_credentials

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://inno-hackathon-fepo-oltor-front.vercel.app"}})

@app.route('/api/login', methods=['POST'])
def login_user():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'status': False, 'user': None, 'message': 'Missing email or password'})

    user = check_user_credentials(email, password)
    if user:
        response = jsonify({'status': True, 'user': user, 'message': 'Login successful'})
        response.headers.add('Access-Control-Allow-Origin', 'https://inno-hackathon-fepo-oltor-front.vercel.app')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response
    
    response = jsonify({'status': False, 'user': None, 'message': 'Invalid email or password'})
    response.headers.add('Access-Control-Allow-Origin', 'https://inno-hackathon-fepo-oltor-front.vercel.app')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

@app.route('/api/login', methods=['OPTIONS'])
def handle_options():
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Origin', 'https://inno-hackathon-fepo-oltor-front.vercel.app')
    response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

if __name__ == "__main__":
    app.run()