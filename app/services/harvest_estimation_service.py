from fastapi import HTTPException
from beanie import PydanticObjectId
from app.repositories.harvest_estimation_repository import HarvestEstimationRepository
from app.repositories.kolam_seeding_repository import KolamSeedingRepository
from app.schemas.harvest_estimation import (
    HarvestEstimationCreate,
    HarvestEstimationRead,
    HarvestEstimationUpdate,
    KolamSeedingEmbedded,
)
from datetime import datetime
from app.utils.converters import to_str_id


async def create(data: HarvestEstimationCreate):
    seeding = await KolamSeedingRepository.find_by_id(data.kolam_seeding_id)
    if not seeding:
        raise HTTPException(status_code=404, detail="Seeding tidak ditemukan")

    estimasi = await HarvestEstimationRepository.create(seeding, data)
    return estimasi


async def get_by_id(estimasi_id: str):
    estimasi = await HarvestEstimationRepository.find_by_id(
        PydanticObjectId(estimasi_id)
    )
    if not estimasi:
        raise HTTPException(status_code=404, detail="sampling tidak ditemukan")
    result = []
    seeding = await KolamSeedingRepository.find_by_id(estimasi.kolam_seeding_id)
    result.append(
        HarvestEstimationRead(
            **estimasi.dict(), seeding=KolamSeedingEmbedded(**seeding.dict())
        )
    )
    return result


async def list_all():
    estimasi_list = await HarvestEstimationRepository.find_all()
    result = []

    for estimasi in estimasi_list:
        seeding = await KolamSeedingRepository.find_by_id(estimasi.kolam_seeding_id)
        result.append(
            HarvestEstimationRead(
                **estimasi.dict(), seeding=KolamSeedingEmbedded(**seeding.dict())
            )
        )
    return result


async def update(estimasi_id: str, data: HarvestEstimationUpdate):
    estimasi = await HarvestEstimationRepository.find_by_id(estimasi_id)
    update_data = data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    return await HarvestEstimationRepository.update(estimasi, update_data)


async def delete(estimasi_id: str):
    estimasi = await HarvestEstimationRepository.find_by_id(estimasi_id)
    return await HarvestEstimationRepository.delete(estimasi)
