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
    return f"/api/static/{relative_path}"


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


def extract_filepath_from_url(url: str) -> Optional[str]:
    """
    Извлекает путь к файлу на диске из URL статики.
    
    Примеры:
    - "/api/static/photos/abc123.jpg" -> "/uploads/photos/abc123.jpg"
    - "http://localhost:8000/api/static/photos/abc123.jpg" -> "/uploads/photos/abc123.jpg"
    """
    # Убираем протокол и домен, если есть
    if "://" in url:
        # Извлекаем путь после домена
        from urllib.parse import urlparse
        parsed = urlparse(url)
        url_path = parsed.path
    else:
        url_path = url
    
    # Убираем префикс /api/static/ или /static/
    if url_path.startswith("/api/static/"):
        url_path = url_path[len("/api/static/"):]
    elif url_path.startswith("/static/"):
        url_path = url_path[len("/static/"):]
    
    if not url_path:
        return None
    
    # Собираем полный путь
    file_path = UPLOAD_BASE / url_path
    return str(file_path)


def delete_file_by_url(url: str) -> bool:
    """
    Удаляет файл по его URL (статическому).
    Возвращает True, если файл удалён, False если файл не найден.
    """
    file_path = extract_filepath_from_url(url)
    if not file_path:
        return False
    
    return delete_file(file_path)