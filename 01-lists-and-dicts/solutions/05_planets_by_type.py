"""Задание 5. Планеты по типам: словарь «тип → список имён»."""

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

by_type = {}
for planet in planets:
    planet_type = planet["type"]
    if planet_type not in by_type:
        by_type[planet_type] = []
    by_type[planet_type].append(planet["name"])

for planet_type, names in by_type.items():
    print(f'{TYPE_NAMES[planet_type]}: {", ".join(names)}')
