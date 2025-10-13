from pydantic import BaseModel, Field, field_serializer
from typing import Optional, Literal
from datetime import datetime, date
from beanie import PydanticObjectId

class GrowthSamplingBase(BaseModel):
    tanggal_sampling: date
    jumlah_sample: int
    rata_rata_berat: float
    rata_rata_panjang: float
    tingkat_kematian: int
    catatan: Optional[str]


class GrowthSamplingCreate(GrowthSamplingBase):
    kolam_seeding_id: PydanticObjectId  # ID User yang akan di-link-kan


class GrowthSamplingUpdate(BaseModel):
    tanggal_sampling: date
    jumlah_sample: int
    rata_rata_berat: float
    rata_rata_panjang: float
    tingkat_kematian: int
    catatan: Optional[str]


class KolamSeedingEmbedded(BaseModel):  # Untuk response relasi
    id: PydanticObjectId
    jenis_benih: str
    tanggal_tebar: date
    jumlah_tebar: int
    rata_rata_berat_awal: float
    kepadatan_tebar: float
    status_seeding: str
    

class GrowthSamplingRead(GrowthSamplingBase):
    id: PydanticObjectId
    seeding: Optional[KolamSeedingEmbedded] = None
    created_at: datetime
    updated_at: datetime

