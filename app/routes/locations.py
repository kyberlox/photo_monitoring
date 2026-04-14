from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.database.database import get_db
from app.models.location import Location
from app.models.photo import Photo
from app.schemas.location import Location as LocationSchema
from app.utils.file_storage import save_upload_file
from app.routes.photos import enrich_photo_with_url

router = APIRouter(prefix="/api/locations", tags=["locations"])


@router.get("/all", response_model=list[LocationSchema])
async def get_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Location).options(selectinload(Location.photos))
    )
    locations = result.scalars().all()
    
    enriched_locations = []
    for loc in locations:
        # Создаём объект схемы из модели локации
        loc_schema = LocationSchema.model_validate(loc, from_attributes=True)
        # Обогащаем фото URL
        enriched_photos = []
        for photo in loc.photos:
            enriched_photos.append(await enrich_photo_with_url(photo))
        # Заменяем photos в схеме
        loc_schema.photos = enriched_photos
        enriched_locations.append(loc_schema)
    
    return enriched_locations


@router.get("/id={location_id}", response_model=LocationSchema)
async def get_location(location_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Location)
        .where(Location.id == location_id)
        .options(selectinload(Location.photos))
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    # Создаём схему локации
    location_schema = LocationSchema.model_validate(location, from_attributes=True)
    # Обогащаем фото URL
    enriched_photos = []
    for photo in location.photos:
        enriched_photos.append(await enrich_photo_with_url(photo))
    location_schema.photos = enriched_photos
    return location_schema


@router.post("/add", response_model=LocationSchema)
async def create_location(
    name: Optional[str] = Form(None),
    coord_x: float = Form(...),
    coord_y: float = Form(...),
    photos: List[UploadFile] = File([]),
    db: AsyncSession = Depends(get_db),
):
    # Создаём локацию
    new_location = Location(
        name=name,
        coordinates=[coord_x, coord_y]
    )
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    
    # Если есть фото, создаём их
    if photos:
        for photo_file in photos:
            if photo_file.filename:  # игнорируем пустые файлы
                file_path = save_upload_file(photo_file)
                new_photo = Photo(
                    comment=None,
                    file_path=file_path,
                    location_id=new_location.id
                )
                db.add(new_photo)
        
        await db.commit()
    
    # Перезагружаем локацию с фото
    result = await db.execute(
        select(Location)
        .where(Location.id == new_location.id)
        .options(selectinload(Location.photos))
    )
    new_location = result.scalar_one()
    # Создаём схему локации
    location_schema = LocationSchema.model_validate(new_location, from_attributes=True)
    # Обогащаем фото URL
    enriched_photos = []
    for photo in new_location.photos:
        enriched_photos.append(await enrich_photo_with_url(photo))
    location_schema.photos = enriched_photos
    
    return location_schema


@router.put("/id={location_id}")#, response_model=LocationSchema)
async def update_location(
    location_id: int,
    name: Optional[str] = Form(None),
    coord_x: Optional[float] = Form(None),
    coord_y: Optional[float] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Location)
        .where(Location.id == location_id)
        .options(selectinload(Location.photos))
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    if name is not None:
        location.name = name
    if coord_x is not None and coord_y is not None:
        location.coordinates = [coord_x, coord_y]
    elif coord_x is not None:
        location.coordinates = [coord_x, location.coordinates[1]]
    elif coord_y is not None:
        location.coordinates = [location.coordinates[0], coord_y]
    elif coord_x is None and coord_y is None:
        location.coordinates = location.coordinates
        # raise HTTPException(
        #     status_code=400,
        #     detail="Необходимо передать обе координаты (coord_x и coord_y)"
        # )
    
    await db.commit()
    # Перезагружаем локацию с фото
    result = await db.execute(
        select(Location)
        .where(Location.id == location_id)
        .options(selectinload(Location.photos))
    )
    location = result.scalar_one()
    # Создаём схему локации
    location_schema = LocationSchema.model_validate(location, from_attributes=True)
    # Обогащаем фото URL
    enriched_photos = []
    for photo in location.photos:
        enriched_photos.append(await enrich_photo_with_url(photo))
    location_schema.photos = enriched_photos
    return location_schema


@router.delete("/id={location_id}")
async def delete_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Location)
        .where(Location.id == location_id)
        .options(selectinload(Location.photos))
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    await db.delete(location)
    await db.commit()
    return {"message": "Локация и все связанные фото удалены"}