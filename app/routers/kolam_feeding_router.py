from fastapi import APIRouter, HTTPException, Query
from app.schemas.kolam_feedings import KolamFeedingCreate, KolamFeedingUpdate
from app.services.kolam_feeding_service import (
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

router = APIRouter(prefix="/feedings", tags=["feedings"])


@router.post("/")
async def create_feeding(data: KolamFeedingCreate):
    feeding = await create(data)
    return success_response(
        message="PPemeberian pakan berhasil ditambahkan", data=feeding, status_code=201
    )


@router.get("/")
async def list_feeding(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None, description="Search keyword"),
    owner: Optional[str] = Query(None, description="Filter by owner"),
    kolam_budidya_id: Optional[str] = Query(
        None, description="Filter by kolam budidaya"
    ),
    seeding_id: Optional[str] = Query(None, description="Filter by seeding"),
):
    feeding_list = await get_paginated(
        page=page,
        per_page=per_page,
        search=q,
        owner=owner,
        kolam_budidaya_id=kolam_budidya_id,
        seeding_id=seeding_id,
    )
    return paginated_response(
            items=feeding_list["items"],
            total=feeding_list["total"],
            page=feeding_list["page"],
            per_page=feeding_list["per_page"]
        )


@router.get("/{feeding_id}")
async def detail_feeding(feeding_id: str):
    kolam = await get_by_id(feeding_id)
    return success_response(message="Detail penebaran berhasil diambil", data=kolam)


@router.put("/{feeding_id}")
async def update_feeding(feeding_id: str, data: KolamFeedingUpdate):
    kolam = await update(feeding_id, data)
    return success_response(message="Penebaran berhasil diperbarui", data=kolam)


@router.delete("/{feeding_id}")
async def delete_feeding(feeding_id: str):
    await delete(feeding_id)
    return success_response(message="Penebaran berhasil dihapus")
