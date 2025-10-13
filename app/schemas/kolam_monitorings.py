from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
from beanie import PydanticObjectId
from app.schemas.kolam_budidaya import UserEmbedded


class KolamMonitoringBase(BaseModel):
    tanggal_monitoring: Optional[date] = None
    water_temperature: Optional[float] = None
    water_ph: Optional[float] = None
    oxygen_level: Optional[float] = None
    amonia_level: Optional[float] = None
    keterangan: Optional[str]


class KolamMonitoringCreate(KolamMonitoringBase):
    kolam_budidaya_id: PydanticObjectId


class KolamMonitoringUpdate(KolamMonitoringBase):
    kolam_budidaya_id: Optional[PydanticObjectId]
    tanggal_monitoring: Optional[date] = None
    water_temperature: Optional[float] = None
    water_ph: Optional[float] = None
    oxygen_level: Optional[float] = None
    amonia_level: Optional[float] = None
    keterangan: Optional[str]


class KolamBudidayaEmbedded(BaseModel):
    id: PydanticObjectId
    user_id: PydanticObjectId
    nama_kolam: str
    lokasi_kolam: Optional[str] = None
    panjang: float
    lebar: float
    kedalaman: float
    volume_air: float
    kapasitas: int
    jenis_kolam: str
    status_kolam: str
    user: Optional[UserEmbedded] = None


class KolamMonitoringRead(BaseModel):
    no: Optional[int] = None
    id: PydanticObjectId
    kolam_budidaya_id: Optional[PydanticObjectId] = None
    tanggal_monitoring: Optional[date] = None
    water_temperature: Optional[float] = None
    water_ph: Optional[float] = None
    oxygen_level: Optional[float] = None
    amonia_level: Optional[float] = None
    keterangan: Optional[str]
    kolam: Optional[KolamBudidayaEmbedded] = None
    created_at: datetime
    updated_at: datetime
