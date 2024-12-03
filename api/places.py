from flask import Flask, jsonify
from flask_cors import CORS
from api.db_utils import get_all_places

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/api/places', methods=['GET'])
def get_places():
    print("Vercel endpoint /api/places called")
    try:
        places = get_all_places()
        return jsonify({'places': places})
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})

if __name__ == "__main__":
    app.run()
