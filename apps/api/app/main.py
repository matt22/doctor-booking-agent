from fastapi import FastAPI

from app.health import router as health_router

app = FastAPI(
    title="Doctor Booking Agent API",
    summary="Educational simulation for Northstar Demo Clinic. Not for real appointments.",
    version="0.1.0",
)
app.include_router(health_router)
