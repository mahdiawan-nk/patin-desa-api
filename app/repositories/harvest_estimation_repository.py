from typing import List, Optional
from beanie import PydanticObjectId
from app.models.kolam_seedings import KolamSeeding
from app.models.harvest_estimation import HarvestEstimation
from app.schemas.harvest_estimation import HarvestEstimationCreate

class HarvestEstimationRepository:

    @staticmethod
    async def create(seeding: KolamSeeding, data: HarvestEstimationCreate) -> HarvestEstimation:
        estimation = HarvestEstimation(
            kolam_seeding_id=seeding.id,  # sekarang user.id sudah ObjectId, jadi aman
            tanggal_estimasi=data.tanggal_estimasi,
            perkiraan_berat_total=data.perkiraan_berat_total,
            perkiraan_jumlah=data.perkiraan_jumlah,
            rata_rata_panjang=data.rata_rata_panjang,
            catatan=data.catatan
        )
        await estimation.insert()
        return estimation

    @staticmethod
    async def find_by_id(estimasi_id: PydanticObjectId) -> Optional[HarvestEstimation]:
        return await HarvestEstimation.get(estimasi_id)

    @staticmethod
    async def find_all() -> List[HarvestEstimation]:
        return await HarvestEstimation.find_all().to_list()

    @staticmethod
    async def update(estimasi: HarvestEstimation, data: dict) -> HarvestEstimation:
        await estimasi.set(data)
        return estimasi

    @staticmethod
    async def delete(estimasi : HarvestEstimation) -> None:
        await estimasi.delete()
    
