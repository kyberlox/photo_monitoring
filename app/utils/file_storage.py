import os
import uuid
from pathlib import Path
from typing import Optional
from fastapi import UploadFile

from app.core.config import settings

# Базовый путь для загрузки файлов (внутри контейнера)
UPLOAD_BASE = Path("/uploads")
PHOTO_DIR = UPLOAD_BASE / "photos"

# Создаём директории, если они не существуют
for directory in [UPLOAD_BASE, PHOTO_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def save_upload_file(upload_file: UploadFile, filename: Optional[str] = None) -> str:
    """
    Сохраняет загруженный файл на диск и возвращает путь к файлу.
    
    Args:
        upload_file: объект UploadFile из FastAPI
        filename: опциональное имя файла (без расширения). Если не указано, генерируется UUID.
    
    Returns:
        Абсолютный путь к сохранённому файлу (строка).
    """
    # Определяем расширение из оригинального имени файла
    original_filename = upload_file.filename
    if original_filename:
        ext = Path(original_filename).suffix.lower()
        if ext not in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]:
            ext = ".jpg"  # fallback
    else:
        ext = ".jpg"
    
    # Генерируем уникальное имя файла
    if filename is None:
        filename = f"{uuid.uuid4().hex}{ext}"
    else:
        # Если имя предоставлено, добавляем расширение, если его нет
        if not filename.lower().endswith(ext):
            filename += ext
    
    # Полный путь к файлу
    file_path = PHOTO_DIR / filename
    
    # Сохраняем файл
    with open(file_path, "wb") as f:
        content = upload_file.file.read()
        f.write(content)
    
    # Возвращаем путь как строку (абсолютный)
    return str(file_path)


def generate_file_url(file_path: str) -> str:
    """
    Генерирует URL для доступа к файлу через статику.
    
    Предполагается, что Nginx раздаёт файлы из /uploads по URL /static/
    """
    # Преобразуем абсолютный путь в относительный относительно UPLOAD_BASE
    try:
        relative_path = Path(file_path).relative_to(UPLOAD_BASE)
    except ValueError:
        # Если файл не внутри UPLOAD_BASE, возвращаем как есть
        relative_path = Path(file_path).name
    
    # URL вида /static/photos/...
    return f"/static/{relative_path}"


def delete_file(file_path: str) -> bool:
    """
    Удаляет файл с диска.
    """
    try:
        os.remove(file_path)
        return True
    except OSError:
        return False


def file_exists(file_path: str) -> bool:
    """
    Проверяет, существует ли файл.
    """
    return os.path.exists(file_path)