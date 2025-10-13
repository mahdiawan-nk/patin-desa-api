from typing import List, Optional
from beanie import PydanticObjectId
from app.models.kolam_seedings import KolamSeeding
from app.models.growth_sampling import GrowthSampling
from app.schemas.growth_sampling import GrowthSamplingCreate

class GrowthSamplingRepository:

    @staticmethod
    async def create(seeding: KolamSeeding, data: GrowthSamplingCreate) -> GrowthSampling:
        sampling = GrowthSampling(
            kolam_seeding_id=seeding.id,  # sekarang user.id sudah ObjectId, jadi aman
            tanggal_sampling=data.tanggal_sampling,
            jumlah_sample=data.jumlah_sample,
            rata_rata_berat=data.rata_rata_berat,
            rata_rata_panjang=data.rata_rata_panjang,
            tingkat_kematian=data.tingkat_kematian,
            catatan=data.catatan
        )
        await sampling.insert()
        return sampling

    @staticmethod
    async def find_by_id(sampling_id: PydanticObjectId) -> Optional[GrowthSampling]:
        return await GrowthSampling.get(sampling_id)

    @staticmethod
    async def find_all() -> List[GrowthSampling]:
        return await GrowthSampling.find_all().to_list()

    @staticmethod
    async def update(sampling: GrowthSampling, data: dict) -> GrowthSampling:
        await sampling.set(data)
        return sampling

    @staticmethod
    async def delete(sampling : GrowthSampling) -> None:
        await sampling.delete()
    
