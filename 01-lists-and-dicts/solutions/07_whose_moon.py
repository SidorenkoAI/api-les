"""Задание 7. Чья это луна?"""

from planets_data import planets

moon_owner = {}  # луна → имя планеты
all_moons = []
for planet in planets:
    all_moons.extend(planet["moons"])
    for moon in planet["moons"]:
        moon_owner[moon] = planet["name"]

print(f"Все луны галактики ({len(all_moons)}):")
print(", ".join(sorted(all_moons)))

moon = input("\nКакую луну найти? ").strip()
if moon in moon_owner:
    print(f"{moon} — луна планеты {moon_owner[moon]}")
else:
    print("Такой луны в галактике нет.")
