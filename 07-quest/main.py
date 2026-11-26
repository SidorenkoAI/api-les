"""Урок 7. Пульт квеста «Спасение станции»: показывает задание, отправляет ответы, берёт подсказки.

Пульт только общается с сервером. Сами ответы ищи и считай отдельными программами —
по одной на шаг (step1.py, step2.py…): данные для них — в разделах /planets, /aliens,
/weather и /board, а нужные числа — в задании и в его поле "data".

Ключ — тот же, что на уроке 6: скопируй файл key.txt в папку с этой программой.
Время идёт с момента, когда учитель нажал «Старт». Неверный ответ — +30 с, подсказка — +60 с.
Таблица лидеров на проекторе: /leaderboard.html
"""

import textwrap

import requests

BASE_URL = "https://api-lessons-sidorenkoai.msk1.amvera.tech"
KEY_FILE = "key.txt"


def load_key():
    """Ключ из файла; если файла нет — регистрация и сохранение ключа (как на уроке 6)."""
    try:
        with open(KEY_FILE, encoding="utf-8") as file:
            return file.read().strip()
    except FileNotFoundError:
        while True:
            name = input("Ключа нет. Как тебя зовут? ").strip()
            response = requests.post(BASE_URL + "/register", json={"name": name}, timeout=10)
            if response.status_code == 201:
                break
            print("Не получилось:", response.json()["error"])
        key = response.json()["api_key"]
        with open(KEY_FILE, "w", encoding="utf-8") as file:
            file.write(key)
        return key


def show_leaderboard():
    players = requests.get(BASE_URL + "/leaderboard", timeout=10).json()["players"]
    print("\n--- Таблица лидеров ---")
    for p in players[:10]:
        where = "финиш" if p["finished"] else f"шаг {p['step']}"
        print(f"{p['place']:>2}. {p['name']:<20} {where:<7} {p['time_text']}  (штраф {p['penalty']} с)")


headers = {"X-API-Key": load_key()}

while True:
    response = requests.get(BASE_URL + "/quest", headers=headers, timeout=10)
    if response.status_code == 409:  # квест ещё не начался
        print(response.json()["error"])
        if input("Enter — проверить снова, 0 — выход: ").strip() == "0":
            break
        continue
    if response.status_code != 200:
        print(f"Ошибка {response.status_code}:", response.json()["error"])
        break

    quest = response.json()
    if quest["status"] == "finished":
        print("\n" + quest["message"])
        show_leaderboard()
        break

    minutes, seconds = divmod(quest["time"], 60)
    print(f"\n=== Шаг {quest['step']} из {quest['total']}: {quest['title']} ===")
    print(textwrap.fill(quest["task"], width=90))  # длинный текст — по строкам до 90 символов
    print("Данные для программы:", quest["data"])
    if quest["hint"]:
        print("Подсказка:", quest["hint"])
    print(f"Время: {minutes:02d}:{seconds:02d}, из них штраф {quest['penalty']} с")

    answer = input("Ответ (? — подсказка, л — лидеры, 0 — выход): ").strip()
    if answer == "0":
        break
    elif answer == "?":
        hint = requests.post(BASE_URL + "/quest/hint", headers=headers, timeout=10).json()
        print(hint["message"])
    elif answer.lower() == "л":
        show_leaderboard()
    elif answer:
        result = requests.post(BASE_URL + "/quest/answer", json={"answer": answer}, headers=headers, timeout=10)
        if result.status_code == 200:
            print(result.json()["message"])
        else:
            print(f"Ошибка {result.status_code}:", result.json()["error"])
