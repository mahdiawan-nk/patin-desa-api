from beanie import Document, Link
from pydantic import Field
from datetime import datetime,date
from typing import Optional
from beanie import PydanticObjectId

class GrowthSampling(Document):
    kolam_seeding_id: Optional[PydanticObjectId] = None
    tanggal_sampling: date
    jumlah_sample: int
    rata_rata_berat: float
    rata_rata_panjang: float
    tingkat_kematian: int
    catatan: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "growth_sampling"
