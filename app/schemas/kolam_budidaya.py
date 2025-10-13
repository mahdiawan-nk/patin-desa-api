from pydantic import BaseModel, Field, field_serializer
from typing import Optional, Literal
from datetime import datetime, date
from beanie import PydanticObjectId

class KolamBudidayaBase(BaseModel):
    nama_kolam: str
    lokasi_kolam: Optional[str]
    panjang: float
    lebar: float
    kedalaman: float
    volume_air: float
    kapasitas: int
    jenis_kolam: str
    status_kolam: str


class KolamBudidayaCreate(KolamBudidayaBase):
    user_id: PydanticObjectId  # ID User yang akan di-link-kan


class KolamBudidayaUpdate(BaseModel):
    user_id: Optional[PydanticObjectId]
    nama_kolam: Optional[str]
    lokasi_kolam: Optional[str]
    panjang: Optional[float]
    lebar: Optional[float]
    kedalaman: Optional[float]
    volume_air: Optional[float]
    kapasitas: Optional[int]
    jenis_kolam: Optional[str]
    status_kolam: Optional[str]


class UserEmbedded(BaseModel):  # Untuk response relasi
    id: PydanticObjectId
    fullname: str
    email: str
    nik: Optional[str]
    jenis_kelamin: Optional[str]
    tanggal_lahir: Optional[datetime]
    no_hp: Optional[str]
    alamat_lengkap: Optional[str]
    tgl_bergabung: Optional[datetime]
    status: str
    


class KolamBudidayaRead(KolamBudidayaBase):
    no: Optional[int] = None
    id: PydanticObjectId
    user: Optional[UserEmbedded] = None
    created_at: datetime
    updated_at: datetime

