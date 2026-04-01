from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database.database import get_db
from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate, Location as LocationSchema

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/", response_model=list[LocationSchema])
async def get_locations(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Location)  # убрали selectinload, т.к. media временно не загружаем
    )
    locations = result.scalars().all()
    return locations


@router.get("/{location_id}", response_model=LocationSchema)
async def get_location(location_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Location)
        .where(Location.id == location_id)
        # убрали selectinload, т.к. media временно не загружаем
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    return location


@router.post("/", response_model=LocationSchema)
async def create_location(
    location_data: LocationCreate, db: AsyncSession = Depends(get_db)
):
    new_location = Location(**location_data.model_dump())
    db.add(new_location)
    await db.commit()
    await db.refresh(new_location)
    return new_location


@router.put("/{location_id}", response_model=LocationSchema)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Location).where(Location.id == location_id))
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    update_data = location_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(location, field, value)
    
    await db.commit()
    await db.refresh(location)
    return location


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Location)
        .where(Location.id == location_id)
        .options(selectinload(Location.media))
    )
    location = result.scalar_one_or_none()
    if location is None:
        raise HTTPException(status_code=404, detail="Локация не найдена")
    
    await db.delete(location)
    await db.commit()
    return {"message": "Локация и все связанные медиа удалены"}