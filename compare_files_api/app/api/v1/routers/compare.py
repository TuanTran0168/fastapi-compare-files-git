from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud import file as crud
from app.db.session import get_db
from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.diff_utils import git_like_diff
from starlette.responses import HTMLResponse

router = APIRouter()


@router.get("/{new_file_id}/{old_file_id}")
def compare_files(new_file_id: int, old_file_id: int, db: Session = Depends(get_db)):
    new_file = crud.get_file(db, new_file_id)
    old_file = crud.get_file(db, old_file_id)

    if not new_file or not old_file:
        raise HTTPException(status_code=404, detail="File not found")

    if new_file.filetype == "pdf":
        new_text = extract_text_from_pdf(new_file.content)
    else:
        new_text = new_file.content.decode("utf-8")

    if old_file.filetype == "pdf":
        old_text = extract_text_from_pdf(old_file.content)
    else:
        old_text = old_file.content.decode("utf-8")

    diff_html = git_like_diff(old_file, new_file, old_text, new_text)
    return HTMLResponse(status_code=200, content=diff_html)
