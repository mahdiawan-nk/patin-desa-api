from beanie import Document,before_event
from pydantic import Field, EmailStr
from typing import Literal, Optional
from datetime import datetime, date
from app.models.kolam_budidaya import KolamBudidaya

class User(Document):
    fullname: str = Field(..., max_length=100)
    email: EmailStr = Field(...)
    nik: Optional[str] = Field(default=None, max_length=20)
    jenis_kelamin: Optional[Literal["L", "P"]] = Field(
        default=None
    )  # L = Laki-laki, P = Perempuan
    tanggal_lahir: Optional[date] = Field(default=None)
    no_hp: Optional[str] = Field(default=None)
    alamat_lengkap: Optional[str] = Field(default=None)
    tgl_bergabung: Optional[date] = Field(default=None)
    status: Optional[Literal["aktif", "suspend"]] = Field(default="aktif")
    password: str = Field(...)
    role: Literal["superadmin", "admin", "pembudidaya"] = Field(default="pembudidaya")
    token_reset_password: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"  # Nama koleksi
        # indexes = [
        #     {"key": {"email": 'text'}},
        #     {"key": {"fullname": 'text'}},
        # ]

    class Config:
        populate_by_name = True
        

    def update_timestamp(self):
        self.updated_at = datetime.utcnow()
    
@before_event("delete")
async def cascade_delete_kolam(self):
    """Hapus semua kolam yang terkait dengan user ini sebelum user dihapus"""
    await KolamBudidaya.find(KolamBudidaya.user.id == self.id).delete()
