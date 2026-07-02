from flask import Flask, render_template, jsonify, request
import requests
import subprocess
import re
import threading
import time
import os

app = Flask(__name__)

# ⚠️ ВСТАВЬ СЮДА СВОЙ URL ИЗ APPS SCRIPT
import os
API_URL = os.environ.get('API_URL', 'https://script.google.com/macros/s/AKfycbxFHwCrriiLrTtUGUFsQ0HBYjI7SeiKOl_a9VqVdJ2GWfgjNKOM4uLzF-LK7CCZ4uGg/exec')
POD_SPECS = {
    "XROS 6": {"recommended_mg": "20-50mg (солевая)", "watts": "15-25W",
               "description": "Новейшая модель с регулировкой обдува"},
    "XROS 6 MINI": {"recommended_mg": "20-50mg (солевая)", "watts": "12-20W",
                    "description": "Компактная версия XROS 6"},
    "XROS 5": {"recommended_mg": "20-50mg (солевая)", "watts": "13-25W", "description": "Классическая модель"},
    "XROS 5 MINI": {"recommended_mg": "20-50mg (солевая)", "watts": "10-20W", "description": "Мини версия"},
    "XROS 5 LE": {"recommended_mg": "20-50mg (солевая)", "watts": "15-25W", "description": "Limited Edition"},
    "XROS 5 MINI LE": {"recommended_mg": "20-50mg (солевая)", "watts": "12-20W", "description": "Мини Limited Edition"},
    "XROS MINI KIT": {"recommended_mg": "20-50mg (солевая)", "watts": "8-15W",
                      "description": "Самая компактная модель"},
    "XROS 2 PRO": {"recommended_mg": "20-50mg (солевая)", "watts": "13-25W", "description": "Профессиональная версия"},
    "AEGIS FORCE": {"recommended_mg": "3-20mg (обычная)", "watts": "5-80W",
                    "description": "Мощный мод для свободной затяжки"},
    "GEEKVAPE HERO 5": {"recommended_mg": "3-20mg (обычная)", "watts": "5-80W", "description": "Флагманская модель"},
    "GEEKVAPE HERO 5 LE": {"recommended_mg": "3-20mg (обычная)", "watts": "5-80W", "description": "Limited Edition"},
}

CONSUMABLE_SPECS = {
    "Vaporesso XROS": {"recommended_mg": "20-50mg (солевая)", "watts": "10-25W",
                       "description": "Картриджи для POD систем XROS"},
    "SMOANT": {"recommended_mg": "3-20mg (обычная)", "watts": "50-65W",
               "description": "Испарители для Pasito 2,3 / Knight 80"},
    "GEEK VAPE": {"recommended_mg": "3-20mg (обычная)", "watts": "30-58W",
                  "description": "Испарители для Boost 2,3 / Hero 2,3,5"}
}


def get_catalog():
    try:
        response = requests.get(API_URL, timeout=30)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Ошибка: {e}")
        return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/catalog')
def api_catalog():
    catalog = get_catalog()
    if catalog:
        return jsonify({
            'success': True,
            'data': catalog,
            'pod_specs': POD_SPECS,
            'consumable_specs': CONSUMABLE_SPECS
        })
    return jsonify({'success': False, 'error': 'Не удалось загрузить каталог'}), 500


def start_ssh_tunnel(port):
    """Создание туннеля через localhost.run"""
    print("⏳ Создание SSH-туннеля через localhost.run...")

    process = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", f"80:127.0.0.1:{port}", "nokey@localhost.run"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace'
    )

    url_found = None
    for line in process.stdout:
        line = line.strip()
        if line:
            print(f"[SSH] {line}")

        if "https://" in line and "lhr.life" in line:
            match = re.search(r'https://[a-zA-Z0-9\-\.]+\.lhr\.life', line)
            if match:
                url_found = match.group(0)
                print(f"\n✅ Найден URL: {url_found}\n")
                break

    return url_found, process


if __name__ == "__main__":
    print("🚀 Запуск приложения...")

    PORT = 8550
    tunnel_info = {}


    def run_tunnel():
        url, proc = start_ssh_tunnel(PORT)
        tunnel_info['url'] = url
        tunnel_info['proc'] = proc


    t = threading.Thread(target=run_tunnel, daemon=True)
    t.start()

    print("⏳ Ожидание URL...")
    for _ in range(120):
        if 'url' in tunnel_info:
            break
        time.sleep(0.5)

    if 'url' not in tunnel_info or not tunnel_info['url']:
        print("❌ Не удалось получить ссылку")
        exit(1)

    url = tunnel_info['url']
    proc = tunnel_info['proc']

    print("=" * 60)
    print(f"✅ Ссылка: {url}")
    print("⚠️  Обнови в @BotFather!")
    print("=" * 60)

    print(f"\n🚀 Запуск Flask сервера на порту {PORT}...")
    try:
        app.run(host='127.0.0.1', port=PORT, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Остановка...")
    finally:
        if proc:
            proc.terminate()