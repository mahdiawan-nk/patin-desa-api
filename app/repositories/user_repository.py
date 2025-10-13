from typing import List, Optional
from beanie import PydanticObjectId
from app.models.user import User


class UserRepository:

    @staticmethod
    async def create(user: User) -> User:
        await user.insert()
        return user

    @staticmethod
    async def get_by_id(user_id: PydanticObjectId) -> Optional[User]:
        return await User.get(user_id)

    @staticmethod
    async def get_by_email(email: str) -> Optional[User]:
        return await User.find_one(User.email == email)

    @staticmethod
    async def get_all() -> List[User]:
        return await User.find_all().to_list()

    @staticmethod
    async def update(user: User) -> User:
        await user.save()
        return user

    @staticmethod
    async def delete(user: User) -> bool:
        await user.delete()
        return True
    
    @staticmethod
    async def get_paginated(skip: int = 0, limit: int = 10, search: Optional[str] = None, status: Optional[str] = None):
        filters = []
        if search:
            filters.append(
                {
                    "$or": [
                        {"fullname": {"$regex": search, "$options": "i"}},
                        {"email": {"$regex": search, "$options": "i"}}
                    ]
                }
            )
        if status:
            filters.append({"status": status})
        query = {"$and": filters} if filters else {}
        total = await User.find(query).count()
        users = await User.find(query).skip(skip).limit(limit).to_list(length=limit)
        return users, total
