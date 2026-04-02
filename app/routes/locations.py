from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.database.database import get_db
from app.models.location import Location
from app.models.photo import Photo
from app.schemas.location import LocationCreate, LocationUpdate, Location as LocationSchema
from app.utils.file_storage import save_base64_as_file

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/all", response_model=list[LocationSchema])
async def get_locations(db: AsyncSession = Depends(get_db)):
    from app.routes.photos import enrich_photo_with_base64
    result = await db.execute(
        select(Location).options(selectinload(Location.photos))
    )
    locations = result.scalars().all()
    
    enriched_locations = []
    for loc in locations:
        # Создаём объект схемы из модели локации
        loc_schema = LocationSchema.model_validate(loc, from_attributes=True)
        # Обогащаем фото base64
        enriched_photos = []
        for photo in loc.photos:
            enriched_photos.append(await enrich_photo_with_base64(photo))
        # Заменяем photos в схеме
        loc_schema.photos = enriched_photos
        enriched_locations.append(loc_schema)
    
    return enriched_locations


@router.get("/id={location_id}", response_model=LocationSchema)
async def get_location(location_id: int, db: AsyncSession = Depends(get_db)):
    from app.routes.photos import enrich_photo_with_base64
    result = await db.execute(
        select(Location)
        .where(Location.id == location_id)
        .options(selectinload(Location.photos))
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    # Обогащаем фото base64
    enriched_photos = []
    for photo in location.photos:
        enriched_photos.append(await enrich_photo_with_base64(photo))
    location.photos = enriched_photos
    return location



@router.post("/add", response_model=LocationSchema)
async def create_location(
    location_data: LocationCreate, db: AsyncSession = Depends(get_db)
):
    # Извлекаем фото из запроса (если есть)
    photos_list = location_data.photos
    # Удаляем поле photos из данных локации, т.к. в модели Location его нет
    location_dict = location_data.model_dump(exclude={"photos"})
    
    new_location = Location(**location_dict)
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    
    # Если есть фото, создаём их
    if photos_list:
        for photo_item in photos_list:
            file_path = None
            
            # Обработка base64 данных для фото
            if photo_item.base64_data:
                file_path = save_base64_as_file(
                    base64_data=photo_item.base64_data,
                    filename=None  # автоматически сгенерирует имя
                )
            
            # Создаём объект Photo
            new_photo = Photo(
                title=photo_item.title,
                comment=photo_item.comment,
                file_path=file_path,
                location_id=new_location.id
            )
            db.add(new_photo)
        
        await db.commit()
    
    # Перезагружаем локацию с фото
    from app.routes.photos import enrich_photo_with_base64
    result = await db.execute(
        select(Location)
        .where(Location.id == new_location.id)
        .options(selectinload(Location.photos))
    )
    new_location = result.scalar_one()
    # Обогащаем фото base64
    enriched_photos = []
    for photo in new_location.photos:
        enriched_photos.append(await enrich_photo_with_base64(photo))
    new_location.photos = enriched_photos
    
    return new_location


@router.put("/id={location_id}", response_model=LocationSchema)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    db: AsyncSession = Depends(get_db),
):
    from app.routes.photos import enrich_photo_with_base64
    result = await db.execute(
        select(Location)
        .where(Location.id == location_id)
        .options(selectinload(Location.photos))
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    update_data = location_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    
    await db.commit()
    # Перезагружаем локацию с фото
    result = await db.execute(
        select(Location)
        .where(Location.id == location_id)
        .options(selectinload(Location.photos))
    )
    location = result.scalar_one()
    # Обогащаем фото base64
    enriched_photos = []
    for photo in location.photos:
        enriched_photos.append(await enrich_photo_with_base64(photo))
    location.photos = enriched_photos
    return location


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