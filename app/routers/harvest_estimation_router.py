from fastapi import APIRouter
from app.schemas.harvest_estimation import HarvestEstimationCreate, HarvestEstimationUpdate
from app.services.harvest_estimation_service import (
    create,
    get_by_id,
    list_all,
    update,
    delete
)
from app.core.response import success_response

router = APIRouter(prefix="/harvest-estimation", tags=["harvest-estimation"])

@router.post("/")
async def create_estimation(data: HarvestEstimationCreate):
    estimasi = await create(data)
    return success_response(message="Harvest estimation berhasil ditambahkan", data=estimasi, status_code=201)

@router.get("/")
async def list_estimation():
    estimation_list = await list_all()
    return success_response(message="Daftar estimasi berhasil diambil", data=estimation_list)

@router.get("/{estimasi_id}")
async def detail_estimation(estimasi_id: str):
    estimasi = await get_by_id(estimasi_id)
    return success_response(message="Detail estimasi berhasil diambil", data=estimasi)

@router.put("/{estimasi_id}")
async def update_estimation(estimasi_id: str, data: HarvestEstimationUpdate):
    estimasi = await update(estimasi_id, data)
    return success_response(message="estimasi berhasil diperbarui", data=estimasi)

@router.delete("/{estimasi_idd}")
async def delete_estimasi(estimasi_idd: str):
    await delete(estimasi_idd)
    return success_response(message="estimasi berhasil dihapus")
