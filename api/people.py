from flask import Flask, jsonify
from flask_cors import CORS
from api.db_utils import get_all_people

app = Flask(__name__)
CORS(app)

@app.route('/api/people', methods=['GET'])
def get_people():
    try:
        people = get_all_people()
        return jsonify({'people': people})
    except Exception as e:
        return jsonify({'status': False, 'message': str(e)})

if __name__ == "__main__":
    app.run()