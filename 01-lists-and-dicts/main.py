"""Урок 1. «Справочник галактики»: списки и словари.

Данные о планетах лежат в соседнем файле planets_data.py.
Там один большой список planets, и каждая планета в нём — словарь.
"""

from planets_data import planets

# Типы планет в данных записаны коротким кодом, а показывать хотим по-русски.
TYPE_NAMES = {
    "rocky": "каменная",
    "gas": "газовый гигант",
    "ice": "ледяная",
    "ocean": "океанская",
    "lava": "вулканическая",
    "desert": "пустынная",
    "jungle": "джунгли",
}

# ---------------------------------------------------------------- 1. Таблица планет
print("Планеты галактики «Космопорт»")
print("-" * 48)
for planet in planets:
    type_name = TYPE_NAMES[planet["type"]]
    moons_count = len(planet["moons"])
    print(f'{planet["id"]:>2}. {planet["name"]:<12} {type_name:<16} лун: {moons_count}')
print("-" * 48)
print("Всего планет:", len(planets))

# ---------------------------------------------------- 2. Самая сильная гравитация
heaviest = planets[0]
for planet in planets:
    if planet["gravity"] > heaviest["gravity"]:
        heaviest = planet
print(f'\nСамая сильная гравитация — на планете {heaviest["name"]}: {heaviest["gravity"]} g')

# ------------------------------------------------------------- 3. Планеты с водой
with_water = []
for planet in planets:
    if planet["has_water"]:
        with_water.append(planet["name"])
print("Вода есть на планетах:", ", ".join(with_water))

# -------------------------------------------------------------- 4. Сколько всего лун
total_moons = 0
for planet in planets:
    total_moons += len(planet["moons"])
print("Всего лун в галактике:", total_moons)


# ------------------------------------------------- 5. Топ-3 по населению (sorted)
def by_population(planet):
    return planet["population"]


top = sorted(planets, key=by_population, reverse=True)
print("\nСамые населённые планеты:")
for planet in top[:3]:
    print(f'  {planet["name"]}: {planet["population"]} жителей')

# ------------------------------------------------- 6. Карточка планеты по имени
name = input("\nО какой планете рассказать? ")

found = None
for planet in planets:
    if planet["name"] == name:
        found = planet
        break

if found is None:
    print("Такой планеты нет в справочнике.")
else:
    temperature = found["temperature"]
    print(f'\n=== {found["name"]} ===')
    print("Тип:", TYPE_NAMES[found["type"]])
    print("Гравитация:", found["gravity"], "g")
    print(f'Температура: от {temperature["min"]} до {temperature["max"]} °C')
    print("Луны:", ", ".join(found["moons"]))
    print(found["description"])
