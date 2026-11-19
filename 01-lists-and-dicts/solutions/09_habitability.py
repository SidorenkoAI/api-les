"""Задание 9. Пригодность для жизни: баллы и рейтинг."""

from planets_data import planets


def reasons(planet):
    """Список причин, за которые планета получает баллы: (текст, баллы)."""
    result = []
    temperature = planet["temperature"]
    if planet["has_water"]:
        result.append(("есть вода", 2))
    if "кислород" in planet["atmosphere"]:
        result.append(("есть кислород", 2))
    if -50 <= temperature["min"] and temperature["max"] <= 50:
        result.append(("терпимая температура", 2))
    if 0.5 <= planet["gravity"] <= 1.5:
        result.append(("удобная гравитация", 1))
    if planet["population"] > 0:
        result.append(("уже есть жители", 1))
    return result


def score(planet):
    total = 0
    for _, points in reasons(planet):
        total += points
    return total


rating = sorted(planets, key=score, reverse=True)
for place, planet in enumerate(rating, start=1):
    print(f'{place:>2}. {planet["name"]:<12} баллы: {score(planet)}')

print("\nЛучшие планеты для жизни:")
for planet in rating[:3]:
    why = ", ".join(text for text, _ in reasons(planet))
    print(f'  {planet["name"]}: {why}')
