from beanie import Document, Link
from pydantic import Field
from datetime import datetime,date
from typing import Optional
from beanie import PydanticObjectId

class HarvestEstimation(Document):
    kolam_seeding_id: Optional[PydanticObjectId] = None
    tanggal_estimasi: date
    perkiraan_berat_total: float
    perkiraan_jumlah: float
    rata_rata_panjang: Optional[float] = None
    catatan: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "harvest_estimation"
