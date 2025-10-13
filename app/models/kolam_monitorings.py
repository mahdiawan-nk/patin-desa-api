from beanie import Document, Link
from pydantic import Field
from datetime import datetime,date
from typing import Optional
from beanie import PydanticObjectId

class KolamMonitoring(Document):
    kolam_budidaya_id: Optional[PydanticObjectId] = None
    tanggal_monitoring: Optional[date] = None
    water_temperature: Optional[float] = None
    water_ph: Optional[float] = None
    oxygen_level: Optional[float] = None
    amonia_level: Optional[float] = None
    keterangan: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "kolam_monitorings"

    class Config:
        allow_population_by_field_name = True