from fastapi import APIRouter, HTTPException, status, Depends, Query
from app.schemas.kolam_budidaya import KolamBudidayaCreate, KolamBudidayaUpdate, KolamBudidayaRead
from app.repositories.kolam_budidaya_repository import KolamBudidayaRepository
from app.services.kolam_budidaya_service import (
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
router = APIRouter(prefix="/kolam", tags=["Kolam Budidaya"])

@router.post("")
async def create_kolam(data: KolamBudidayaCreate):
    kolam = await create(data)
    return success_response(message="Kolam berhasil ditambahkan", data=kolam, status_code=201)

@router.get("")
async def list_kolam(
    paginate: bool = Query(True),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None, description="Search keyword"),
    status: Optional[str] = Query(None, description="Filter by status")
):
    if paginate:
        result = await get_paginated(page=page, per_page=per_page, search=q, status=status)
        return paginated_response(
            items=result["items"],
            total=result["total"],
            page=result["page"],
            per_page=result["per_page"]
        )
    else:
        kolam = await list_all()
        return success_response(
            message="Success", data=kolam
        )
  

@router.get("{kolam_id}")
async def detail_kolam(kolam_id: str):
    kolam = await get_by_id(kolam_id)
    return success_response(message="Detail kolam berhasil diambil", data=kolam[0])

@router.put("{kolam_id}")
async def update_kolam(kolam_id: str, data: KolamBudidayaUpdate):
    kolam = await update(kolam_id, data)
    return success_response(message="Kolam berhasil diperbarui", data=kolam)

@router.delete("{kolam_id}")
async def delete_kolam(kolam_id: str):
    await delete(kolam_id)
    return success_response(message="Kolam berhasil dihapus")
