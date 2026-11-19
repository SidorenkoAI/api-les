"""Урок 5. «Прогноз для космонавта»: почасовая погода на планете и график.

Сервер присылает прогноз как open-meteo.com: несколько списков одинаковой длины
(«параллельные массивы») — время, температура, ветер, буря. Программа находит
самый тёплый и самый холодный час, часы с бурей, лучший час для выхода из корабля
и рисует график в файл forecast.png.

Нужны библиотеки requests и matplotlib (как поставить — в THEORY.md).
"""

import matplotlib.pyplot as plt
import requests

BASE_URL = "https://api-lessons-sidorenkoai.msk1.amvera.tech"


def load_forecast(planet, days):
    """Скачать прогноз. Если не получилось — объяснить почему и вернуть None."""
    try:
        response = requests.get(BASE_URL + "/weather", params={"planet": planet, "days": days}, timeout=10)
    except requests.RequestException as error:
        print("Нет связи с сервером:", error)
        return None
    if response.status_code != 200:
        print("Сервер ответил ошибкой:", response.json()["error"])
        return None
    return response.json()


# ------------------------------------------------------------ 1. Получаем прогноз
forecast = None
while forecast is None:
    planet = input("Для какой планеты прогноз (имя или номер)? ").strip()
    forecast = load_forecast(planet, 1)

name = forecast["planet"]["name"]
hourly = forecast["hourly"]
times = hourly["time"]  # ["2026-11-19T00:00", "2026-11-19T01:00", ...]
temps = hourly["temperature"]  # [-41.5, -44.0, ...]
winds = hourly["wind"]
storms = hourly["storm"]  # [False, False, True, ...]

# Из "2026-11-19T15:00" оставим только часы: символы с 11-го по 15-й → "15:00"
hours = []
for moment in times:
    hours.append(moment[11:16])

print(f"\nПрогноз для планеты {name} на {forecast['start']} ({forecast['timezone']})")

# ------------------------------------------------ 2. Таблица: zip идёт по всем спискам сразу
print("Время   Темп., °C  Ветер, м/с")
for hour, temp, wind, storm in zip(hours, temps, winds, storms):
    mark = "  БУРЯ!" if storm else ""
    print(f"{hour}  {temp:>9}  {wind:>10}{mark}")

# ---------------------------------------------- 3. Максимум, минимум и среднее
warmest = max(temps)
warmest_i = temps.index(warmest)  # номер элемента → по нему же берём час из hours
coldest = min(temps)
coldest_i = temps.index(coldest)
average = sum(temps) / len(temps)

print(f"\nСамый тёплый час: {hours[warmest_i]}, {warmest} °C")
print(f"Самый холодный час: {hours[coldest_i]}, {coldest} °C")
print(f"Средняя температура: {average:.1f} °C, самый сильный ветер: {max(winds)} м/с")

# ------------------------------------------------------------- 4. Часы с бурей
storm_hours = []
for hour, storm in zip(hours, storms):
    if storm:
        storm_hours.append(hour)

if storm_hours:
    print(f"Буря ({len(storm_hours)} ч):", ", ".join(storm_hours))
else:
    print("Бурь не будет весь день!")

# ------------------------------------- 5. Совет: тихий час без бури и с самым слабым ветром
best_i = None
for i in range(len(hours)):
    if not storms[i] and (best_i is None or winds[i] < winds[best_i]):
        best_i = i

if best_i is None:
    print("Совет космонавту: сегодня из корабля лучше не выходить!")
else:
    print(f"Совет космонавту: выходи в {hours[best_i]} — ветер {winds[best_i]} м/с, {temps[best_i]} °C")

# ------------------------------------------------------------------ 6. График
plt.figure(figsize=(10, 5))
plt.plot(hours, temps, marker="o", linewidth=2, label="температура")

# Часы с бурей отметим поверх графика красными крестиками
storm_temps = []
for temp, storm in zip(temps, storms):
    if storm:
        storm_temps.append(temp)
if storm_hours:
    plt.scatter(storm_hours, storm_temps, color="red", marker="X", s=120, zorder=3, label="буря")

plt.title(f"Температура на планете {name}, {forecast['start']}")
plt.xlabel("Время")
plt.ylabel("Температура, °C")
plt.xticks(rotation=45)  # повернём подписи, чтобы 24 часа не налезали друг на друга
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("forecast.png", dpi=100)
print("\nГрафик сохранён в forecast.png")
plt.show()  # открыть окно с графиком (в PyCharm он может появиться на вкладке Plots)
