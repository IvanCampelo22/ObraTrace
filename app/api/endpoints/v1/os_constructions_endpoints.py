from fastapi import APIRouter, File, UploadFile, Depends
from app.models.os_constructions_models import ConstructionsOs
from sqlalchemy.ext.asyncio import AsyncSession
from database.conn import async_session
from database import conn

router = APIRouter

@async_session
@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
    file_location = f"some/directory/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    new_image = ConstructionsOs(file_path=file_location)
    await session.add(new_image)
    await session.commit()
    await session.refresh(new_image)
    
    return {"filename": new_image.image}