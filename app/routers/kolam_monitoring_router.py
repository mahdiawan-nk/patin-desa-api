from fastapi import APIRouter, HTTPException, Query
from app.schemas.kolam_monitorings import KolamMonitoringCreate, KolamMonitoringUpdate
from app.services.kolam_monitoring_service import (
    create,
    get_by_id,
    list_all,
    update,
    delete,
    get_paginated,
)
from app.core.response import success_response, paginated_response
from app.utils.converters import to_read_model
from typing import List, Optional
from datetime import datetime, date

router = APIRouter(prefix="/kolam-monitorings", tags=["monitorings-kolam"])


@router.post("/", response_model=KolamMonitoringCreate)
async def create_kolam_monitoring(kolam_monitoring: KolamMonitoringCreate):
    monitoring = await create(kolam_monitoring)
    return success_response(
        message="Monitoring kolam berhasil ditambahkan",
        data=monitoring,
        status_code=201,
    )

@router.get("/")
async def list_kolam_monitoring(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None, description="Search keyword"),
    owner: Optional[str] = Query(None, description="Filter by owner"),
    kolam_budidaya_id: Optional[str] = Query(None, description="Filter by kolam budidaya"),
    tanggal_monitoring: Optional[date] = Query(None, description="Filter by tanggal monitoring"),
):
    monitoring_list = await get_paginated(
        page=page,
        per_page=per_page,
        search=q,
        owner=owner,
        kolam_budidaya_id=kolam_budidaya_id,
        tanggal_monitoring=tanggal_monitoring,
    )
    
    return paginated_response(
        items=monitoring_list["items"],
        total=monitoring_list["total"],
        page=monitoring_list["page"],
        per_page=monitoring_list["per_page"]
    )

@router.get("/{kolam_monitoring_id}")
async def detail_monitoring(kolam_monitoring_id: str):
    monitoring = await get_by_id(kolam_monitoring_id)
    if not monitoring:
        raise HTTPException(status_code=404, detail="Monitoring not found")
    return success_response(message="Success", data=monitoring)

@router.put("/{kolam_monitoring_id}")
async def update_monitoring(kolam_monitoring_id: str, monitoring_update: KolamMonitoringUpdate):
    monitoring = await update(kolam_monitoring_id, monitoring_update)
    return success_response(message="Success", data=monitoring)

@router.delete("/{kolam_monitoring_id}")
async def delete_monitoring(kolam_monitoring_id: str):
    monitoring = await delete(kolam_monitoring_id)
    return success_response(message="Success", data=monitoring)
    