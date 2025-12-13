from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud import file as crud
from app.utils.diff_utils import generate_diff_html_old
from app.utils.pdf_utils import extract_text_from_pdf

router = APIRouter()


@router.get("/{new_file_id}/{old_file_id}")
def compare_files_old(new_file_id: int, old_file_id: int, db: Session = Depends(get_db)):
    new_file = crud.get_file(db, new_file_id)
    old_file = crud.get_file(db, old_file_id)
    if not new_file or not old_file:
        raise HTTPException(status_code=404, detail="File not found")

    # Convert bytes -> str
    if old_file.filetype == "pdf":
        old_text = extract_text_from_pdf(old_file.content)
    else:
        old_text = old_file.content.decode("utf-8")

    if new_file.filetype == "pdf":
        new_text = extract_text_from_pdf(new_file.content)
    else:
        new_text = new_file.content.decode("utf-8")

    diff = generate_diff_html_old(old_text, new_text, old_file.filename, new_file.filename)
    return HTMLResponse(content=diff)
