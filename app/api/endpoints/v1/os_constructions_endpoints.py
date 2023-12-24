from fastapi import APIRouter, File, UploadFile, Depends, status
from app.models.os_constructions_models import OsConstructions
from sqlalchemy.ext.asyncio import AsyncSession
from database.conn import async_session
from database import conn

from app.schemas.os_constructions_schemas import OsConstructionsCreate
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import get_hashed_password, create_access_token,create_refresh_token,verify_password, token_client_required
from fastapi import Depends, HTTPException,status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import conn
from sqlalchemy.future import select
from jose import jwt
from datetime import datetime
from typing import List

router=APIRouter()

@router.post("/register-os-construction")
async def register_os_construction(osconstruction: OsConstructionsCreate, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(OsConstructions).where(OsConstructions.client_id == osconstruction.client_id, OsConstructions.employee_id == osconstruction.employee_id, 
                                                                 OsConstructions.construction_id == osconstruction.construction_id, OsConstructions.checklist_auto_id == osconstruction.checklist_auto_id, 
                                                                 OsConstructions.checklist_cam_id == osconstruction.checklist_cam_id, OsConstructions.checklist_sound_id == osconstruction.checklist_sound_id, 
                                                                 OsConstructions.other_checklist_id == osconstruction.other_checklist_id,
                                                                 OsConstructions.sale == osconstruction.sale, OsConstructions.scheduling == osconstruction.scheduling, OsConstructions.signature_client == osconstruction.signature_client,
                                                                 OsConstructions.signature_emplooye == osconstruction.signature_emplooye, OsConstructions.solution == osconstruction.solution, OsConstructions.info == osconstruction.info,
                                                                 OsConstructions.end_date == osconstruction.end_date))
    existing_os_construction = result.scalar()
    if existing_os_construction: 
        raise HTTPException(status_code=400, detail="Já temos essa ordem de serviço registrada")
    
    try: 
        new_os_construction = OsConstructions(client_id=osconstruction.client_id, employee_id=osconstruction.employee_id, construction_id=osconstruction.construction_id, 
                                              checklist_auto_id=osconstruction.checklist_auto_id, checklist_cam_id=osconstruction.checklist_cam_id, checklist_sound_id=osconstruction.checklist_sound_id,
                                              other_checklist_id=osconstruction.other_checklist_id, sale=osconstruction.sale, scheduling=osconstruction.scheduling, signature_client=osconstruction.signature_client,
                                              signature_emplooye=osconstruction.signature_emplooye, solution=osconstruction.solution, info=osconstruction.info, end_date=osconstruction.end_date)

        session.add(new_os_construction)
        await session.commit()

        return {"message":"Ordem de serviço para obra criada com sucesso"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    
    
@router.get("/list-os-construction")
async def list_os_osconstructions(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(OsConstructions))
        return result.scalar()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')


# @async_session
# @router.post("/uploadfile/", status_code=status.HTTP_200_OK)
# async def create_upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
#     file_location = f"some/directory/{file.filename}"
#     with open(file_location, "wb+") as file_object:
#         file_object.write(file.file.read())
    
#     new_image = OsConstructions(image=file_location)
#     await session.add(new_image)
#     await session.commit()
#     await session.refresh(new_image)
    
#     return {"filename": new_image.image}