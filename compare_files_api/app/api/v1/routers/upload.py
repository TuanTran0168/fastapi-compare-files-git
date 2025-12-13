from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import file as crud

router = APIRouter()


@router.post("/")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = (await file.read()).decode("utf-8")
    db_file = crud.create_file(db, file.filename, content)
    return {"id": db_file.id, "filename": db_file.filename}
