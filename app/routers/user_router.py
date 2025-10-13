from fastapi import APIRouter, HTTPException, status, Depends, Query
from beanie import PydanticObjectId
from typing import List, Optional

from app.core.response import success_response, paginated_response
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services.user_service import (
    create_user,
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user,
    get_users_paginated,
)

from app.services.auth_service import get_current_user
from app.utils.converters import to_read_model, to_read_model_list

router = APIRouter(prefix="/users", tags=["Users"])
# router = APIRouter(prefix="/users", tags=["Users"], dependencies=[Depends(get_current_user)])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_new_user(user_data: UserCreate):
    user = await create_user(user_data)
    return success_response(message="Success", data=to_read_model(user, UserRead))


@router.get("/", response_model=None)
async def list_users(
    paginate: bool = Query(True),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None, description="Search keyword"),
    status: Optional[str] = Query(None, description="Filter by status"),
):
    if paginate:
        result = await get_users_paginated(
            page=page, per_page=per_page, search=q, status=status
        )

        return paginated_response(
            items=result["items"],
            total=result["total"],
            page=result["page"],
            per_page=result["per_page"],
        )
    else:
        users = await get_all_users()
        return success_response(
            message="Success", data=to_read_model_list(users, UserRead)
        )


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: PydanticObjectId):
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(message="Success", data=user)


@router.put("/{user_id}", response_model=UserRead)
async def update_existing_user(user_id: PydanticObjectId, user_data: UserUpdate):
    updated_user = await update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(
        message="Success", data=to_read_model(updated_user, UserRead)
    )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_user(user_id: PydanticObjectId):
    deleted = await delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return success_response(message="Success deleted")


#
