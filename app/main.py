from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.database import engine, Base
from app.routes import locations, photos

app = FastAPI(
    title="Virtual Map API",
    description="API для виртуальной карты с поддержкой фотографий по локациям",
    version="2.0.0",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(locations.router)
app.include_router(photos.router)


@app.on_event("startup")
async def create_tables():
    """Автоматическое создание таблиц при запуске приложения."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Таблицы базы данных созданы/проверены")


@app.get("/")
async def root():
    return {"message": "Virtual Map API работает"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}