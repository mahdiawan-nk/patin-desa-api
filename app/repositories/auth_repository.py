from typing import Optional
from beanie import PydanticObjectId
from app.models.user import User


class AuthRepository:

    @staticmethod
    async def get_by_email(email: str) -> Optional[User]:
        return await User.find_one(User.email == email)

    @staticmethod
    async def get_by_id(user_id: PydanticObjectId) -> Optional[User]:
        return await User.get(user_id)
