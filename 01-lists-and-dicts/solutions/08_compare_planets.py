"""Задание 8. Сравнение двух планет."""

from planets_data import planets

# Строки таблицы: подпись и что сравниваем
ROWS = [
    ("гравитация", "gravity"),
    ("радиус, км", "radius_km"),
    ("лун", "moons"),
    ("мин. темп.", "min"),
    ("макс. темп.", "max"),
    ("население", "population"),
]


def find_planet(name):
    name = name.strip().lower()
    for planet in planets:
        if planet["name"].lower() == name:
            return planet
    return None


def value(planet, key):
    """Значение для сравнения: с особыми случаями для лун и температуры."""
    if key == "moons":
        return len(planet["moons"])
    if key in ("min", "max"):
        return planet["temperature"][key]
    return planet[key]


def ask_planet(question):
    while True:
        planet = find_planet(input(question))
        if planet is not None:
            return planet
        print("Такой планеты нет, попробуй ещё раз.")


first = ask_planet("Первая планета: ")
second = ask_planet("Вторая планета: ")

print()
print(f'{"":<15}{first["name"]:>12}  {second["name"]:>12}')
for title, key in ROWS:
    a = value(first, key)
    b = value(second, key)
    mark_a = " ←" if a > b else "  "
    mark_b = " ←" if b > a else "  "
    print(f"{title:<15}{a:>12}{mark_a}{b:>12}{mark_b}")
