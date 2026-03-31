from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.services.db_service import DatabaseService
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    db_service = DatabaseService()
    await db_service.init_db()
    yield

app = FastAPI(
    title="GlobalAI Data Comparison API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "GlobalAI API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

