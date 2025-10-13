from typing import List, Optional
from beanie import PydanticObjectId
from app.models.kolam_seedings import KolamSeeding
from app.models.harvest_realisation import HarvestRealisation
from app.schemas.harvest_realisation import HarvestRealisationCreate

class HarvestRealisationRepository:

    @staticmethod
    async def create(seeding: KolamSeeding, data: HarvestRealisationCreate) -> HarvestRealisation:
        realisasi = HarvestRealisation(
            kolam_seeding_id=seeding.id,  # sekarang user.id sudah ObjectId, jadi aman
            tanggal_panen=data.tanggal_panen,
            berat_total=data.berat_total,
            jumlah_ikan=data.jumlah_ikan,
            rata_rata_panjang=data.rata_rata_panjang,
            catatan=data.catatan
        )
        await realisasi.insert()
        return realisasi

    @staticmethod
    async def find_by_id(realisasi_id: PydanticObjectId) -> Optional[HarvestRealisation]:
        return await HarvestRealisation.get(realisasi_id)

    @staticmethod
    async def find_all() -> List[HarvestRealisation]:
        return await HarvestRealisation.find_all().to_list()

    @staticmethod
    async def update(realisi: HarvestRealisation, data: dict) -> HarvestRealisation:
        await realisi.set(data)
        return realisi

    @staticmethod
    async def delete(realisasi : HarvestRealisation) -> None:
        await realisasi.delete()
    
