from beanie import Document, Link
from pydantic import Field
from datetime import datetime,date
from typing import Optional
from beanie import PydanticObjectId

class KolamSeeding(Document):
    kolam_budidaya_id: Optional[PydanticObjectId] = None
    jenis_benih: str
    tanggal_tebar: date
    jumlah_tebar: int
    rata_rata_berat_awal: float
    kepadatan_tebar: float
    status_seeding: str
    catatan: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "kolam_seedings"
