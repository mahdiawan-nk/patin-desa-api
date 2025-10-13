from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from app.models.kolam_budidaya import KolamBudidaya
from app.models.kolam_seedings import KolamSeeding
from app.models.kolam_feedings import KolamFeeding
from app.models.growth_sampling import GrowthSampling
from app.models.harvest_estimation import HarvestEstimation
from app.models.harvest_realisation import HarvestRealisation
from app.models.kolam_monitorings import KolamMonitoring
from datetime import datetime
from passlib.hash import bcrypt


async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URI)
    db = client[settings.DB_NAME]

    await init_beanie(
        database=db,
        document_models=[
            User,
            KolamBudidaya,
            KolamMonitoring,
            KolamSeeding,
            KolamFeeding,
            GrowthSampling,
            HarvestEstimation,
            HarvestRealisation,
        ],
    )

    # Buat default superadmin jika belum ada
    admin_email = settings.DEFAULT_ADMIN_EMAIL
    existing_admin = await User.find_one(User.email == admin_email)

    if not existing_admin:
        default_user = User(
            fullname="Administrator",
            email=admin_email,
            password=bcrypt.hash(settings.DEFAULT_ADMIN_PASSWORD),
            role="superadmin",
            status="aktif",
            tgl_bergabung=datetime.utcnow().date(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
        )
        await default_user.insert()
        print(f"Default superadmin created: {admin_email}")
