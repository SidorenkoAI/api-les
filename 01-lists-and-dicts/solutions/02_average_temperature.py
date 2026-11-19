"""Задание 2. Средняя температура."""

from planets_data import planets

total = 0
for planet in planets:
    temperature = planet["temperature"]
    average = (temperature["min"] + temperature["max"]) / 2
    total += average
    print(f'{planet["name"]:<12} {average:>7.1f} °C')

print("-" * 24)
print("Средняя по галактике:", round(total / len(planets), 1), "°C")
