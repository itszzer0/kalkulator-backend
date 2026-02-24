from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import math

# Создаём приложение
app = FastAPI()
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

    room_area_m2 = (data.length * data.width)
    plank_area_m2 = (data.plank_length * data.plank_width) / 1_000_000

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
#
# #== КРАСКА ============================================
# class PaintData(BaseModel):
#     length: float
#     width: float
#     layers: int
#     paint_type: str
#     can_volume: float
#     can_price: float
#
# @app.post("/calculate/paint")
# def calculate_paint(data: PaintData):
#
#     consumption_map = {
#         "acrylic": 10,
#         "latex": 12,
#         "silicone": 8,
#         "water": 9,
#         "enamel": 11
#     }
#
#     consumption = consumption_map.get(data.paint_type, 10)
#
#     area = data.length * data.width
#
#     total_liters = (area * data.layers) / consumption
#     total_liters = round(total_liters, 1)
#
#     import math
#     cans_needed = math.ceil(total_liters / data.can_volume)
#
#     total_price = cans_needed * data.can_price
#
#     paint_names = {
#         "acrylic": "Акриловая",
#         "latex": "Латексная",
#         "silicone": "Силиконовая",
#         "water": "Водно-дисперсионная",
#         "enamel": "Эмаль"
#     }
#     paint_name = paint_names.get(data.paint_type, "Неизвестный тип")
#
#     return {
#         "paint_type": paint_name,
#         "area": round(area, 2),
#         "layers": data.layers,
#         "total_liters": total_liters,
#         "cans_needed": cans_needed,
#         "total_price": round(total_price, 2),
#         "can_volume": data.can_volume
#     }
# #======================================



#тест
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Сервер работает!"}

# Для запуска: uvicorn main:app --reload