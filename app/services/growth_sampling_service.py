from fastapi import HTTPException
from beanie import PydanticObjectId
from app.repositories.growth_sampling_repository import GrowthSamplingRepository
from app.repositories.kolam_seeding_repository import KolamSeedingRepository
from app.schemas.growth_sampling import (
    GrowthSamplingCreate,
    GrowthSamplingUpdate,
    GrowthSamplingRead,
    KolamSeedingEmbedded
)
from datetime import datetime
from app.utils.converters import to_str_id


async def create(data: GrowthSamplingCreate):
    seeding = await KolamSeedingRepository.find_by_id(data.kolam_seeding_id)
    if not seeding:
        raise HTTPException(status_code=404, detail="Seeding tidak ditemukan")

    sampling = await GrowthSamplingRepository.create(seeding, data)
    return sampling


async def get_by_id(sampling_id: str):
    sampling = await GrowthSamplingRepository.find_by_id(PydanticObjectId(sampling_id))
    if not sampling:
        raise HTTPException(status_code=404, detail="sampling tidak ditemukan")
    result = []
    seeding = await KolamSeedingRepository.find_by_id(sampling.kolam_seeding_id)
    result.append(
        GrowthSamplingRead(**sampling.dict(), seeding=KolamSeedingEmbedded(**seeding.dict()))
    )
    return result


async def list_all():
    sampling_list = await GrowthSamplingRepository.find_all()
    result = []
    
    for sampling in sampling_list:
        seeding = await KolamSeedingRepository.find_by_id(sampling.kolam_seeding_id)
        result.append(
            GrowthSamplingRead(**sampling.dict(), seeding=KolamSeedingEmbedded(**seeding.dict()))
        )
    return result

async def update(sampling_id: str, data: GrowthSamplingUpdate):
    sampling = await GrowthSamplingRepository.find_by_id(sampling_id)
    update_data = data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    return await GrowthSamplingRepository.update(sampling, update_data)



async def delete(sampling_id: str):
    sampling = await GrowthSamplingRepository.find_by_id(sampling_id)
    return await GrowthSamplingRepository.delete(sampling)