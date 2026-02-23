from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math

# Создаём приложение
app = FastAPI()

# Разрешаем запросы с любого сайта (для теста)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# === ЛАМИНАТ =======================================================

class LaminateData(BaseModel):
    length: float
    width: float
    plank_length: float
    plank_width: float
    pack_quantity: int
    pack_price: float

@app.post("/calculate/laminate")
def calculate_laminate(data: LaminateData):
    """Расчёт количества ламината и стоимости"""
    room_area_m2 = (data.length * data.width)
    plank_area_m2 = (data.plank_length * data.plank_width)

    raw_planks = room_area_m2 / plank_area_m2
    planks_needed = math.ceil(raw_planks * 1.05)

    packs_needed = math.ceil(planks_needed / data.pack_quantity)
    total_price = packs_needed * data.pack_price

    return {
        "planks_needed": planks_needed,
        "packs_needed": packs_needed,
        "total_price": round(total_price, 2),
        "room_area": round(room_area_m2, 2),
        "message": f"Нужно {planks_needed} панелей, {packs_needed} упаковок, стоимость {total_price:.2f} руб."
    }
#====================================================================================

# Тестовый эндпоинт для проверки связи
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Сервер работает!"}

# Для запуска: uvicorn main:app --reload