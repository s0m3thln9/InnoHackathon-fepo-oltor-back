from flask import Flask, jsonify
from flask_cors import CORS
from .db_utils import get_all_places

app = Flask(__name__)
CORS(app)

@app.route('/places', methods=['GET'])
def get_places():
    return jsonify('places')
    try:
        places = get_all_places()
        return jsonify({'places': places})
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})
