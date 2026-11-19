"""Задание 1. Полная карточка планеты."""

from planets_data import planets

TYPE_NAMES = {
    "rocky": "каменная",
    "gas": "газовый гигант",
    "ice": "ледяная",
    "ocean": "океанская",
    "lava": "вулканическая",
    "desert": "пустынная",
    "jungle": "джунгли",
}


def with_spaces(number):
    """56000 → '56 000'"""
    return f"{number:,}".replace(",", " ")


def print_card(planet):
    temperature = planet["temperature"]
    if planet["moons"]:
        moons = ", ".join(planet["moons"])
    else:
        moons = "нет"
    if planet["has_water"]:
        water = "есть"
    else:
        water = "нет"

    print(f'=== {planet["name"]} ===')
    print("Тип:", TYPE_NAMES[planet["type"]])
    print(f'Гравитация: {planet["gravity"]} g, радиус: {with_spaces(planet["radius_km"])} км')
    print(f'Температура: от {temperature["min"]} до {temperature["max"]} °C')
    print("Луны:", moons)
    print("Вода:", water)
    print("Атмосфера:", ", ".join(planet["atmosphere"]))
    print("Население:", with_spaces(planet["population"]))
    print("Открыта:", planet["discovered"])
    print(planet["description"])


name = input("О какой планете рассказать? ")
found = None
for planet in planets:
    if planet["name"] == name:
        found = planet
        break

if found is None:
    print("Такой планеты нет в справочнике.")
else:
    print_card(found)
