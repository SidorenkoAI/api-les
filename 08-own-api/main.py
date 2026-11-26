"""Урок 8. Свой API на FastAPI: «Космический зоопарк».

Семь уроков мы были клиентами: спрашивали сервер «Космопорт» и разбирали его ответы.
Сегодня мы по ту сторону — пишем сервер сами:
1) маршрут — функция, которая отвечает на запрос по адресу (@app.get("/animals"));
2) параметры пути (/animals/2) и запроса (/animals?planet=Мурлыка);
3) функция возвращает словарь — FastAPI сам превращает его в JSON;
4) нет такого зверя — отвечаем кодом 404;
5) POST /animals — принимаем нового зверя в теле запроса.
Страница /docs с описанием API появляется сама, её писать не нужно.

Запуск — кнопкой Run. Остановка — красный квадрат «Stop» в PyCharm.
Открой в браузере http://127.0.0.1:8000/docs
"""

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Космический зоопарк", description="Звери со всех планет Космопорта")

# Данные зоопарка — обычный список словарей, как на уроке 1.
# Они живут в памяти: перезапустил сервер — новые звери пропали.
animals = [
    {"id": 1, "name": "Пушок", "species": "звёздный кот", "planet": "Мурлыка", "age": 3, "legs": 4},
    {"id": 2, "name": "Бульк", "species": "медуза-фонарик", "planet": "Аквамарина", "age": 12, "legs": 0},
    {"id": 3, "name": "Топотун", "species": "гравитяк", "planet": "Гигантус", "age": 40, "legs": 6},
    {"id": 4, "name": "Искра", "species": "огненная ящерка", "planet": "Пеклон", "age": 2, "legs": 4},
    {"id": 5, "name": "Снежок", "species": "ледяной пингвин", "planet": "Ледяна", "age": 7, "legs": 2},
    {"id": 6, "name": "Шуршик", "species": "песчаный крот", "planet": "Барханья", "age": 5, "legs": 4},
]


class NewAnimal(BaseModel):
    """Каким должно быть тело POST /animals. Неподходящее тело FastAPI не пустит: ответит 422."""

    name: str
    species: str
    planet: str
    age: int
    legs: int = 4  # необязательное поле: если не прислали — будет 4


@app.get("/")
def welcome():
    """Приветствие и список разделов — как GET / у Космопорта."""
    return {
        "message": "Добро пожаловать в Космический зоопарк!",
        "animals": len(animals),
        "endpoints": ["/animals", "/animals/{id}", "/docs"],
    }


@app.get("/animals")
def list_animals(planet: str | None = None):
    """Все звери. ?planet=Мурлыка — только звери с этой планеты."""
    result = []
    for animal in animals:
        if planet is None or animal["planet"].lower() == planet.lower():
            result.append(animal)
    return {"count": len(result), "animals": result}


@app.get("/animals/{animal_id}")
def get_animal(animal_id: int):
    """Один зверь по номеру. Нет такого — 404."""
    for animal in animals:
        if animal["id"] == animal_id:
            return animal
    raise HTTPException(status_code=404, detail=f"Зверя №{animal_id} в зоопарке нет")


@app.post("/animals", status_code=201)
def add_animal(new: NewAnimal):
    """Новый зверь. Номер выдаёт сервер: на 1 больше самого большого."""
    animal = {
        "id": max(a["id"] for a in animals) + 1,
        "name": new.name,  # поля тела — атрибуты через точку
        "species": new.species,
        "planet": new.planet,
        "age": new.age,
        "legs": new.legs,
    }
    animals.append(animal)
    return animal


if __name__ == "__main__":
    # host="0.0.0.0" — пускать запросы не только с этого компьютера, но и от соседей по сети.
    # Сам открывай http://127.0.0.1:8000, а соседу дай адрес http://<твой IP>:8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
