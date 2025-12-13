from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from app.crud import file as crud
from app.db.session import get_db
from app.schemas import file

router = APIRouter()


@router.post("/", response_model=file.FileResponse)
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    content = await file.read()
    ext = file.filename.split(".")[-1].lower()
    filetype = "pdf" if ext == "pdf" else "txt"
    db_file = crud.create_file(db, filename=file.filename, content=content, filetype=filetype)
    return db_file
