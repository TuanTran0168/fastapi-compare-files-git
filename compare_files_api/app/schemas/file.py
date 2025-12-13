from pydantic import BaseModel

class FileResponse(BaseModel):
    id: int
    filename: str
    filetype: str

    class Config:
        from_attributes = True
