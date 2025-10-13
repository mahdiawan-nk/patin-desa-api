from typing import List, Optional
from beanie import PydanticObjectId
from app.models.kolam_budidaya import KolamBudidaya
from app.models.user import User
from app.schemas.kolam_budidaya import KolamBudidayaCreate

class KolamBudidayaRepository:

    @staticmethod
    async def create(user: User, data: KolamBudidayaCreate) -> KolamBudidaya:
        kolam = KolamBudidaya(
            user_id=user.id,  # sekarang user.id sudah ObjectId, jadi aman
            nama_kolam=data.nama_kolam,
            lokasi_kolam=data.lokasi_kolam,
            panjang=data.panjang,
            lebar=data.lebar,
            kedalaman=data.kedalaman,
            volume_air=data.volume_air,
            kapasitas=data.kapasitas,
            jenis_kolam=data.jenis_kolam,
            status_kolam=data.status_kolam
        )
        await kolam.insert()
        return kolam

    @staticmethod
    async def find_by_id(kolam_id: PydanticObjectId) -> Optional[KolamBudidaya]:
        return await KolamBudidaya.get(kolam_id)

    @staticmethod
    async def find_all() -> List[KolamBudidaya]:
        return await KolamBudidaya.find_all().to_list()

    @staticmethod
    async def update(kolam: KolamBudidaya, data: dict) -> KolamBudidaya:
        await kolam.set(data)
        return kolam

    @staticmethod
    async def delete(kolam: KolamBudidaya) -> None:
        await kolam.delete()
    
    @staticmethod
    async def get_paginated(skip: int = 0, limit: int = 10, search: Optional[str] = None, status: Optional[str] = None):
        filters = []
        if search:
            filters.append(
                {
                    "$or": [
                        {"nama_kolam": {"$regex": search, "$options": "i"}},
                        {"lokasi_kolam": {"$regex": search, "$options": "i"}}
                    ]
                }
            )
        if status:
            filters.append({"status_kolam": status})
        query = {"$and": filters} if filters else {}
        total = await KolamBudidaya.find(query).count()
        kolam = await KolamBudidaya.find(query).skip(skip).limit(limit).to_list(length=limit)
        return kolam, total
        