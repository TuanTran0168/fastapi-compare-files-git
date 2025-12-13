from sqlalchemy.orm import Session
from app.db import models

def create_file(db: Session, filename: str, content: bytes, filetype: str):
    db_file = models.File(filename=filename, content=content, filetype=filetype)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id).first()

def list_files(db: Session):
    return db.query(models.File).all()
