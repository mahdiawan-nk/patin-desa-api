from fastapi import HTTPException
from beanie import PydanticObjectId
from app.repositories.kolam_seeding_repository import KolamSeedingRepository
from app.repositories.kolam_budidaya_repository import KolamBudidayaRepository
from app.repositories.user_repository import UserRepository
from app.schemas.kolam_seedings import (
    KolamSeeddingCreate,
    KolamSeedingUpdate,
    KolamSeedingRead,
    KolamBudidayaEmbedded,
)
from datetime import datetime, date
from app.utils.converters import to_str_id
from typing import List, Optional


async def create(data: KolamSeeddingCreate):
    kolam = await KolamBudidayaRepository.find_by_id(data.kolam_budidaya_id)
    if not kolam:
        raise HTTPException(status_code=404, detail="Kolam tidak ditemukan")

    seeding = await KolamSeedingRepository.create(kolam, data)
    return seeding


async def get_by_id(seeding_id: str):
    seeding = await KolamSeedingRepository.find_by_id(PydanticObjectId(seeding_id))
    if not seeding:
        raise HTTPException(status_code=404, detail="Kolam tidak ditemukan")
    result = []
    kolam = await KolamBudidayaRepository.find_by_id(seeding.kolam_budidaya_id)
    result.append(
        KolamSeedingRead(**seeding.dict(), kolam=KolamBudidayaEmbedded(**kolam.dict()))
    )
    return result


async def list_all():
    seeding_list = await KolamSeedingRepository.find_all()
    result = []

    for i, seeding in enumerate(seeding_list, start=1):
        kolam_embedded = None
        if seeding.kolam_budidaya_id:
            kolam_obj = await KolamBudidayaRepository.find_by_id(seeding.kolam_budidaya_id)
            if kolam_obj:
                user_obj = await UserRepository.get_by_id(kolam_obj.user_id) if kolam_obj.user_id else None
                kolam_data = kolam_obj.dict()
                if user_obj:
                    kolam_data["user"] = user_obj.dict()
                kolam_embedded = KolamBudidayaEmbedded(**kolam_data)
        
        result.append(
            KolamSeedingRead(**seeding.dict(), kolam=kolam_embedded, no=i)
        )

    return result


async def update(seeding_id: str, data: KolamSeedingUpdate):
    seeding = await KolamSeedingRepository.find_by_id(seeding_id)
    update_data = data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    return await KolamSeedingRepository.update(seeding, update_data)


async def delete(seeding_id: str):
    kolam = await KolamSeedingRepository.find_by_id(seeding_id)
    await KolamSeedingRepository.delete(kolam)
    return True


async def get_paginated(
    page: int = 1,
    per_page: int = 10,
    search: Optional[str] = None,
    status_seeding: Optional[str] = None,
    owner: Optional[str] = None,
    kolam_budidaya_id: Optional[str] = None,
    tanggal_tebar: Optional[date] = None,
):
    skip = (page - 1) * per_page

    seeding_list, total= await KolamSeedingRepository.get_paginated(
        page=page,
        per_page=per_page,
        search=search,
        status_seeding=status_seeding,
        owner=owner,
        kolam_budidaya_id=kolam_budidaya_id,
        tanggal_tebar=tanggal_tebar,
    )

    return {
        "items": seeding_list,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page,
    }
