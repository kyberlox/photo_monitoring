import base64
import os
import uuid
from pathlib import Path
from typing import Optional

from app.core.config import settings

# Директория для хранения загруженных изображений
UPLOAD_DIR = Path("uploads/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def save_base64_as_file(base64_data: str, filename: Optional[str] = None) -> str:
    """
    Сохраняет base64 строку как файл на диск и возвращает путь к файлу.
    """
    if not base64_data:
        raise ValueError("Base64 данные пусты")
    
    # Извлекаем данные из base64 (формат data:image/png;base64,...)
    if "," in base64_data:
        header, data = base64_data.split(",", 1)
    else:
        data = base64_data
    
    # Декодируем
    file_data = base64.b64decode(data)
    
    # Генерируем уникальное имя файла
    if filename is None:
        ext = ".jpg"  # по умолчанию jpg, можно определить из header
        filename = f"{uuid.uuid4().hex}{ext}"
    
    file_path = UPLOAD_DIR / filename
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