from fastapi import HTTPException
from beanie import PydanticObjectId
from app.repositories import KolamMonitoringRepository,KolamBudidayaRepository,UserRepository
from app.schemas.kolam_monitorings import (
    KolamMonitoringCreate,
    KolamMonitoringUpdate,
    KolamMonitoringRead,
    KolamBudidayaEmbedded,
)
from datetime import datetime,date
from typing import List, Optional

async def create(data: KolamMonitoringCreate):
    kolam = await KolamBudidayaRepository.find_by_id(data.kolam_budidaya_id)
    if not kolam:
        raise HTTPException(status_code=404, detail="Kolam tidak ditemukan")

    monitoring = await KolamMonitoringRepository.create(kolam, data)
    return monitoring

async def get_by_id(monitoring_id:str):
    monitoring = await KolamMonitoringRepository.find_by_id(PydanticObjectId(monitoring_id))
    if not monitoring:
        raise HTTPException(status_code=404, detail="Kolam tidak ditemukan")
    result = []
    kolam = await KolamBudidayaRepository.find_by_id(monitoring.kolam_budidaya_id)
    result.append(
        KolamMonitoringRead(**monitoring.dict(), kolam=KolamBudidayaEmbedded(**kolam.dict()))
    )
    return result

async def list_all():
    monitoring_list = await KolamMonitoringRepository.find_all()
    result = []

    for i, monitoring in enumerate(monitoring_list, start=1):
        kolam_embedded = None
        if monitoring.kolam_budidaya_id:
            kolam_obj = await KolamBudidayaRepository.find_by_id(monitoring.kolam_budidaya_id)
            if kolam_obj:
                user_obj = await UserRepository.get_by_id(kolam_obj.user_id) if kolam_obj.user_id else None
                kolam_data = kolam_obj.dict()
                if user_obj:
                    kolam_data["user"] = user_obj.dict()
                kolam_embedded = KolamBudidayaEmbedded(**kolam_data)
        
        result.append(
            KolamMonitoringRead(**monitoring.dict(), kolam=kolam_embedded, no=i)
        )
            
    return result

async def update(monitoring_id: str, data: KolamMonitoringUpdate):
    monitoring = await KolamMonitoringRepository.find_by_id(PydanticObjectId(monitoring_id))
    if not monitoring:
        raise HTTPException(status_code=404, detail="Kolam tidak ditemukan")
    update_data = data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    monitoring = await KolamMonitoringRepository.update(monitoring, update_data)
    return monitoring

async def delete(monitoring_id: str):
    monitoring = await KolamMonitoringRepository.find_by_id(PydanticObjectId(monitoring_id))
    if not monitoring:
        raise HTTPException(status_code=404, detail="Kolam tidak ditemukan")
    await KolamMonitoringRepository.delete(monitoring)
    return True

async def get_paginated(
    page: int = 1,
    per_page: int = 10,
    search: Optional[str] = None,
    owner: Optional[str] = None,
    kolam_budidaya_id: Optional[str] = None,
    tanggal_monitoring: Optional[date] = None,
):
   monitoring_list,total = await KolamMonitoringRepository.get_paginated(
        page=page, per_page=per_page, search=search, owner=owner, kolam_budidaya_id=kolam_budidaya_id, tanggal_monitoring=tanggal_monitoring
    )
   return {
        "items": monitoring_list,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (len(monitoring_list) + per_page - 1) // per_page,
    }