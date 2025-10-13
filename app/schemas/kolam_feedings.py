from pydantic import BaseModel, Field, field_serializer
from typing import Optional, Literal
from datetime import datetime, date
from beanie import PydanticObjectId
from app.schemas.kolam_seedings import KolamBudidayaEmbedded
class KolamFeedingBase(BaseModel):
    nama_pakan: str
    tanggal_pemberian: date
    jumlah_pakan: float
    frekuensi: int
    catatan: Optional[str]


class KolamFeedingCreate(KolamFeedingBase):
    kolam_seeding_id: PydanticObjectId  # ID User yang akan di-link-kan


class KolamFeedingUpdate(BaseModel):
    nama_pakan: str
    tanggal_pemberian: date
    jumlah_pakan: float
    frekuensi: int
    catatan: Optional[str]


class KolamSeedingEmbedded(BaseModel):  # Untuk response relasi
    id: PydanticObjectId
    jenis_benih: str
    tanggal_tebar: date
    jumlah_tebar: int
    rata_rata_berat_awal: float
    kepadatan_tebar: float
    status_seeding: str
    

class KolamFeedingRead(BaseModel):
    no: Optional[int]
    id: PydanticObjectId
    kolam_seeding_id: Optional[PydanticObjectId] = None
    nama_pakan: str
    tanggal_pemberian: date
    jumlah_pakan: float
    frekuensi: int
    catatan: Optional[str]
    seeding: Optional[KolamSeedingEmbedded] = None
    kolam: Optional[KolamBudidayaEmbedded] = None
    created_at: datetime
    updated_at: datetime

