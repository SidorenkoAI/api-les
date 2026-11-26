"""Урок 6. Консольный клиент доски станции: личный ключ API, чтение и отправка сообщений.

До сих пор мы только получали данные (GET). Сегодня отправляем свои (POST):
1) регистрируемся — POST /register с именем, сервер выдаёт личный ключ;
2) сохраняем ключ в файл key.txt, чтобы не регистрироваться при каждом запуске;
3) пишем на доску станции — POST /board, а ключ передаём в заголовке X-API-Key.

Доска общая для всего класса. Учитель показывает её на проекторе: /board.html
"""

import requests

BASE_URL = "https://api-lessons-sidorenkoai.msk1.amvera.tech"
KEY_FILE = "key.txt"


def explain(response):
    """Текст ошибки от сервера: главное сообщение и подробности, если они есть."""
    data = response.json()
    text = data["error"]
    for detail in data.get("details", []):
        text += f" ({detail['param']}: {detail['message']})"
    return text


def register():
    """Спрашивать имя, пока сервер не выдаст ключ. Вернуть ключ."""
    while True:
        name = input("Как тебя зовут (2–20 символов)? ").strip()
        # json= — словарь станет JSON в теле запроса
        response = requests.post(BASE_URL + "/register", json={"name": name}, timeout=10)
        if response.status_code == 201:  # 201 Created — «создано»
            data = response.json()
            print(data["message"])
            return data["api_key"]
        print(f"Не получилось (код {response.status_code}):", explain(response))


def load_key():
    """Взять ключ из файла. Если файла ещё нет — зарегистрироваться и сохранить ключ."""
    try:
        with open(KEY_FILE, encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        key = register()
        with open(KEY_FILE, "w", encoding="utf-8") as file:
            file.write(key)
        print(f"Ключ сохранён в файл {KEY_FILE}. Не показывай его никому!")
        return key


def show_board():
    """Последние 10 сообщений доски: старые сверху, новые снизу."""
    response = requests.get(BASE_URL + "/board", params={"limit": 10}, timeout=10)
    messages = response.json()["messages"]
    if not messages:
        print("На доске пока пусто. Напиши первым!")
    for message in messages:
        hour = message["time"][11:16]  # "2026-11-19T15:04:05" → "15:04"
        print(f"[{hour}] {message['author']}: {message['text']}")


def send(text):
    """Отправить сообщение на доску. Нужен ключ — он в заголовках."""
    response = requests.post(BASE_URL + "/board", json={"text": text}, headers=headers, timeout=10)
    if response.status_code == 201:
        print("Отправлено! Номер сообщения:", response.json()["id"])
    else:
        print(f"Ошибка {response.status_code}:", explain(response))


# ---------------------------------------------------------- 1. Ключ: из файла или регистрация
key = load_key()
headers = {"X-API-Key": key}

# ---------------------------------------------------------------- 2. Проверяем ключ
response = requests.get(BASE_URL + "/me", headers=headers, timeout=10)
if response.status_code != 200:
    print(f"Ключ не подходит (код {response.status_code}):", explain(response))
    print(f"Удали файл {KEY_FILE} и запусти программу снова — получишь новый ключ.")
    raise SystemExit
print(response.json()["message"])

# ------------------------------------------------------------------- 3. Меню
while True:
    print("\n1 — показать доску, 2 — написать сообщение, 0 — выход")
    choice = input("> ").strip()
    if choice == "1":
        show_board()
    elif choice == "2":
        send(input("Сообщение: "))
    elif choice == "0":
        print("До связи!")
        break
    else:
        print("Нет такого пункта")
