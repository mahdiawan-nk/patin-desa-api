from pydantic import BaseModel, Field, field_serializer
from typing import Optional, Literal
from datetime import datetime, date
from beanie import PydanticObjectId
from app.schemas.kolam_budidaya import UserEmbedded


class KolamSeedingBase(BaseModel):
    jenis_benih: str
    tanggal_tebar: date
    jumlah_tebar: int
    rata_rata_berat_awal: float
    kepadatan_tebar: float
    status_seeding: str
    catatan: Optional[str]


class KolamSeeddingCreate(KolamSeedingBase):
    kolam_budidaya_id: PydanticObjectId  # ID User yang akan di-link-kan


class KolamSeedingUpdate(BaseModel):
    jenis_benih: Optional[str]
    tanggal_tebar: Optional[date]
    jumlah_tebar: Optional[int]
    rata_rata_berat_awal: Optional[float]
    kepadatan_tebar: Optional[float]
    status_seeding: Optional[str]
    catatan: Optional[str]


class KolamBudidayaEmbedded(BaseModel):  # Untuk response relasi
    id: PydanticObjectId
    user_id: PydanticObjectId
    nama_kolam: str
    lokasi_kolam: Optional[str] = None
    panjang: float
    lebar: float
    kedalaman: float
    volume_air: float
    kapasitas: int
    jenis_kolam: str
    status_kolam: str
    user: Optional[UserEmbedded] = None


class KolamSeedingRead(BaseModel):
    no: Optional[int]  # nomor urut untuk pagination
    id: PydanticObjectId
    kolam_budidaya_id: Optional[PydanticObjectId] = None
    jenis_benih: str
    tanggal_tebar: datetime
    jumlah_tebar: int
    rata_rata_berat_awal: float
    kepadatan_tebar: float
    status_seeding: str
    catatan: Optional[str] = None
    kolam: Optional[KolamBudidayaEmbedded] = None
    created_at: datetime
    updated_at: datetime
