from beanie import Document, Link
from pydantic import Field
from datetime import datetime
from typing import Optional
from beanie import PydanticObjectId

class KolamBudidaya(Document):
    user_id: Optional[PydanticObjectId] = None
    nama_kolam: str
    lokasi_kolam: Optional[str]
    panjang: float
    lebar: float
    kedalaman: float
    volume_air: float
    kapasitas: int
    jenis_kolam: str
    status_kolam: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "kolam_budidaya"
