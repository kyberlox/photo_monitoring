import asyncio
import sys
import os

# Текущая директория скрипта
script_dir = os.path.dirname(os.path.abspath(__file__))
# Директория app (на уровень выше)
app_dir = os.path.dirname(script_dir)
# Директория data (на уровень выше app)
data_dir = os.path.dirname(app_dir)

# Добавляем обе директории в путь
sys.path.insert(0, data_dir)
sys.path.insert(0, app_dir)

from database.database import engine, Base
from models import location, media


async def create_tables():
    async with engine.begin() as conn:
        # Удаляем существующие таблицы (для разработки)
        # В продакшене используйте миграции Alembic
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы созданы успешно")


if __name__ == "__main__":
    asyncio.run(create_tables())