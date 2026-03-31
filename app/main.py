from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, locations, images

app = FastAPI(
    title="Photo Monitoring API",
    description="API для мониторинга фотографий по локациям",
    version="1.0.0",
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
app.include_router(users.router)
app.include_router(locations.router)
app.include_router(images.router)


@app.get("/")
async def root():
    return {"message": "Photo Monitoring API работает"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}