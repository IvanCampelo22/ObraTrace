from app.models.checklist_auto_models import CheckListAuto
from sqlalchemy.ext.asyncio import AsyncSession
from database.conn import async_session


from app.schemas.checlist_auto_schemas import CheckListAutoCreate
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
@router.post("/create-checklist-auto")
async def create_checlist_auto(checlistauto: CheckListAutoCreate, session: AsyncSession = Depends(conn.get_async_session)):    
    result = await session.execute(select(CheckListAuto).where(CheckListAuto.rele_type == checlistauto.rele_type, CheckListAuto.qtd_rele == checlistauto.qtd_rele, CheckListAuto.qtd_cable == checlistauto.qtd_cable, CheckListAuto.switch_type == checlistauto.switch_type, CheckListAuto.qtd_hub == checlistauto.qtd_hub, CheckListAuto.other_equipament == checlistauto.other_equipament))
    existing_checlistauto = result.scalar()
    if existing_checlistauto: 
        return {"message": f"Já temos algo igual no nosso banco de dados {existing_checlistauto.id}"}
    try: 
        new_checlistauto = CheckListAuto(employee_id=checlistauto.employee_id, rele_type=checlistauto.rele_type, qtd_rele=checlistauto.qtd_rele, qtd_cable=checlistauto.qtd_cable, switch_type=checlistauto.switch_type, qtd_switch=checlistauto.qtd_switch, qtd_hub=checlistauto.qtd_hub, other_equipament=checlistauto.other_equipament)

        session.add(new_checlistauto)
        await session.commit()

        return {"message":"Checklist para instalação de automação criado com sucesso!"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@router.get("/list-checklist-auto")
async def list_checklist_auto(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(CheckListAuto))
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
    
#     new_image = CheckListAuto(file_budget=file_location)
#     await session.add(new_image)
#     await session.commit()
#     await session.refresh(new_image)
    
#     return {"filename": new_image.file_budget}