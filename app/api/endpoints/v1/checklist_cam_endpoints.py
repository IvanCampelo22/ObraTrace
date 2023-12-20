from fastapi import APIRouter, File, UploadFile, Depends, status
from app.models.checklist_cam_models import CheckListCam
from sqlalchemy.ext.asyncio import AsyncSession
from database.conn import async_session
from database import conn

from app.schemas.checlist_cam_schemas import CheckListCamCreate
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
@router.post("/create-checklist-cam")
async def create_checlist_auto(checlistcam: CheckListCamCreate, session: AsyncSession = Depends(conn.get_async_session)):    
    result = await session.execute(select(CheckListCam).where(CheckListCam.rele_type == checlistcam.rele_type, CheckListCam.qtd_rele == checlistcam.qtd_rele, CheckListCam.qtd_cable == checlistcam.qtd_cable, CheckListCam.switch_type == checlistcam.switch_type, CheckListCam.qtd_hub == checlistcam.qtd_hub, CheckListCam.other_equipament == checlistcam.other_equipament))
    existing_checlistcam = result.scalar()
    if existing_checlistcam: 
        return {"message": f"Já temos algo igual no nosso banco de dados {existing_checlistcam.id}"}
    try: 
        new_checlistcam = CheckListCam(employee_id=checlistcam.employee_id, rele_type=checlistcam.rele_type, qtd_rele=checlistcam.qtd_rele, qtd_cable=checlistcam.qtd_cable, switch_type=checlistcam.switch_type, qtd_switch=checlistcam.qtd_switch, qtd_hub=checlistcam.qtd_hub, other_equipament=checlistcam.other_equipament)

        session.add(new_checlistcam)
        await session.commit()

        return {"message":"Checklist para instalação de automação criado com sucesso!"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@router.get("/list-checklist-auto")
async def list_checklist_auto(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(CheckListCam))
        return result.scalar()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')


# @async_session
# @router.post("/uploadfile/", status_code=status.HTTP_200_OK)
# async def create_upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
#     file_location = f"some/directory/{file.filename}"
#     with open(file_location, "wb+") as file_object:
#         file_object.write(file.file.read())
    
#     new_image = CheckListCam(file_budget=file_location)
#     await session.add(new_image)
#     await session.commit()
#     await session.refresh(new_image)
    
#     return {"filename": new_image.file_budget}