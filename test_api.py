import requests
import json

API_URL = "https://script.google.com/macros/s/AKfycbxFHwCrriiLrTtUGUFsQ0HBYjI7SeiKOl_a9VqVdJ2GWfgjNKOM4uLzF-LK7CCZ4uGg/exec"

print("🔄 Запрос к API...")
response = requests.get(API_URL, timeout=15)

print(f"\n📊 Статус: {response.status_code}")
print(f"📏 Размер: {len(response.text)} символов\n")

if response.status_code == 200:
    data = response.json()

    # Показываем структуру
    print("=" * 80)
    print("📋 СТРУКТУРА ДАННЫХ:")
    print("=" * 80)
    print(f"Категории: {list(data.keys())}\n")

    # Жидкости
    liquids = data.get('liquids', [])
    print(f"💨 ЖИДКОСТИ: {len(liquids)} записей")
    if liquids:
        print("Первая запись:")
        print(json.dumps(liquids[0], ensure_ascii=False, indent=2))
        print()

    # Pod системы
    pods = data.get('pods', [])
    print(f"🔋 POD СИСТЕМЫ: {len(pods)} записей")
    if pods:
        print("Первая запись:")
        print(json.dumps(pods[0], ensure_ascii=False, indent=2))
        print()

    # Одноразки
    disposables = data.get('disposables', [])
    print(f"🎯 ОДНОРАЗКИ: {len(disposables)} записей")
    if disposables:
        print("Первая запись:")
        print(json.dumps(disposables[0], ensure_ascii=False, indent=2))
        print()

    # Расходники
    consumables = data.get('consumables', [])
    print(f"⚙️ РАСХОДНИКИ: {len(consumables)} записей")
    if consumables:
        print("Первая запись:")
        print(json.dumps(consumables[0], ensure_ascii=False, indent=2))
        print()

    # Сохраняем в файл
    with open('debug_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\n💾 Полные данные сохранены в: debug_data.json")

else:
    print(f"❌ Ошибка: {response.text[:500]}")