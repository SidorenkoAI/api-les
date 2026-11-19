"""Задание 4. Рейтинги: первые три места."""

from planets_data import planets


def moons_count(planet):
    return len(planet["moons"])


def gravity(planet):
    return planet["gravity"]


def radius(planet):
    return planet["radius_km"]


def print_top(title, sorted_planets, key, unit):
    print(title)
    for place, planet in enumerate(sorted_planets[:3], start=1):
        print(f'  {place}. {planet["name"]} — {key(planet)} {unit}')
    print()


print_top("Больше всего лун:", sorted(planets, key=moons_count, reverse=True), moons_count, "шт.")
print_top("Самые лёгкие планеты:", sorted(planets, key=gravity), gravity, "g")
print_top("Самые большие планеты:", sorted(planets, key=radius, reverse=True), radius, "км")
