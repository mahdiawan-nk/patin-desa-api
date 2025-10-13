from fastapi import APIRouter
from app.schemas.growth_sampling import GrowthSamplingCreate, GrowthSamplingUpdate
from app.services.growth_sampling_service import (
    create,
    get_by_id,
    list_all,
    update,
    delete
)
from app.core.response import success_response
from app.utils.converters import to_read_model

router = APIRouter(prefix="/sampling", tags=["sampling"])

@router.post("/")
async def create_sampling(data: GrowthSamplingCreate):
    sampling = await create(data)
    return success_response(message="Sampling berhasil ditambahkan", data=sampling, status_code=201)

@router.get("/")
async def list_sampling():
    sampling_list = await list_all()
    return success_response(message="Daftar sampling berhasil diambil", data=sampling_list)

@router.get("/{sampling_id}")
async def detail_sampling(sampling_id: str):
    sampling = await get_by_id(sampling_id)
    return success_response(message="Detail penebaran berhasil diambil", data=sampling)

@router.put("/{sampling_id}")
async def update_sampling(sampling_id: str, data: GrowthSamplingUpdate):
    sampling = await update(sampling_id, data)
    return success_response(message="sampling berhasil diperbarui", data=sampling)

@router.delete("/{sampling_id}")
async def delete_sampling(sampling_id: str):
    await delete(sampling_id)
    return success_response(message="sampling berhasil dihapus")
