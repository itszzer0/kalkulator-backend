from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Создаём приложение
app = FastAPI()

# Разрешаем запросы с любого сайта (для теста)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Модель данных: что мы ждём от фронтенда
class RoomData(BaseModel):
    length: float
    width: float


# Эндпоинт для расчёта площади
@app.post("/calculate/area")
def calculate_area(data: RoomData):
    """Принимает длину и ширину, возвращает площадь"""
    area = data.length * data.width

    return {
        "length": data.length,
        "width": data.width,
        "area": round(area, 2),
        "message": f"Площадь комнаты {area:.2f} м²"
    }


# Тестовый эндпоинт для проверки связи
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Сервер работает!"}

# Для запуска: uvicorn main:app --reload