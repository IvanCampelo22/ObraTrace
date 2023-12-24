from fastapi import APIRouter, File, UploadFile, Depends, status
from app.models.os_maintenance_models import OsMaintenance
from sqlalchemy.ext.asyncio import AsyncSession
from database.conn import async_session
from database import conn

from app.schemas.os_maintenance_schemas import OsMaintenanceCreate
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

@router.post("/register-os-maintenance")
async def register_os_maintenance(osmaintenance: OsMaintenanceCreate, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(OsMaintenance).where(OsMaintenance.client_id == osmaintenance.client_id, OsMaintenance.employee_id == osmaintenance.employee_id, 
                                                                 OsMaintenance.client_adress_id == osmaintenance.client_adress_id, OsMaintenance.checklist_auto_id == osmaintenance.checklist_auto_id, 
                                                                 OsMaintenance.checklist_cam_id == osmaintenance.checklist_cam_id, OsMaintenance.checklist_sound_id == osmaintenance.checklist_sound_id, 
                                                                 OsMaintenance.other_checklist_id == osmaintenance.other_checklist_id,
                                                                 OsMaintenance.sale == osmaintenance.sale, OsMaintenance.scheduling == osmaintenance.scheduling, OsMaintenance.signature_client == osmaintenance.signature_client,
                                                                 OsMaintenance.signature_emplooye == osmaintenance.signature_emplooye, OsMaintenance.solution == osmaintenance.solution, OsMaintenance.info == osmaintenance.info,
                                                                 OsMaintenance.end_date == osmaintenance.end_date))
    existing_os_construction = result.scalar()
    if existing_os_construction: 
        raise HTTPException(status_code=400, detail="Já temos essa ordem de serviço registrada")
    
    try: 
        new_os_maintenance = OsMaintenance(client_id=osmaintenance.client_id, employee_id=osmaintenance.employee_id, client_adress_id=osmaintenance.client_adress_id, 
                                              checklist_auto_id=osmaintenance.checklist_auto_id, checklist_cam_id=osmaintenance.checklist_cam_id, checklist_sound_id=osmaintenance.checklist_sound_id,
                                              other_checklist_id=osmaintenance.other_checklist_id, sale=osmaintenance.sale, scheduling=osmaintenance.scheduling, signature_client=osmaintenance.signature_client,
                                              signature_emplooye=osmaintenance.signature_emplooye, solution=osmaintenance.solution, info=osmaintenance.info, end_date=osmaintenance.end_date)

        session.add(new_os_maintenance)
        await session.commit()

        return {"message":"Ordem de serviço para manutenção criada com sucesso"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    
    
@router.get("/list-os-maintenance")
async def list_os_osconstructions(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(OsMaintenance))
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