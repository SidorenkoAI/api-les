"""Урок 4. Параметры запроса и ошибки: генератор экипажа корабля.

Программа набирает экипаж из случайных инопланетян. Один и тот же номер экипажа (seed)
всегда даёт один и тот же экипаж — можно сравнить с соседом. Портрет капитана
сохраняется в файл captain.svg (открой его в браузере).
"""

import requests

BASE_URL = "https://api-lessons-sidorenkoai.msk1.amvera.tech"
CREW_SIZE = 5
TIMEOUT = 10  # сколько секунд ждать ответа сервера, прежде чем сдаться

seed = input("Номер экипажа (целое число, Enter — случайный экипаж): ").strip()

# Параметры запроса — словарь. requests сам допишет их к адресу: ?count=5&seed=42
params = {"count": CREW_SIZE}
if seed:
    params["seed"] = seed

try:
    response = requests.get(BASE_URL + "/aliens/random", params=params, timeout=TIMEOUT)
    print("Адрес запроса:", response.url)

    if response.status_code == 400:
        # Неверный параметр: сервер объясняет, какой именно и что с ним не так
        error = response.json()
        print("Сервер не понял запрос:", error["error"])
        for detail in error["details"]:
            print(f'  {detail["param"]}: {detail["message"]}')
    else:
        response.raise_for_status()  # любая другая ошибка (404, 500…) → исключение HTTPError
        crew = response.json()["results"]

        # Капитан — самый старший и опытный
        captain = crew[0]
        for alien in crew:
            if alien["age"] > captain["age"]:
                captain = alien

        print(f"\nЭкипаж корабля «Комета» ({len(crew)} чел.)")
        print("-" * 60)
        team_skills = []  # навыки всей команды, без повторов
        for alien in crew:
            role = "капитан" if alien["id"] == captain["id"] else "экипаж"
            print(f'{alien["name"]:<24} {alien["age"]:>3} лет, {alien["planet"]["name"]:<11} [{role}]')
            print(f'    умеет: {", ".join(alien["skills"])}')
            for skill in alien["skills"]:
                if skill not in team_skills:
                    team_skills.append(skill)
        print("-" * 60)

        print("Навыки команды:", ", ".join(sorted(team_skills)))
        if "пилотирование" in team_skills:
            print("Пилот есть — можно взлетать!")
        else:
            print("Пилота нет! Попробуй другой номер экипажа.")

        # Портрет — это не JSON, а картинка: берём «сырые» байты r.content
        photo = requests.get(captain["photo"], timeout=TIMEOUT)
        photo.raise_for_status()
        with open("captain.svg", "wb") as file:  # "wb" — запись байтов
            file.write(photo.content)
        print(f'Портрет капитана {captain["name"]} сохранён в captain.svg ({len(photo.content)} байт)')

except requests.RequestException as error:
    # Сюда попадаем, если нет интернета, сервер не ответил за TIMEOUT секунд или ответил ошибкой
    print("Не получилось поговорить с сервером:", error)
