from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.database import get_db
from app.models.photo import Photo
from app.models.location import Location
from app.schemas.photo import PhotoCreate, PhotoUpdate, Photo as PhotoSchema
from app.utils.file_storage import save_base64_as_file, file_to_base64, delete_file

router = APIRouter(prefix="/photos", tags=["photos"])


async def enrich_photo_with_base64(photo: Photo) -> PhotoSchema:
    """Добавляет base64 данные к фото для ответа."""
    base64_data = None
    if photo.file_path:
        base64_data = file_to_base64(photo.file_path)
    
    return PhotoSchema(
        id=photo.id,
        title=photo.title,
        comment=photo.comment,
        created_at=photo.created_at,
        file_path=photo.file_path,
        location_id=photo.location_id,
        base64_data=base64_data,
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
    return [await enrich_photo_with_base64(p) for p in photos_list]


@router.get("/id={photo_id}", response_model=PhotoSchema)
async def get_photo(photo_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if photo is None:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    return await enrich_photo_with_base64(photo)


@router.post("/add", response_model=PhotoSchema)
async def create_photo(photo_data: PhotoCreate, db: AsyncSession = Depends(get_db)):
    # Проверка существования локации
    result = await db.execute(select(Location).where(Location.id == photo_data.location_id))
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    if not photo_data.base64_data:
        raise HTTPException(
            status_code=400,
            detail="Для фото необходимо передать base64_data"
        )
    
    # Сохраняем файл на диск
    file_path = save_base64_as_file(photo_data.base64_data)
    
    # Создаем запись в БД
    new_photo = Photo(
        title=photo_data.title,
        comment=photo_data.comment,
        file_path=file_path,
        location_id=photo_data.location_id,
    )
    db.add(new_photo)
    await db.commit()
    await db.refresh(new_photo)
    
    return await enrich_photo_with_base64(new_photo)


@router.put("/id={photo_id}", response_model=PhotoSchema)
async def update_photo(
    photo_id: int,
    photo_data: PhotoUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if photo is None:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    
    update_data = photo_data.model_dump(exclude_unset=True)
    
    # Если пришел новый base64
    if "base64_data" in update_data and update_data["base64_data"]:
        # Удаляем старый файл
        if photo.file_path:
            delete_file(photo.file_path)
        # Сохраняем новый
        new_file_path = save_base64_as_file(update_data["base64_data"])
        photo.file_path = new_file_path
        # Удаляем base64_data из update_data, чтобы не пытаться записать в модель
        del update_data["base64_data"]
    
    for field, value in update_data.items():
        setattr(photo, field, value)
    
    await db.commit()
    await db.refresh(photo)
    return await enrich_photo_with_base64(photo)


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