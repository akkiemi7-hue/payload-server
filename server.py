from flask import Flask, request
import json
import os
from datetime import datetime

app = Flask(__name__)

# Создаем папку для логов
if not os.path.exists('logs'):
    os.makedirs('logs')

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    # Сохраняем в файл с временем
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"logs/data_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"[+] Сохранено: {filename}")
    return 'OK', 200

@app.route('/')
def index():
    return "Server running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
