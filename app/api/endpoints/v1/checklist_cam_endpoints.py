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
async def create_checlist_cam(checlistcam: CheckListCamCreate, session: AsyncSession = Depends(conn.get_async_session)):    
    result = await session.execute(select(CheckListCam).where(CheckListCam.qtd_cam == checlistcam.qtd_cam, CheckListCam.qtd_box_cable == checlistcam.qtd_box_cable, CheckListCam.qtd_rca == checlistcam.qtd_rca, CheckListCam.qtd_p4 == checlistcam.qtd_p4, CheckListCam.qtd_dvr == checlistcam.qtd_dvr, CheckListCam.qtd_hd == checlistcam.qtd_hd, CheckListCam.hds_size == checlistcam.hds_size, CheckListCam.other_equipament == checlistcam.other_equipament))
    existing_checlistcam = result.scalar()
    if existing_checlistcam: 
        return {"message": f"Já temos algo igual no nosso banco de dados {existing_checlistcam.id}"}
    try: 
        new_checlistcam = CheckListCam(employee_id=checlistcam.employee_id, qtd_cam=checlistcam.qtd_cam, qtd_box_cable=checlistcam.qtd_box_cable, qtd_rca=checlistcam.qtd_rca, qtd_p4=checlistcam.qtd_p4, qtd_dvr=checlistcam.qtd_dvr, qtd_hd=checlistcam.qtd_hd, hds_size=checlistcam.hds_size, other_equipament=checlistcam.other_equipament)

        session.add(new_checlistcam)
        await session.commit()

        return {"message":"Checklist para instalação de câmeras criado com sucesso!"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@async_session
@router.get("/list-checklist-auto")
async def list_checklist_cam(session: AsyncSession = Depends(conn.get_async_session)):
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