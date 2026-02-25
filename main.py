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
    installation_type: str


@app.post("/calculate/laminate")
def calculate_laminate(data: LaminateData):
    import math

    #процент и вычисления
    waste_map = {
        "straight": 0.05,  # прямая укладка — 5%
        "diagonal": 0.10,  # диагональная — 10%
        "herringbone": 0.15  # ёлочка — 15%
    }

    waste_percent = waste_map.get(data.installation_type, 0.05)
    room_area = data.length * data.width
    plank_area = (data.plank_length * data.plank_width) / 1_000_000
    raw_planks = room_area / plank_area
    planks_needed = math.ceil(raw_planks * (1 + waste_percent))
    packs_needed = math.ceil(planks_needed / data.pack_quantity)
    total_price = packs_needed * data.pack_price

    type_names = {
        "straight": "Прямая",
        "diagonal": "Диагональная",
        "herringbone": "Ёлочка"
    }
    display_name = type_names.get(data.installation_type, "Прямая")

    return {
        "room_area": round(room_area, 2),
        "planks_needed": planks_needed,
        "packs_needed": packs_needed,
        "total_price": round(total_price, 2),
        "waste_percent": waste_percent * 100,
        "installation_type": display_name,
        "message": f"{display_name} укладка: {planks_needed} панелей, {packs_needed} упаковок, {total_price:.2f} руб."
    }
# === КРАСКА ========================================================
class PaintData(BaseModel):
    length: float
    width: float
    layers: int
    paint_type: str
    bucket_volume: float
    bucket_price: float

@app.post("/calculate/paint")
def calculate_paint(data: PaintData):
    import math

    consumption_map = {
        "acrylic": 10,
        "latex": 12,
        "water": 9,
        "enamel": 11
    }

    consumption = consumption_map.get(data.paint_type, 10)

    area = data.length * data.width

    total_liters = (area * data.layers) / consumption
    total_liters = round(total_liters, 1)

    buckets_needed = math.ceil(total_liters / data.bucket_volume)

    total_price = buckets_needed * data.bucket_price

    type_names = {
        "acrylic": "Акриловая",
        "latex": "Латексная",
        "water": "Водоэмульсионная",
        "enamel": "Эмаль"
    }
    paint_name = type_names.get(data.paint_type, "Неизвестный тип")

    return {
        "paint_type": paint_name,
        "area": round(area, 2),
        "layers": data.layers,
        "total_liters": total_liters,
        "buckets_needed": buckets_needed,
        "total_price": round(total_price, 2),
        "message": f"{buckets_needed} ведро(а) по {data.bucket_volume} л, стоимость {total_price:.2f} руб."
    }
# === ОБОИ =========================================================
class WallpaperData(BaseModel):
    wall_length: float
    wall_height: float
    has_opening: bool
    opening_width: float
    opening_height: float
    roll_length: float
    roll_width: float
    roll_price: float

@app.post("/calculate/wallpaper")
def calculate_wallpaper(data: WallpaperData):
    import math

    wall_area = data.wall_length * data.wall_height

    opening_area = 0
    if data.has_opening and data.opening_width > 0 and data.opening_height > 0:
        opening_area = data.opening_width * data.opening_height

    net_area = wall_area - opening_area

    roll_area = data.roll_length * data.roll_width

    rolls_needed = math.ceil(net_area / roll_area)

    total_price = rolls_needed * data.roll_price

    return {
        "net_area": round(net_area, 2),
        "rolls_needed": rolls_needed,
        "total_price": round(total_price, 2)
    }
# === КЛЕЙ =========================================================
class GlueData(BaseModel):
    length: float
    width: float
    consumption: float      # расход клея (кг/м² на 1 мм слоя)
    thickness: float
    pack_weight: float
    pack_price: float

@app.post("/calculate/glue")
def calculate_glue(data: GlueData):
    import math

    area = data.length * data.width

    real_consumption = data.consumption * data.thickness

    total_kg = area * real_consumption
    total_kg = round(total_kg, 1)

    packs_needed = math.ceil(total_kg / data.pack_weight)

    total_price = packs_needed * data.pack_price

    return {
        "area": round(area, 2),
        "total_kg": total_kg,
        "packs_needed": packs_needed,
        "total_price": round(total_price, 2),
        "message": f"Нужно {packs_needed} упаковок, стоимость {total_price:.2f} руб."
    }


#тест
@app.get("/ping")
def ping():
    return {"status": "ok", "message": "Сервер работает!"}

# Для запуска: uvicorn main:app --reload

#git add .
#git commit -m "описание изменений"
#git push