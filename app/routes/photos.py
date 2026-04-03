from fastapi import APIRouter, Depends, HTTPException, Query, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.database import get_db
from app.models.photo import Photo
from app.models.location import Location
from app.schemas.photo import PhotoCreate, PhotoUpdate, Photo as PhotoSchema
from app.utils.file_storage import save_upload_file, generate_file_url, delete_file

router = APIRouter(prefix="/photos", tags=["photos"])


async def enrich_photo_with_url(photo: Photo) -> PhotoSchema:
    """Добавляет URL к фото для ответа."""
    file_url = None
    if photo.file_path:
        file_url = generate_file_url(photo.file_path)
    
    return PhotoSchema(
        id=photo.id,
        title=photo.title,
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


@router.post("/add", response_model=PhotoSchema)
async def create_photo(
    title: str = Form(...),
    comment: Optional[str] = Form(None),
    location_id: int = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    # Проверка существования локации
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    # Сохраняем файл на диск
    file_path = save_upload_file(file)
    
    # Создаем запись в БД
    new_photo = Photo(
        title=title,
        comment=comment,
        file_path=file_path,
        location_id=location_id,
    )
    db.add(new_photo)
    await db.commit()
    await db.refresh(new_photo)
    
    return await enrich_photo_with_url(new_photo)


@router.put("/id={photo_id}", response_model=PhotoSchema)
async def update_photo(
    photo_id: int,
    title: Optional[str] = Form(None),
    comment: Optional[str] = Form(None),
    file: UploadFile = File(None),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if photo is None:
        raise HTTPException(status_code=404, detail="Фото не найдено")
    
    update_data = {}
    if title is not None:
        update_data["title"] = title
    if comment is not None:
        update_data["comment"] = comment
    
    # Если пришел новый файл
    if file is not None and file.filename:
        # Удаляем старый файл
        if photo.file_path:
            delete_file(photo.file_path)
        # Сохраняем новый
        new_file_path = save_upload_file(file)
        photo.file_path = new_file_path
    
    for field, value in update_data.items():
        setattr(photo, field, value)
    
    await db.commit()
    await db.refresh(photo)
    return await enrich_photo_with_url(photo)


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