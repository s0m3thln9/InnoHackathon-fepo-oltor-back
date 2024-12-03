from flask import Flask, jsonify
from flask_cors import CORS
from .db_utils import get_all_people

app = Flask(__name__)
CORS(app)

@app.route('/people', methods=['GET'])
def get_people():
    try:
        people = get_all_people()
        return jsonify({'people': people})
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})
