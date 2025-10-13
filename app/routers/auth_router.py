from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, UserLogin, Token, UserRead,UserRegister, UpdatePassword
# from app.services.user_service import reg
from app.services.auth_service import login_user, get_current_user,register_user, update_user_password
from app.core.response import success_response

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserRead)
async def register(user: UserRegister):
    new_user = await register_user(user)
    return success_response(
        message="Registration successful",
        data=UserRead(
            id=str(new_user.id),
            fullname=new_user.fullname,
            email=new_user.email,
            no_hp=new_user.no_hp,
            nik=new_user.nik,
            jenis_kelamin=new_user.jenis_kelamin,
            tanggal_lahir=new_user.tanggal_lahir,
            alamat_lengkap=new_user.alamat_lengkap,
            tgl_bergabung=new_user.tgl_bergabung,
            status=new_user.status,
            role=new_user.role,
            created_at=new_user.created_at,
            updated_at=new_user.updated_at,
        )
    )

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    return await login_user(user.email, user.password)

@router.get("/me", response_model=UserRead)
async def me(current_user: UserRead = Depends(get_current_user)):
    return success_response(message="Success", data=current_user)

@router.put("/update-password")
async def update_password(
    body: UpdatePassword,
    current_user: UserRead = Depends(get_current_user)
):
    await update_user_password(current_user.id, body.old_password, body.new_password)
    return success_response(message="Password updated successfully")
