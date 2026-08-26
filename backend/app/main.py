from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.models.database import Base, engine
from app.api.routes import router as api_router

settings = get_settings()

# Create tables if they don't already exist (init.sql handles the Docker path;
# this covers local runs against a fresh database).
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RiskLens API",
    description="Real-time transaction fraud detection API",
    version="1.0.0",
)

origins = [o.strip() for o in settings.CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/")
async def root():
    return {"service": "RiskLens API", "docs": "/docs"}
