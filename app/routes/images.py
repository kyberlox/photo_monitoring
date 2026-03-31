from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload

from app.database.database import get_db
from app.models.image import Image
from app.models.location import Location
from app.models.user import User
from app.schemas.image import ImageCreate, ImageUpdate, Image as ImageSchema
from app.utils.file_storage import save_base64_as_file, file_to_base64, delete_file

router = APIRouter(prefix="/images", tags=["images"])


async def enrich_image_with_base64(image: Image) -> ImageSchema:
    """Добавляет base64 данные к изображению для ответа."""
    base64_data = file_to_base64(image.file_path) if image.file_path else None
    return ImageSchema(
        id=image.id,
        title=image.title,
        comment=image.comment,
        created_at=image.created_at,
        file_path=image.file_path,
        location_id=image.location_id,
        author_id=image.author_id,
        base64_data=base64_data,
    )


@router.get("/", response_model=list[ImageSchema])
async def get_images(
    location_id: int = Query(None, description="Фильтр по локации"),
    author_id: int = Query(None, description="Фильтр по автору"),
    db: AsyncSession = Depends(get_db),
):
    query = select(Image)
    if location_id is not None:
        query = query.where(Image.location_id == location_id)
    if author_id is not None:
        query = query.where(Image.author_id == author_id)
    
    result = await db.execute(query)
    images = result.scalars().all()
    return [await enrich_image_with_base64(img) for img in images]


@router.get("/{image_id}", response_model=ImageSchema)
async def get_image(image_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()
    if image is None:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    return await enrich_image_with_base64(image)


@router.post("/", response_model=ImageSchema)
async def create_image(image_data: ImageCreate, db: AsyncSession = Depends(get_db)):
    # Проверка существования локации
    result = await db.execute(select(Location).where(Location.id == image_data.location_id))
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    # Проверка существования автора
    result = await db.execute(select(User).where(User.id == image_data.author_id))
    author = result.scalar_one_or_none()
    if author is None:
        raise HTTPException(status_code=404, detail="Автор не найден")
    
    # Сохраняем файл на диск
    file_path = save_base64_as_file(image_data.base64_data)
    
    # Создаем запись в БД
    new_image = Image(
        title=image_data.title,
        comment=image_data.comment,
        file_path=file_path,
        location_id=image_data.location_id,
        author_id=image_data.author_id,
    )
    db.add(new_image)
    await db.commit()
    await db.refresh(new_image)
    
    return await enrich_image_with_base64(new_image)


@router.put("/{image_id}", response_model=ImageSchema)
async def update_image(
    image_id: int,
    image_data: ImageUpdate,
    db: AsyncSession = Depends(get_db),
    # В реальном приложении проверка авторства
):
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()
    if image is None:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    # Проверка прав (только автор может редактировать)
    # if image.author_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Только автор может редактировать изображение")
    
    update_data = image_data.model_dump(exclude_unset=True)
    
    # Если пришел новый base64, обновляем файл
    if "base64_data" in update_data and update_data["base64_data"]:
        # Удаляем старый файл
        delete_file(image.file_path)
        # Сохраняем новый
        new_file_path = save_base64_as_file(update_data["base64_data"])
        image.file_path = new_file_path
        # Удаляем base64_data из update_data, чтобы не пытаться записать в модель
        del update_data["base64_data"]
    
    for field, value in update_data.items():
        setattr(image, field, value)
    
    await db.commit()
    await db.refresh(image)
    return await enrich_image_with_base64(image)


@router.delete("/{image_id}")
async def delete_image(
    image_id: int,
    db: AsyncSession = Depends(get_db),
    # В реальном приложении проверка авторства
):
    result = await db.execute(select(Image).where(Image.id == image_id))
    image = result.scalar_one_or_none()
    if image is None:
        raise HTTPException(status_code=404, detail="Изображение не найдено")
    
    # Проверка прав (только автор может удалять)
    # if image.author_id != current_user.id:
    #     raise HTTPException(status_code=403, detail="Только автор может удалять изображение")
    
    # Удаляем файл с диска
    delete_file(image.file_path)
    
    await db.delete(image)
    await db.commit()
    return {"message": "Изображение удалено"}