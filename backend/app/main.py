from fastapi import FastAPI

from app.api.routes.health import router as health_router

app = FastAPI(
    title="SocietyAPP API",
    version="0.1.0",
    description="Backend API for the SocietyAPP MVP.",
)

app.include_router(health_router)
