from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.database import get_db
from app.models.photo import Photo
from app.models.location import Location
from app.schemas.photo import PhotoCreate, PhotoUpdate, Photo as PhotoSchema
from app.utils.file_storage import (
    save_upload_file,
    generate_file_url,
    delete_file,
    delete_file_by_url,
    extract_filepath_from_url
)

router = APIRouter(prefix="/api/photos", tags=["photos"])


async def enrich_photo_with_url(photo: Photo) -> PhotoSchema:
    """Добавляет URL к фото для ответа."""
    file_url = None
    if photo.file_path:
        file_url = generate_file_url(photo.file_path)
    
    return PhotoSchema(
        id=photo.id,
        comment=photo.comment,
        created_at=photo.created_at,
        file_url=file_url,
        location_id=photo.location_id,
    )


@router.get("/all", response_model=list[PhotoSchema])
async def get_photos(
    location_id: int = Query(None, description="Фильтр по локации"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Photo)
    if location_id is not None:
        query = query.where(Photo.location_id == location_id)
    
    result = await db.execute(query)
    photos_list = result.scalars().all()
    return [await enrich_photo_with_url(p) for p in photos_list]


@router.get("/id={photo_id}", response_model=PhotoSchema)
async def get_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if photo is None:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    return await enrich_photo_with_url(photo)


@router.post("/add", response_model=list[PhotoSchema])
async def create_photo(
    comment: Optional[str] = Form(None),
    location_id: int = Form(...),
    photos: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
):
    # Проверка существования локации
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    created_photos = []
    for photo_file in photos:
        if not photo_file.filename:
            continue  # пропускаем пустые файлы
        # Сохраняем файл на диск
        file_path = save_upload_file(photo_file)
        
        # Создаем запись в БД
        new_photo = Photo(
            comment=comment,
            file_path=file_path,
            location_id=location_id,
        )
        db.add(new_photo)
        created_photos.append(new_photo)
    
    await db.commit()
    
    # Обогащаем каждое фото URL
    enriched = []
    for photo in created_photos:
        await db.refresh(photo)
        enriched.append(await enrich_photo_with_url(photo))
    
    return enriched


@router.put("/id={photo_id}", response_model=PhotoSchema)
async def update_photo(
    photo_id: int,
    comment: Optional[str] = Form(None),
    photo: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo_obj = result.scalar_one_or_none()
    if photo_obj is None:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    
    if comment is not None:
        photo_obj.comment = comment
    
    # Если пришел новый файл
    if photo is not None and photo.filename:
        # Удаляем старый файл
        if photo_obj.file_path:
            delete_file(photo_obj.file_path)
        # Сохраняем новый
        new_file_path = save_upload_file(photo)
        photo_obj.file_path = new_file_path
    
    await db.commit()
    await db.refresh(photo_obj)
    return await enrich_photo_with_url(photo_obj)


@router.delete("/id={photo_id}")
async def delete_photo(
    photo_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if photo is None:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    
    # Удаляем файл с диска (если есть)
    if photo.file_path:
        delete_file(photo.file_path)
    
    await db.delete(photo)
    await db.commit()
    return {"message": "Фото удалено"}


@router.delete("/by-url")
async def delete_photo_by_url(
    url: str = Query(..., description="URL фото для удаления (например, /static/photos/filename.jpg)"),
    db: AsyncSession = Depends(get_db),
):
    """
    Удаляет фото по его URL.
    
    URL может быть полным (http://localhost:8000/static/photos/...)
    или относительным (/static/photos/...).
    """
    # Извлекаем путь к файлу из URL
    file_path = extract_filepath_from_url(url)
    if not file_path:
        raise HTTPException(
            status_code=400,
            detail="Некорректный URL. Ожидается URL вида /static/photos/..."
        )
    
    # Проверяем, существует ли файл
    import os
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    # Ищем запись в БД по file_path
    result = await db.execute(select(Photo).where(Photo.file_path == file_path))
    photo = result.scalar_one_or_none()
    
    # Удаляем файл с диска
    delete_file(file_path)
    
    # Если есть запись в БД, удаляем и её
    if photo:
        await db.delete(photo)
        await db.commit()
        return {"message": "Фото удалено (файл и запись в БД)"}
    else:
        await db.commit()  # коммит для завершения транзакции
        return {"message": "Файл удалён (запись в БД не найдена)"}