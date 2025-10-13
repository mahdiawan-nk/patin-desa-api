from pydantic import BaseModel, Field, field_serializer
from typing import Optional, Literal
from datetime import datetime, date
from beanie import PydanticObjectId

class HarvestEstimationBase(BaseModel):
    tanggal_estimasi: date
    perkiraan_berat_total: float
    perkiraan_jumlah: float
    rata_rata_panjang: Optional[float] = None
    catatan: Optional[str]


class HarvestEstimationCreate(HarvestEstimationBase):
    kolam_seeding_id: PydanticObjectId  # ID User yang akan di-link-kan


class HarvestEstimationUpdate(BaseModel):
    tanggal_estimasi: date
    perkiraan_berat_total: float
    perkiraan_jumlah: float
    rata_rata_panjang: Optional[float] = None
    catatan: Optional[str]


class KolamSeedingEmbedded(BaseModel):  # Untuk response relasi
    id: PydanticObjectId
    jenis_benih: str
    tanggal_tebar: date
    jumlah_tebar: int
    rata_rata_berat_awal: float
    kepadatan_tebar: float
    status_seeding: str
    

class HarvestEstimationRead(HarvestEstimationBase):
    id: PydanticObjectId
    seeding: Optional[KolamSeedingEmbedded] = None
    created_at: datetime
    updated_at: datetime

