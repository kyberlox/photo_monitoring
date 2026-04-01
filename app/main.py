from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import locations, media

app = FastAPI(
    title="Virtual Map API",
    description="API для виртуальной карты с поддержкой фото, видео и текстовых описаний",
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
app.include_router(media.router)


@app.get("/")
async def root():
    return {"message": "Virtual Map API работает"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}