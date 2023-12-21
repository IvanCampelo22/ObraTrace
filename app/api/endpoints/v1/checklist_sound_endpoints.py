from fastapi import APIRouter, File, UploadFile, Depends, status
from app.models.checklist_sound_models import CheckListSound
from sqlalchemy.ext.asyncio import AsyncSession
from database.conn import async_session
from database import conn

from app.schemas.checlist_sound_schemas import CheckListSoundCreate
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import get_hashed_password, create_access_token,create_refresh_token,verify_password, token_client_required
from fastapi import Depends, HTTPException,status, APIRouter, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from database import conn
from sqlalchemy.future import select
from jose import jwt
from datetime import datetime

router=APIRouter()

@async_session
@router.post("/create-checklist-sound")
async def create_checlist_sound(checlistsound: CheckListSoundCreate, session: AsyncSession = Depends(conn.get_async_session)):    

    result = await session.execute(select(CheckListSound).where(CheckListSound.qtd_sound_box == checlistsound.qtd_sound_box, CheckListSound.qtd_cable == checlistsound.qtd_cable, CheckListSound.qtd_conn == checlistsound.qtd_conn, CheckListSound.qtd_ampli == checlistsound.qtd_ampli, CheckListSound.qtd_receiver == checlistsound.qtd_receiver,  CheckListSound.other_equipament == checlistsound.other_equipament))
    existing_checlistsound = result.scalar()
    if existing_checlistsound: 
        return {"message": f"Já temos algo igual no nosso banco de dados {existing_checlistsound.id}"}
    try: 
        new_checlistsound = CheckListSound(employee_id=checlistsound.employee_id, qtd_sound_box=checlistsound.qtd_sound_box, qtd_cable=checlistsound.qtd_cable, qtd_conn=checlistsound.qtd_conn, qtd_ampli=checlistsound.qtd_ampli, qtd_receiver=checlistsound.qtd_receiver, other_equipament=checlistsound.other_equipament)

        session.add(new_checlistsound)
        await session.commit()
        await session.refresh()

        return {"message":"Checklist para instalação de som criado com sucesso!"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@async_session
@router.get("/list-checklist-sound")
async def list_checklist_sound(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(CheckListSound))
        return result.scalar()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')


# @async_session
# @router.post("/uploadfile/", status_code=status.HTTP_200_OK)
# async def create_upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
#     file_location = f"/home/ivan/Downloads/{file.filename}"
#     with open(file_location, "wb+") as file_object:
#         file_object.write(file.file.read())
    
#     new_image = CheckListSound(file_budget=file_location)
#     session.add(new_image)
#     await session.commit()
#     await session.refresh(new_image)
    
#     return {"filename": new_image.file_budget}