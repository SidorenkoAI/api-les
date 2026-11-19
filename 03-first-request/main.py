"""Урок 3. Первый запрос к API: «Справочник галактики» берёт данные с сервера.

Данные о планетах больше не лежат у нас в файле — их присылает сервер в интернете.
Нужна библиотека requests (как её поставить — в начале THEORY.md).
"""

import requests

# Адрес сервера «Космопорт». Все запросы начинаются с него.
BASE_URL = "https://api-lessons-sidorenkoai.msk1.amvera.tech"

TYPE_NAMES = {
    "rocky": "каменная",
    "gas": "газовый гигант",
    "ice": "ледяная",
    "ocean": "океанская",
    "lava": "вулканическая",
    "desert": "пустынная",
    "jungle": "джунгли",
}

# ------------------------------------------------------------ 1. Первый запрос
response = requests.get(BASE_URL + "/")

print("Код ответа:", response.status_code)  # 200 — всё хорошо
print("Тип r.text:", type(response.text))  # просто строка с JSON
data = response.json()  # разобрать JSON → словарь (как json.loads)
print("Тип r.json():", type(data))
print("Сервер говорит:", data["message"])

# ------------------------------------------------------------ 2. Список планет
response = requests.get(BASE_URL + "/planets")
data = response.json()
planets = data["planets"]  # в ответе словарь: {"count": 12, "planets": [...]}

print("\nПланеты галактики «Космопорт» (с сервера)")
print("-" * 40)
for planet in planets:
    print(f'{planet["id"]:>2}. {planet["name"]:<12} {TYPE_NAMES[planet["type"]]}')
print("-" * 40)
print("Всего планет:", data["count"])

# ------------------------------------------------- 3. Карточка планеты по номеру
planet_id = input("\nВведи номер планеты: ").strip()
response = requests.get(f"{BASE_URL}/planets/{planet_id}")

if response.status_code == 200:
    planet = response.json()
    temperature = planet["temperature"]
    print(f'\n=== {planet["name"]} ===')
    print("Тип:", TYPE_NAMES[planet["type"]])
    print("Гравитация:", planet["gravity"], "g")
    print(f'Температура: от {temperature["min"]} до {temperature["max"]} °C')
    print("Луны:", ", ".join(planet["moons"]) or "нет")
    print("Население:", planet["population"])
    print(planet["description"])
elif response.status_code == 404:
    # Даже ошибку сервер присылает в JSON: {"error": "..."}
    print("Такой планеты нет. Сервер ответил:", response.json()["error"])
else:
    print("Что-то пошло не так, код ответа:", response.status_code)
