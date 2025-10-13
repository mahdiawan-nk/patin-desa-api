from typing import List, Optional, Tuple
from beanie import PydanticObjectId
from datetime import datetime, date
from app.models import KolamSeeding, KolamBudidaya,User
from app.schemas.kolam_seedings import KolamSeeddingCreate, KolamSeedingRead, KolamBudidayaEmbedded

class KolamSeedingRepository:

    @staticmethod
    async def create(kolam: KolamBudidaya, data: KolamSeeddingCreate) -> KolamSeeding:
        seeding = KolamSeeding(
            kolam_budidaya_id=kolam.id,  # sekarang user.id sudah ObjectId, jadi aman
            jenis_benih=data.jenis_benih,
            tanggal_tebar=data.tanggal_tebar,
            jumlah_tebar=data.jumlah_tebar,
            rata_rata_berat_awal=data.rata_rata_berat_awal,
            kepadatan_tebar=data.kepadatan_tebar,
            status_seeding=data.status_seeding,
            catatan=data.catatan,
        )
        await seeding.insert()
        return seeding

    @staticmethod
    async def find_by_id(seeding_id: PydanticObjectId) -> Optional[KolamSeeding]:
        return await KolamSeeding.get(seeding_id)

    @staticmethod
    async def find_all() -> List[KolamSeeding]:
        return await KolamSeeding.find_all().to_list()

    @staticmethod
    async def update(seeding: KolamSeeding, data: dict) -> KolamSeeding:
        await seeding.set(data)
        return seeding

    @staticmethod
    async def delete(seeding: KolamSeeding) -> None:
        await seeding.delete()

    @staticmethod
    async def get_paginated(
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        status_seeding: Optional[str] = None,
        owner: Optional[str] = None,
        kolam_budidaya_id: Optional[str] = None,
        tanggal_tebar: Optional[date] = None,
    ) -> Tuple[List[KolamSeedingRead], int]:

        skip = (page - 1) * per_page
        filters = []

        # Filter dasar
        if status_seeding:
            filters.append({"status_seeding": status_seeding})
        if kolam_budidaya_id:
            filters.append({"kolam_budidaya_id": kolam_budidaya_id})
        if tanggal_tebar:
            filters.append({"tanggal_tebar": tanggal_tebar})

        query = {"$and": filters} if filters else {}

        total = await KolamSeeding.find(query).count()
        seedings = await KolamSeeding.find(query).skip(skip).limit(per_page).to_list(length=per_page)

        seeding_list = []
        for i, s in enumerate(seedings, start=1):
            kolam_embedded = None

            if s.kolam_budidaya_id:
                kolam_obj = await KolamBudidaya.get(s.kolam_budidaya_id)
                if kolam_obj:
                    # filter owner
                    if owner and str(kolam_obj.user_id) != str(owner):
                        continue

                    # ambil user
                    user_obj = await User.get(kolam_obj.user_id) if kolam_obj.user_id else None
                    kolam_data = kolam_obj.dict()
                    if user_obj:
                        kolam_data["user"] = user_obj.dict()
                    kolam_embedded = KolamBudidayaEmbedded(**kolam_data)

            # Search gabungan: jenis_benih atau nama_kolam
            match_jenis_benih = search.lower() in s.jenis_benih.lower() if search else True
            match_nama_kolam = True
            if search and kolam_embedded and kolam_embedded.nama_kolam:
                match_nama_kolam = search.lower() in kolam_embedded.nama_kolam.lower()

            if search and not (match_jenis_benih or match_nama_kolam):
                continue

            seeding_list.append(
                KolamSeedingRead(
                    **s.dict(),
                    kolam=kolam_embedded,
                    no=skip + len(seeding_list) + 1
                )
            )

        return seeding_list, total
