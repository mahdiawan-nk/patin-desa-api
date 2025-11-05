from fastapi import FastAPI
from app.database import init_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from app.routers import (
    kolam_budidaya_router,
    user_router,
    auth_router,
    kolam_seeding_router,
    kolam_feeding_router,
    growth_sampling_router,
    harvest_estimation_router,
    harvest_realisation_router,
    kolam_monitoring_router,
)
from fastapi.responses import JSONResponse
from fastapi.requests import Request

app = FastAPI()

app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["api.patindesa.com", "patindesa.com", "localhost", "127.0.0.1"]
)

origins = [
    "https://patindesa.com",
    "http://patindesa.com"
    "https://api.patindesa.com",
    "http://localhost:3000",  # Nuxt/Vue/React Dev
    "http://127.0.0.1:3000",  # kadang beda akses
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ["*"] kalau mau semua origin (kurang aman)
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, OPTIONS
    allow_headers=["*"],  # biar bisa kirim Authorization, Content-Type, dll
)

app.router.redirect_slashes = False

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": str(exc)},
    )
    
@app.on_event("startup")
async def startup():
    await init_db()


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(kolam_budidaya_router)
app.include_router(kolam_monitoring_router)
app.include_router(kolam_seeding_router)
app.include_router(kolam_feeding_router)
app.include_router(growth_sampling_router)
app.include_router(harvest_estimation_router)
app.include_router(harvest_realisation_router)
