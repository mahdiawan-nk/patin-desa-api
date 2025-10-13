from fastapi import APIRouter
from app.schemas.harvest_realisation import HarvestRealisationCreate, HarvestRealisationUpdate
from app.services.harvest_realisation_service import (
    create,
    get_by_id,
    list_all,
    update,
    delete
)
from app.core.response import success_response

router = APIRouter(prefix="/harvest-realisasi", tags=["harvest-realisasi"])

@router.post("/")
async def create_realisation(data: HarvestRealisationCreate):
    realisasi = await create(data)
    return success_response(message="Harvest realisasi berhasil ditambahkan", data=estimasi, status_code=201)

@router.get("/")
async def list_realisation():
    realisasi_list = await list_all()
    return success_response(message="Daftar realisasi berhasil diambil", data=realisasi_list)

@router.get("/{realisasi_id}")
async def detail_realisation(realisasi_id: str):
    realisasi = await get_by_id(realisasi_id)
    return success_response(message="Detail realisasi berhasil diambil", data=realisasi)

@router.put("/{realisasi_id}")
async def update_realisation(realisasi_id: str, data: HarvestRealisationUpdate):
    realisasi = await update(realisasi_id, data)
    return success_response(message="realisasi berhasil diperbarui", data=estimasi)

@router.delete("/{realisasi_id}")
async def delete_realisation(realisasi_id: str):
    await delete(realisasi_id)
    return success_response(message="realisasi berhasil dihapus")
