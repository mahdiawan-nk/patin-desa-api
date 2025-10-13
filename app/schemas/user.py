from pydantic import BaseModel, EmailStr
from typing import Literal, Optional
from datetime import datetime, date

class UserBase(BaseModel):
    fullname: str
    email: EmailStr
    no_hp: Optional[str] = None
    nik: Optional[str] = None
    jenis_kelamin: Optional[Literal["L", "P"]] = None
    tanggal_lahir: Optional[date] = None
    alamat_lengkap: Optional[str] = None
    tgl_bergabung: Optional[date] = None
    status: Optional[Literal["aktif", "suspend"]] = "aktif"
    role: Optional[Literal["superadmin", "admin", "pembudidaya"]] = "pembudidaya"

class UserRegister(BaseModel):
    fullname: str
    email: EmailStr
    no_hp: Optional[str] = None
    password: str
    
class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    
    # class Config:
    #     orm_mode = True

class UserUpdate(BaseModel):
    fullname: Optional[str] = None
    nik: Optional[str] = None
    jenis_kelamin: Optional[Literal["L", "P"]] = None
    tanggal_lahir: Optional[date] = None
    no_hp: Optional[str] = None
    email: Optional[EmailStr] = None
    alamat_lengkap: Optional[str] = None
    tgl_bergabung: Optional[date] = None
    status: Optional[Literal["aktif", "suspend"]] = None
    password: Optional[str] = None
    token_reset_password: Optional[str] = None
    role: Optional[Literal["superadmin", "admin", "pembudidaya"]] = None

class UserDelete(BaseModel):
    id: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UpdatePassword(BaseModel):
    old_password: str
    new_password: str
class Token(BaseModel):
    access_token: str
    token_type: str