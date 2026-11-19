"""Задание 3. Поиск без учёта регистра, вопросы по кругу до пустой строки."""

from planets_data import planets


def find_planet(name):
    name = name.strip().lower()
    for planet in planets:
        if planet["name"].lower() == name:
            return planet
    return None


while True:
    name = input("О какой планете рассказать? (пустая строка — выход) ")
    if name.strip() == "":
        print("До встречи в космопорте!")
        break

    planet = find_planet(name)
    if planet is None:
        print("Такой планеты нет в справочнике.")
    else:
        print(f'{planet["name"]}: {planet["description"]}')
