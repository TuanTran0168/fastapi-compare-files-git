from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import file as crud
from app.utils.diff_utils import generate_diff_html

router = APIRouter()


@router.get("/{new_file_id}/{old_file_id}")
def compare_files(new_file_id: int, old_file_id: int, db: Session = Depends(get_db)):
    new_file = crud.get_file(db, new_file_id)
    old_file = crud.get_file(db, old_file_id)
    if not new_file or not old_file:
        raise HTTPException(status_code=404, detail="File not found")
    diff = generate_diff_html(old_file.content, new_file.content, old_file.filename, new_file.filename)
    return HTMLResponse(content=diff)

