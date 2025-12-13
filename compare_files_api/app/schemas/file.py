from pydantic import BaseModel

class FileResponse(BaseModel):
    id: int
    filename: str

    class Config:
        orm_mode = True
