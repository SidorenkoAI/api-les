"""Урок 2. JSON: справочник читает планеты из файла и сохраняет отчёт в файл.

Рядом должен лежать planets.json — те же планеты, что на уроке 1, но в формате JSON.
"""

import json

# ------------------------------------------------- 1. Данные → строка JSON и обратно
planet = {"name": "Комета-Х", "moons": [], "has_water": False, "rings": None}

text = json.dumps(planet, ensure_ascii=False)
print("Строка JSON:", text)
print("Тип:", type(text))

again = json.loads(text)
print("Снова словарь:", again)
print("Тип:", type(again), "| совпадает с исходным:", again == planet)

# -------------------------------------------------------- 2. Читаем planets.json
with open("planets.json", encoding="utf-8") as file:
    planets = json.load(file)

print("\nЗагружено планет:", len(planets))
print("Первая планета:", planets[0]["name"], "| тип данных:", type(planets[0]))

# ------------------------------------------- 3. Обрабатываем — как на уроке 1
moons_total = 0
with_water = []
heaviest = planets[0]
for planet in planets:
    moons_total += len(planet["moons"])
    if planet["has_water"]:
        with_water.append(planet["name"])
    if planet["gravity"] > heaviest["gravity"]:
        heaviest = planet


def by_population(planet):
    return planet["population"]


top_population = []
for planet in sorted(planets, key=by_population, reverse=True)[:3]:
    top_population.append({"name": planet["name"], "population": planet["population"]})

# Отчёт — тоже словарь: внутри числа, списки и словари
report = {
    "planets_total": len(planets),
    "moons_total": moons_total,
    "with_water": with_water,
    "heaviest": {"name": heaviest["name"], "gravity": heaviest["gravity"]},
    "top_population": top_population,
}

# ------------------------------------------------- 4. Сохраняем отчёт в report.json
with open("report.json", "w", encoding="utf-8") as file:
    json.dump(report, file, ensure_ascii=False, indent=2)

print("\nОтчёт сохранён в report.json:")
print(json.dumps(report, ensure_ascii=False, indent=2))
