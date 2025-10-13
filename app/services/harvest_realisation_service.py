from fastapi import HTTPException
from beanie import PydanticObjectId
from app.repositories.harvest_realisation_repository import HarvestRealisationRepository
from app.repositories.kolam_seeding_repository import KolamSeedingRepository
from app.schemas.harvest_realisation import (
    HarvestRealisationCreate,
    HarvestRealisationRead,
    HarvestRealisationUpdate,
    KolamSeedingEmbedded,
)
from datetime import datetime
from app.utils.converters import to_str_id


async def create(data: HarvestRealisationCreate):
    seeding = await KolamSeedingRepository.find_by_id(data.kolam_seeding_id)
    if not seeding:
        raise HTTPException(status_code=404, detail="Seeding tidak ditemukan")

    realisasi = await HarvestRealisationRepository.create(seeding, data)
    return realisasi


async def get_by_id(realisasi_id: str):
    realisasi = await HarvestRealisationRepository.find_by_id(
        PydanticObjectId(realisasi_id)
    )
    if not realisasi:
        raise HTTPException(status_code=404, detail="realisasi tidak ditemukan")
    result = []
    seeding = await KolamSeedingRepository.find_by_id(realisasi.kolam_seeding_id)
    result.append(
        HarvestRealisationRead(
            **realisasi.dict(), seeding=KolamSeedingEmbedded(**seeding.dict())
        )
    )
    return result


async def list_all():
    realisasi_list = await HarvestRealisationRepository.find_all()
    result = []

    for realisasi in realisasi_list:
        seeding = await KolamSeedingRepository.find_by_id(realisasi.kolam_seeding_id)
        result.append(
            HarvestRealisationRead(
                **realisasi.dict(), seeding=KolamSeedingEmbedded(**seeding.dict())
            )
        )
    return result


async def update(realisasi_id: str, data: HarvestRealisationUpdate):
    realisasi = await HarvestRealisationRepository.find_by_id(realisasi_id)
    update_data = data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    return await HarvestRealisationRepository.update(realisasi, update_data)


async def delete(realisasi_id: str):
    estimasi = await HarvestRealisationRepository.find_by_id(realisasi_id)
    return await HarvestRealisationRepository.delete(estimasi)
