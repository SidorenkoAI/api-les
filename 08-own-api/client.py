"""Урок 8. Клиент для зоопарка соседа: тот же requests, что на уроках 3–7, только сервер — у соседа.

Сосед запускает у себя main.py и говорит свой IP (например, 192.168.1.15).
Впиши его в BASE_URL: "http://192.168.1.15:8000". Пока проверяешь свой сервер — оставь 127.0.0.1.
"""

import requests

BASE_URL = "http://127.0.0.1:8000"


def explain(response):
    """Текст ошибки от FastAPI. В detail — строка (ошибку написали мы сами, как 404)
    или список проблем (422: FastAPI сам проверил данные, и они не подошли)."""
    detail = response.json()["detail"]
    if isinstance(detail, str):
        return detail
    problems = []
    for problem in detail:
        problems.append(f"{problem['loc'][-1]}: {problem['msg']}")  # loc — где проблема, msg — какая
    return "; ".join(problems)


def show(animal):
    """Одна строка про зверя."""
    print(f"№{animal['id']} {animal['name']} — {animal['species']} с планеты {animal['planet']}, "
          f"возраст {animal['age']}, ног: {animal['legs']}")


def show_all(planet=None):
    """Все звери или только с одной планеты."""
    params = {}
    if planet:
        params["planet"] = planet
    data = requests.get(BASE_URL + "/animals", params=params, timeout=5).json()
    print(f"Зверей: {data['count']}")
    for animal in data["animals"]:
        show(animal)


def show_one(animal_id):
    """Один зверь по номеру. На «нет такого» сервер отвечает 404, на «abc» вместо номера — 422."""
    response = requests.get(BASE_URL + f"/animals/{animal_id}", timeout=5)
    if response.status_code == 200:
        show(response.json())
    else:
        print(f"Ошибка {response.status_code}:", explain(response))


def add():
    """Отправить соседу нового зверя — POST с телом, как на уроке 6."""
    animal = {
        "name": input("Имя: "),
        "species": input("Вид: "),
        "planet": input("Планета: "),
        "age": input("Возраст: "),  # строка "3" подойдёт: FastAPI сам переведёт её в число
    }
    response = requests.post(BASE_URL + "/animals", json=animal, timeout=5)
    if response.status_code == 201:
        print("Зверь принят! Ему дали номер", response.json()["id"])
    else:
        print(f"Не приняли (код {response.status_code}):", explain(response))


# --------------------------------------------------------------- 1. Есть ли связь?
try:
    hello = requests.get(BASE_URL + "/", timeout=5).json()
except requests.RequestException:
    print(f"Не могу связаться с {BASE_URL}. Сервер запущен? Адрес верный?")
    raise SystemExit
print(hello["message"], "Зверей сейчас:", hello["animals"])

# --------------------------------------------------------------- 2. Меню
while True:
    print("\n1 — все звери, 2 — зверь по номеру, 3 — звери с планеты, 4 — добавить, 0 — выход")
    choice = input("> ").strip()
    if choice == "1":
        show_all()
    elif choice == "2":
        show_one(input("Номер: ").strip())
    elif choice == "3":
        show_all(input("Планета: ").strip())
    elif choice == "4":
        add()
    elif choice == "0":
        print("Пока!")
        break
    else:
        print("Нет такого пункта")
