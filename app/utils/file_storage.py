import base64
import os
import uuid
import mimetypes
from pathlib import Path
from typing import Optional, Tuple

from app.core.config import settings

# Директории для хранения загруженных файлов
UPLOAD_BASE = Path("uploads")
PHOTO_DIR = UPLOAD_BASE / "photos"
VIDEO_DIR = UPLOAD_BASE / "videos"

for directory in [UPLOAD_BASE, PHOTO_DIR, VIDEO_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


def detect_media_type_from_base64(base64_data: str) -> Tuple[str, str]:
    """
    Определяет тип медиа (photo/video) и расширение файла из base64 строки.
    Возвращает (media_type, extension).
    """
    if not base64_data:
        raise ValueError("Base64 данные пусты")
    
    # Извлекаем заголовок data:image/png;base64,...
    if "," in base64_data:
        header = base64_data.split(",")[0]
    else:
        header = ""
    
    if "image/" in header:
        # Определяем расширение из MIME типа
        mime_type = header.split(":")[1].split(";")[0]
        ext = mimetypes.guess_extension(mime_type) or ".jpg"
        return "photo", ext
    elif "video/" in header:
        mime_type = header.split(":")[1].split(";")[0]
        ext = mimetypes.guess_extension(mime_type) or ".mp4"
        return "video", ext
    else:
        # По умолчанию считаем изображением
        return "photo", ".jpg"


def save_base64_as_file(base64_data: str, filename: Optional[str] = None) -> str:
    """
    Сохраняет base64 строку как файл на диск и возвращает путь к файлу.
    Автоматически определяет тип (photo/video) и сохраняет в соответствующую папку.
    """
    if not base64_data:
        raise ValueError("Base64 данные пусты")
    
    # Извлекаем данные из base64
    if "," in base64_data:
        header, data = base64_data.split(",", 1)
    else:
        header = ""
        data = base64_data
    
    # Декодируем
    file_data = base64.b64decode(data)
    
    # Определяем тип и расширение
    media_type, extension = detect_media_type_from_base64(base64_data)
    
    # Генерируем уникальное имя файла
    if filename is None:
        filename = f"{uuid.uuid4().hex}{extension}"
    
    # Выбираем директорию
    if media_type == "photo":
        file_path = PHOTO_DIR / filename
    else:  # video
        file_path = VIDEO_DIR / filename
    
    with open(file_path, "wb") as f:
        f.write(file_data)
    
    return str(file_path)


def file_to_base64(file_path: str) -> Optional[str]:
    """
    Читает файл с диска и возвращает его в формате base64.
    """
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, "rb") as f:
        data = f.read()
    
    return base64.b64encode(data).decode("utf-8")


def delete_file(file_path: str) -> bool:
    """
    Удаляет файл с диска.
    """
    try:
        os.remove(file_path)
        return True
    except OSError:
        return False