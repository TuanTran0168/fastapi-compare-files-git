from fastapi import FastAPI
from app.api.v1.routers import upload, compare, compare_old
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="File Compare App")

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(compare_old.router, prefix="/compare-old", tags=["Compare-Old"])
app.include_router(compare.router, prefix="/compare", tags=["Compare"])
