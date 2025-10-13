from beanie import Document, Link
from pydantic import Field
from datetime import datetime,date
from typing import Optional
from beanie import PydanticObjectId

class KolamFeeding(Document):
    kolam_seeding_id: Optional[PydanticObjectId] = None
    nama_pakan: str
    tanggal_pemberian: date
    jumlah_pakan: float
    frekuensi: int
    catatan: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "kolam_feedings"
