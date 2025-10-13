from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user import Token, UserRead, UserCreate
from app.core.security import (
    verify_password,
    create_access_token,
    decode_access_token,
    get_password_hash,
    hash_password,
)
from beanie import PydanticObjectId
from app.repositories.auth_repository import AuthRepository
from app.repositories.user_repository import UserRepository
from app.models.user import User
from fastapi import HTTPException

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login-v2")


async def register_user(user_data: UserCreate) -> User:
    existing = await UserRepository.get_by_email(user_data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    hashed_pw = hash_password(user_data.password)
    user = User(
        fullname=user_data.fullname,
        email=user_data.email,
        no_hp=user_data.no_hp,
        password=hashed_pw,
        status="aktif",
        role="pembudidaya",
    )
    return await UserRepository.create(user)


async def authenticate_user(email: str, password: str):
    user = await AuthRepository.get_by_email(email)
    if not user or not verify_password(password, user.password):
        return None
    return user


async def login_user(email: str, password: str) -> Token:
    user = await authenticate_user(email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    token = create_access_token({"sub": str(user.id)})
    return Token(access_token=token, token_type="bearer")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserRead:
    user_id = decode_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = await AuthRepository.get_by_id(PydanticObjectId(user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserRead(
        id=str(user.id),
        fullname=user.fullname,
        nik=user.nik,
        jenis_kelamin=user.jenis_kelamin,
        tanggal_lahir=user.tanggal_lahir,
        no_hp=user.no_hp,
        email=user.email,
        alamat_lengkap=user.alamat_lengkap,
        tgl_bergabung=user.tgl_bergabung,
        status=user.status,
        role=user.role,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


async def update_user_password(user_id: str, old_password: str, new_password: str):
    # ambil user berdasarkan ID
    user = await UserRepository.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # cek password lama
    if not verify_password(old_password, user.password):
        raise HTTPException(status_code=400, detail="Old password is incorrect")

    # update password baru (hashed)
    user.password = get_password_hash(new_password)
    await user.save()  # Beanie style
    return True
