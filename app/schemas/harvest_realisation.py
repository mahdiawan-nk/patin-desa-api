from pydantic import BaseModel, Field, field_serializer
from typing import Optional, Literal
from datetime import datetime, date
from beanie import PydanticObjectId

class HarvestRealisationBase(BaseModel):
    tanggal_panen: date
    berat_total: float
    jumlah_ikan: float
    rata_rata_panjang: Optional[float] = None
    catatan: Optional[str]


class HarvestRealisationCreate(HarvestRealisationBase):
    kolam_seeding_id: PydanticObjectId  # ID User yang akan di-link-kan


class HarvestRealisationUpdate(BaseModel):
    tanggal_panen: date
    berat_total: float
    jumlah_ikan: float
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
    

class HarvestRealisationRead(HarvestRealisationBase):
    id: PydanticObjectId
    seeding: Optional[KolamSeedingEmbedded] = None
    created_at: datetime
    updated_at: datetime

