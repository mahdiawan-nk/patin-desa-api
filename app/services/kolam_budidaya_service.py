from fastapi import HTTPException
from beanie import PydanticObjectId
from app.repositories.kolam_budidaya_repository import KolamBudidayaRepository
from app.repositories.user_repository import UserRepository
from app.schemas.kolam_budidaya import (
    KolamBudidayaCreate,
    KolamBudidayaUpdate,
    KolamBudidayaRead,
    UserEmbedded,
)
from datetime import datetime
from app.utils.converters import to_str_id
from typing import List, Optional, Dict, Any


async def create(data: KolamBudidayaCreate):
    user = await UserRepository.get_by_id(data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    kolam = await KolamBudidayaRepository.create(user, data)
    return kolam


async def get_by_id(kolam_id: str):
    kolam = await KolamBudidayaRepository.find_by_id(PydanticObjectId(kolam_id))
    if not kolam:
        raise HTTPException(status_code=404, detail="Kolam tidak ditemukan")
    result = []
    user = await UserRepository.get_by_id(kolam.user_id)
    result.append(KolamBudidayaRead(**kolam.dict(), user=UserEmbedded(**user.dict())))
    return result


async def list_all():
    kolam_list = await KolamBudidayaRepository.find_all()
    result = []

    for i, kolam in enumerate(kolam_list, start=1):
        user = await UserRepository.get_by_id(kolam.user_id)
        result.append(
            KolamBudidayaRead(
                **kolam.dict(),
                user=UserEmbedded(**user.dict()),
                no=i
                )
        )
    return result


async def update(kolam_id: str, data: KolamBudidayaUpdate):
    kolam = await KolamBudidayaRepository.find_by_id(kolam_id)
    update_data = data.dict(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()
    return await KolamBudidayaRepository.update(kolam, update_data)


async def delete(kolam_id: str):
    kolam = await KolamBudidayaRepository.find_by_id(kolam_id)
    await KolamBudidayaRepository.delete(kolam)
    return True


async def get_paginated(
    page: int = 1,
    per_page: int = 10,
    search: Optional[str] = None,
    status: Optional[str] = None,
) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    kolam, total = await KolamBudidayaRepository.get_paginated(
        skip=skip, limit=per_page, search=search, status=status
    )

    kolam_list = []
    for i, k in enumerate(kolam, start=1):
        user = await UserRepository.get_by_id(k.user_id)
        kolam_list.append(
            KolamBudidayaRead(
                **k.dict(),
                user=UserEmbedded(**user.dict()),
                no=skip + i  # penomoran global sesuai pagination
            )
        )

    return {"items": kolam_list, "total": total, "page": page, "per_page": per_page}
