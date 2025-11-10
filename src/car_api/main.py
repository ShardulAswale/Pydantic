from contextlib import asynccontextmanager
from fastapi import FastAPI
from .routes.car_routes import router as car_router
from .db.mongo import init_mongo, shutdown_mongo

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_mongo()
    try:
        yield
    finally:
        await shutdown_mongo()

app = FastAPI(
    title="Car API",
    version="0.2.0",
    description="Simple CRUD API with HTTP Basic auth (Mongo-backed).",
    docs_url="/swagger",     # <- Swagger UI here
    redoc_url=None,          # <- disable ReDoc (optional)
    openapi_url="/openapi.json",
    lifespan=lifespan,
)
app.include_router(car_router, tags=["cars"])

@app.get("/healthz", tags=["meta"])
async def healthz():
    return {"status": "ok"}
