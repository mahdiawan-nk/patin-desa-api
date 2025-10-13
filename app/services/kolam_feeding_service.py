from fastapi import HTTPException
from beanie import PydanticObjectId
from app.repositories.kolam_feeding_repository import KolamFeedingRepository
from app.repositories.kolam_seeding_repository import KolamSeedingRepository
from app.schemas.kolam_feedings import (
    KolamFeedingCreate,
    KolamFeedingUpdate,
    KolamFeedingRead,
    KolamSeedingEmbedded,
)
from datetime import datetime
from app.utils.converters import to_str_id
from typing import List, Optional


async def create(data: KolamFeedingCreate):
    seeding = await KolamSeedingRepository.find_by_id(data.kolam_seeding_id)
    if not seeding:
        raise HTTPException(status_code=404, detail="Seeding tidak ditemukan")

    feeding = await KolamFeedingRepository.create(seeding, data)
    return feeding


async def get_by_id(feeding_id: str):
    feeding = await KolamFeedingRepository.find_by_id(PydanticObjectId(feeding_id))
    if not feeding:
        raise HTTPException(status_code=404, detail="Feeding tidak ditemukan")
    result = []
    seeding = await KolamSeedingRepository.find_by_id(feeding.kolam_seeding_id)
    result.append(
        KolamFeedingRead(
            **feeding.dict(), seeding=KolamSeedingEmbedded(**seeding.dict())
        )
    )
    return result


async def list_all():
    feeding_list = await KolamFeedingRepository.find_all()
    result = []

    for feeding in feeding_list:
        seeding = await KolamSeedingRepository.find_by_id(feeding.kolam_seeding_id)
        result.append(
            KolamFeedingRead(
                **feeding.dict(), seeding=KolamSeedingEmbedded(**seeding.dict())
            )
        )
    return result


async def update(feeding_id: str, data: KolamFeedingUpdate):
    feeding = await KolamFeedingRepository.find_by_id(feeding_id)
    update_data = data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    return await KolamFeedingRepository.update(feeding, update_data)


async def delete(feeding_id: str):
    feeding = await KolamFeedingRepository.find_by_id(feeding_id)
    return await KolamFeedingRepository.delete(feeding)


async def get_paginated(
    page: int = 1,
    per_page: int = 10,
    search: Optional[str] = None,
    owner: Optional[str] = None,
    kolam_budidaya_id: Optional[str] = None,
    seeding_id: Optional[str] = None,
):
    skip = (page - 1) * per_page

    feedings_list, total = await KolamFeedingRepository.get_paginated_feedings(
        page=page,
        per_page=per_page,
        search=search,
        owner=owner,
        kolam_budidaya_id=kolam_budidaya_id,
        kolam_seeding_id=seeding_id,
    )

    return {
        "items": feedings_list,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page,
    }
