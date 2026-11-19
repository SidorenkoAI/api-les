"""Задание 6. Словарь-счётчик: на скольких планетах встречается каждый газ."""

from planets_data import planets

counter = {}
for planet in planets:
    for gas in planet["atmosphere"]:
        counter[gas] = counter.get(gas, 0) + 1

for gas, count in counter.items():
    print(f"{gas} — {count}")

# Самый частый газ — поиск максимума циклом, как в уроке
best_gas = None
for gas in counter:
    if best_gas is None or counter[gas] > counter[best_gas]:
        best_gas = gas
print(f"\nЧаще всего встречается {best_gas}: на {counter[best_gas]} планетах")

# То же самое одной строкой
assert best_gas == max(counter, key=counter.get)
