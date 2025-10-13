from typing import List, Optional, Union, Dict, Any
from beanie import PydanticObjectId
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead
from app.core import hash_password
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.utils.converters import to_read_model

async def create_user(user_data: UserCreate) -> User:
    existing = await UserRepository.get_by_email(user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(user_data.password)
    user = User(
        fullname=user_data.fullname,
        nik=user_data.nik,
        jenis_kelamin=user_data.jenis_kelamin or None,
        tanggal_lahir=user_data.tanggal_lahir or None,
        no_hp=user_data.no_hp,
        email=user_data.email,
        alamat_lengkap=user_data.alamat_lengkap or None,
        tgl_bergabung=user_data.tgl_bergabung or None,
        status=user_data.status,
        password=hashed_pw,
        role=user_data.role or "pembudidaya",
    )

    return await UserRepository.create(user)


async def get_user_by_id(user_id: PydanticObjectId) -> Optional[UserRead]:
    user = await UserRepository.get_by_id(user_id)
    if not user:
        return None

    return to_read_model(user, UserRead)


async def get_all_users() -> List[UserRead]:
    users = await UserRepository.get_all()
    user_list = []
    for u in users:
        data = u.dict()
        data.pop("id", None)  # hapus id dari dict asli
        user_list.append(UserRead(**data, id=str(u.id)))
    return user_list


async def get_users_paginated(
    page: int = 1,
    per_page: int = 10,
    search: Optional[str] = None,
    status: Optional[str] = None) -> Dict[str, Any]:
    skip = (page - 1) * per_page
    users, total = await UserRepository.get_paginated(skip=skip, limit=per_page, search=search, status=status)

    user_list = []
    for u in users:
        data = u.dict()
        data.pop("password", None)
        data.pop("id", None)
        user_list.append(UserRead(**data, id=str(u.id)))

    return {"items": user_list, "total": total, "page": page, "per_page": per_page}


async def update_user(
    user_id: PydanticObjectId, user_data: UserUpdate
) -> Optional[User]:
    user = await UserRepository.get_by_id(user_id)
    if not user:
        return None

    update_fields = user_data.dict(exclude_unset=True)
    for field, value in update_fields.items():
        if field == "password":
            setattr(user, "password", hash_password(value))
        else:
            setattr(user, field, value)

    user.update_timestamp()
    return await UserRepository.update(user)


async def delete_user(user_id: PydanticObjectId) -> bool:
    user = await UserRepository.get_by_id(user_id)
    if not user:
        return False
    return await UserRepository.delete(user)


# async def authenticate_user(email: str, password: str) -> Optional[User]:
#     user = await UserRepository.get_by_email(email)
#     if not user:
#         return None
#     if not user.verify_password(password):
#         return None
#     return user
