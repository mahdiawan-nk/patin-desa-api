from fastapi import APIRouter, HTTPException, Query
from app.schemas.kolam_seedings import KolamSeeddingCreate, KolamSeedingUpdate
from app.services.kolam_seeding_service import (
    create,
    get_by_id,
    list_all,
    update,
    delete,
    get_paginated
)
from app.core.response import success_response, paginated_response
from app.utils.converters import to_read_model
from typing import List, Optional
from datetime import datetime, date
router = APIRouter(prefix="/seedings", tags=["seedings"])


@router.post("")
async def create_seeding(data: KolamSeeddingCreate):
    seeding = await create(data)
    return success_response(
        message="Penebaran Benih berhasil ditambahkan", data=seeding, status_code=201
    )


@router.get("")
async def list_seeding(
    paginate: bool = Query(True),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None, description="Search keyword"),
    status_seeding: Optional[str] = Query(None, description="Filter by status"),
    owner: Optional[str] = Query(None, description="Filter by owner"),
    kolam_budidya_id: Optional[str] = Query(None, description="Filter by kolam budidaya"),
    tanggal_tebar: Optional[date] = Query(None, description="Filter by tanggal tebar")
):
    if paginate:
        seeding_list = await get_paginated(
            page=page,
            per_page=per_page,
            search=q,
            status_seeding=status_seeding,
            owner=owner,
            kolam_budidaya_id=kolam_budidya_id,
            tanggal_tebar=tanggal_tebar
        )
        return paginated_response(
            items=seeding_list["items"],
            total=seeding_list["total"],
            page=seeding_list["page"],
            per_page=seeding_list["per_page"]
        )
    else:
        kolam = await list_all()
        return success_response(
            message="Success", data=kolam
        )


@router.get("/{seeding_id}")
async def detail_seeding(seeding_id: str):
    kolam = await get_by_id(seeding_id)
    return success_response(message="Detail penebaran berhasil diambil", data=kolam)


@router.put("/{seeding_id}")
async def update_seeding(seeding_id: str, data: KolamSeedingUpdate):
    kolam = await update(seeding_id, data)
    return success_response(message="Penebaran berhasil diperbarui", data=kolam)


@router.delete("/{seeding_id}")
async def delete_seeding(seeding_id: str):
    await delete(seeding_id)
    return success_response(message="Penebaran berhasil dihapus")
