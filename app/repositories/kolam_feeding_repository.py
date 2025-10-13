from typing import List, Optional, Tuple
from beanie import PydanticObjectId
from app.models import KolamFeeding, KolamSeeding, KolamBudidaya, User
from app.schemas.kolam_feedings import (
    KolamFeedingCreate,
    KolamFeedingRead,
    KolamSeedingEmbedded,
)
from app.schemas.kolam_seedings import KolamBudidayaEmbedded


class KolamFeedingRepository:

    @staticmethod
    async def create(seeding: KolamSeeding, data: KolamFeedingCreate) -> KolamFeeding:
        feeding = KolamFeeding(
            kolam_seeding_id=seeding.id,  # sekarang user.id sudah ObjectId, jadi aman
            nama_pakan=data.nama_pakan,
            tanggal_pemberian=data.tanggal_pemberian,
            jumlah_pakan=data.jumlah_pakan,
            frekuensi=data.frekuensi,
            catatan=data.catatan,
        )
        await feeding.insert()
        return feeding

    @staticmethod
    async def find_by_id(feeding_id: PydanticObjectId) -> Optional[KolamFeeding]:
        return await KolamFeeding.get(feeding_id)

    @staticmethod
    async def find_all() -> List[KolamFeeding]:
        return await KolamFeeding.find_all().to_list()

    @staticmethod
    async def update(feeding: KolamFeeding, data: dict) -> KolamFeeding:
        await feeding.set(data)
        return feeding

    @staticmethod
    async def delete(feeding: KolamFeeding) -> None:
        await feeding.delete()

    @staticmethod
    async def get_paginated_feedings(
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        owner: Optional[str] = None,
        kolam_seeding_id: Optional[str] = None,
        kolam_budidaya_id: Optional[str] = None,  # <--- filter baru
    ) -> Tuple[List[KolamFeedingRead], int]:

        skip = (page - 1) * per_page
        filters = []

        # filter dasar
        if kolam_seeding_id:
            filters.append({"kolam_seeding_id": PydanticObjectId(kolam_seeding_id)})

        query = {"$and": filters} if filters else {}

        total = await KolamFeeding.find(query).count()
        feedings = await KolamFeeding.find(query).skip(skip).limit(per_page).to_list(length=per_page)

        feeding_list = []

        for i, f in enumerate(feedings, start=1):
            seeding_embedded = None
            kolam_embedded = None

            if f.kolam_seeding_id:
                seeding_obj = await KolamSeeding.get(f.kolam_seeding_id)
                if seeding_obj:
                    # ambil kolam budidaya
                    if seeding_obj.kolam_budidaya_id:
                        kolam_obj = await KolamBudidaya.get(seeding_obj.kolam_budidaya_id)
                        if kolam_obj:
                            # filter owner
                            if owner and str(kolam_obj.user_id) != str(owner):
                                continue
                            # filter kolam_budidaya_id
                            if kolam_budidaya_id and str(kolam_obj.id) != str(kolam_budidaya_id):
                                continue

                            user_obj = await User.get(kolam_obj.user_id) if kolam_obj.user_id else None
                            kolam_data = kolam_obj.dict()
                            if user_obj:
                                kolam_data["user"] = user_obj.dict()
                            kolam_embedded = KolamBudidayaEmbedded(**kolam_data)

                    seeding_data = seeding_obj.dict()
                    seeding_embedded = KolamSeedingEmbedded(**seeding_data)

                    # search: nama_pakan / jenis_benih / nama_kolam
                    match_nama_pakan = search.lower() in f.nama_pakan.lower() if search else True
                    match_jenis_benih = search.lower() in seeding_obj.jenis_benih.lower() if search else True
                    match_nama_kolam = search.lower() in kolam_obj.nama_kolam.lower() if search and kolam_obj else True

                    if search and not (match_nama_pakan or match_jenis_benih or match_nama_kolam):
                        continue

            feeding_list.append(
                KolamFeedingRead(
                    **f.dict(),
                    seeding=seeding_embedded,
                    kolam=kolam_embedded,
                    no=skip + len(feeding_list) + 1
                )
            )

        return feeding_list, total
