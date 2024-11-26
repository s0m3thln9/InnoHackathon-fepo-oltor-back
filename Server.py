from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import socket

app = Flask(__name__)
CORS(app)  # Это базовая настройка CORS


@app.route('/api/data', methods=['GET'])
@cross_origin()  # Добавьте этот декоратор к вашему маршруту
def get_data():
    data = {"message": "Hello from Flask!"}
    return jsonify(data)


if __name__ == '__main__':
    # Получаем IP-адрес хоста
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    # Выводим IP-адрес в консоль
    print(f"Server is running on http://{ip_address}:80")

    # Запускаем сервер на 80 порту
    app.run(host='localhost', port=80, debug=True)
