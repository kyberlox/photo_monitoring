from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.database import get_db
from app.models.media import Media, MediaType
from app.models.location import Location
from app.schemas.media import MediaCreate, MediaUpdate, Media as MediaSchema
from app.utils.file_storage import save_base64_as_file, file_to_base64, delete_file

router = APIRouter(prefix="/media", tags=["media"])


async def enrich_media_with_base64(media: Media) -> MediaSchema:
    """Добавляет base64 данные к медиа (для фото/видео) для ответа."""
    base64_data = None
    if media.media_type in (MediaType.PHOTO, MediaType.VIDEO) and media.file_path:
        base64_data = file_to_base64(media.file_path)
    
    return MediaSchema(
        id=media.id,
        title=media.title,
        comment=media.comment,
        media_type=media.media_type,
        created_at=media.created_at,
        file_path=media.file_path,
        content=media.content,
        location_id=media.location_id,
        base64_data=base64_data,
    )


@router.get("/", response_model=list[MediaSchema])
async def get_media(
    location_id: int = Query(None, description="Фильтр по локации"),
    media_type: MediaType = Query(None, description="Фильтр по типу (photo/video/text)"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Media)
    if location_id is not None:
        query = query.where(Media.location_id == location_id)
    if media_type is not None:
        query = query.where(Media.media_type == media_type)
    
    result = await db.execute(query)
    media_list = result.scalars().all()
    return [await enrich_media_with_base64(m) for m in media_list]


@router.get("/{media_id}", response_model=MediaSchema)
async def get_media_item(media_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    if media is None:
        raise HTTPException(status_code=404, detail="Медиа не найдено")
    return await enrich_media_with_base64(media)


@router.post("/", response_model=MediaSchema)
async def create_media(media_data: MediaCreate, db: AsyncSession = Depends(get_db)):
    # Проверка существования локации
    result = await db.execute(select(Location).where(Location.id == media_data.location_id))
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    file_path = None
    content = media_data.content
    
    # Обработка в зависимости от типа медиа
    if media_data.media_type in (MediaType.PHOTO, MediaType.VIDEO):
        if not media_data.base64_data:
            raise HTTPException(
                status_code=400,
                detail=f"Для типа {media_data.media_type.value} необходимо передать base64_data"
            )
        # Сохраняем файл на диск
        file_path = save_base64_as_file(media_data.base64_data)
        # content не используется для фото/видео
        content = None
    elif media_data.media_type == MediaType.TEXT:
        if not media_data.content:
            raise HTTPException(
                status_code=400,
                detail="Для текстового типа необходимо передать content"
            )
        # file_path не используется для текста
        file_path = None
    
    # Создаем запись в БД
    new_media = Media(
        title=media_data.title,
        comment=media_data.comment,
        media_type=media_data.media_type,
        file_path=file_path,
        content=content,
        location_id=media_data.location_id,
    )
    db.add(new_media)
    await db.commit()
    await db.refresh(new_media)
    
    return await enrich_media_with_base64(new_media)


@router.put("/{media_id}", response_model=MediaSchema)
async def update_media(
    media_id: int,
    media_data: MediaUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    if media is None:
        raise HTTPException(status_code=404, detail="Медиа не найдено")
    
    update_data = media_data.model_dump(exclude_unset=True)
    
    # Если пришел новый base64 для фото/видео
    if "base64_data" in update_data and update_data["base64_data"]:
        if media.media_type not in (MediaType.PHOTO, MediaType.VIDEO):
            raise HTTPException(
                status_code=400,
                detail="base64_data можно обновлять только для фото и видео"
            )
        # Удаляем старый файл
        if media.file_path:
            delete_file(media.file_path)
        # Сохраняем новый
        new_file_path = save_base64_as_file(update_data["base64_data"])
        media.file_path = new_file_path
        # Удаляем base64_data из update_data, чтобы не пытаться записать в модель
        del update_data["base64_data"]
    
    # Если пришел новый content для текста
    if "content" in update_data and update_data["content"] is not None:
        if media.media_type != MediaType.TEXT:
            raise HTTPException(
                status_code=400,
                detail="content можно обновлять только для текстового типа"
            )
        media.content = update_data["content"]
        del update_data["content"]
    
    for field, value in update_data.items():
        setattr(media, field, value)
    
    await db.commit()
    await db.refresh(media)
    return await enrich_media_with_base64(media)


@router.delete("/{media_id}")
async def delete_media(
    media_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalar_one_or_none()
    if media is None:
        raise HTTPException(status_code=404, detail="Медиа не найдено")
    
    # Удаляем файл с диска (если есть)
    if media.file_path:
        delete_file(media.file_path)
    
    await db.delete(media)
    await db.commit()
    return {"message": "Медиа удалено"}