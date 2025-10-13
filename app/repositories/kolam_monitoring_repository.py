from typing import List, Optional, Tuple
from beanie import PydanticObjectId
from datetime import datetime, date
from app.models import KolamMonitoring, KolamBudidaya,User
from app.schemas.kolam_monitorings import (
    KolamMonitoringCreate,
    KolamMonitoringRead,
    KolamBudidayaEmbedded,
)

class KolamMonitoringRepository:
    @staticmethod
    async def create(kolam: KolamBudidaya, data: KolamMonitoringCreate) -> KolamMonitoring:
        monitoring = KolamMonitoring(
            kolam_budidaya_id=kolam.id, 
            tanggal_monitoring=data.tanggal_monitoring,
            water_temperature=data.water_temperature,
            water_ph=data.water_ph,
            oxygen_level=data.oxygen_level,
            amonia_level=data.amonia_level,
            keterangan=data.keterangan,
        )
        await monitoring.insert()
        return monitoring
    
    @staticmethod
    async def find_by_id(monitoring_id: PydanticObjectId) -> Optional[KolamMonitoring]:
        return await KolamMonitoring.get(monitoring_id)
    
    @staticmethod
    async def find_all() -> List[KolamMonitoring]:
        return await KolamMonitoring.find().to_list()
    
    @staticmethod
    async def update(monitoring: KolamMonitoring, data: dict) -> KolamMonitoring:
        await monitoring.set(data)
        return monitoring
    
    @staticmethod
    async def delete(monitoring: KolamMonitoring):
        await monitoring.delete()
    
    @staticmethod
    async def get_paginated(
        page: int = 1,
        per_page: int = 10,
        search: Optional[str] = None,
        owner: Optional[str] = None,
        kolam_budidaya_id: Optional[str] = None,
        tanggal_monitoring: Optional[date] = None,
    ) -> Tuple[List[KolamMonitoringRead], int]:
        skip = (page - 1) * per_page
        filters = []

        # Filter dasar
        if kolam_budidaya_id:
            filters.append({"kolam_budidaya_id": PydanticObjectId(kolam_budidaya_id)})
        if tanggal_monitoring:
            filters.append({"tanggal_monitoring": tanggal_monitoring})

        query = {"$and": filters} if filters else {}

        total = await KolamMonitoring.find(query).count()
        monitorings = await KolamMonitoring.find(query).skip(skip).limit(per_page).to_list(length=per_page)

        monitoring_list = []
        for i, m in enumerate(monitorings, start=1):
            kolam_embedded = None
            
            if m.kolam_budidaya_id:
                kolam_obj = await KolamBudidaya.get(m.kolam_budidaya_id)
                if kolam_obj:
                    #filter owner
                    if owner and str(kolam_obj.user_id) != str(owner):
                        continue
                    
                    #ambil user
                    user_obj = await User.get(kolam_obj.user_id) if kolam_obj.user_id else None
                    kolam_data = kolam_obj.dict()
                    if user_obj:
                        kolam_data["user"] = user_obj.dict()
                    kolam_embedded = KolamBudidayaEmbedded(**kolam_data)
            
            match_nama_kolam = True
            if search and kolam_embedded and kolam_embedded.nama_kolam:
                match_nama_kolam = search.lower() in kolam_embedded.nama_kolam.lower()
            
            if search and not match_nama_kolam:
                continue

            monitoring_list.append(
                KolamMonitoringRead(
                    **m.dict(), kolam=kolam_embedded, no=skip + len(monitoring_list) + 1
                )
            )

        return monitoring_list, total
                