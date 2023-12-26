from app.models.other_checklist_models import OtherCheckList
from sqlalchemy.ext.asyncio import AsyncSession
from database.conn import async_session


from app.schemas.other_checklist_schemas import OtherCheckListCreate, OtherCheckListSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import get_hashed_password, create_access_token,create_refresh_token,verify_password, token_client_required, token_employee_required
from fastapi import Depends, HTTPException,status, APIRouter, UploadFile, File, Response
from sqlalchemy.ext.asyncio import AsyncSession
from database import conn
from sqlalchemy.future import select
from jose import jwt
from datetime import datetime

router=APIRouter()


@token_employee_required
@async_session
@router.post("/create-other-checklist", status_code=status.HTTP_201_CREATED)
async def create_other_checklist(otherchecklist: OtherCheckListCreate, 
                                 dependencies=Depends(JWTBearer()), 
                                 session: AsyncSession = Depends(conn.get_async_session)):    
    result = await session.execute(select(OtherCheckList).where(OtherCheckList.equipment == otherchecklist.equipment))
    existing_otherchecklist = result.scalar()
    if existing_otherchecklist: 
        return {"message": f"Já temos algo igual no nosso banco de dados {existing_otherchecklist.id}"}
    try: 
        new_otherchecklist = OtherCheckList(employee_id=otherchecklist.employee_id, equipment=otherchecklist.equipment)

        session.add(new_otherchecklist)
        await session.commit()

        return {"message":"Checklist para instalação criado com sucesso!"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-other-checklist", status_code=status.HTTP_200_OK)
async def list_other_checklist(dependencies=Depends(JWTBearer()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(OtherCheckList))
        return result.scalar()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-other-checklist", status_code=status.HTTP_200_OK)
async def get_one_other_checklist(other_checklist_id: int = None, dependencies=Depends(JWTBearer()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(OtherCheckList).where(OtherCheckList.id == other_checklist_id))
    try: 
        if checklist_id:
            obj_os_construction = checklist_id.scalar_one()
            return obj_os_construction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-other-checklist", status_code=status.HTTP_200_OK)
async def delete_other_checklist(other_checklist_id: int = None, dependencies=Depends(JWTBearer()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(OtherCheckList).where(OtherCheckList.id == other_checklist_id))
    try: 
        if checklist_id:
            obj_other_checklist = checklist_id.scalar_one()
            await session.delete(obj_other_checklist)
            await session.commit()
            return {"message": "checklist deletada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@async_session
@router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
    file_location = f"/home/ivan/Projects/homelabs/backend-homelabs-app/{file.filename}"
    result = await session.execute(select(OtherCheckList))
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    
    new_image = OtherCheckList(file_budget=file_location)
    session.add(new_image)
    await session.commit()
    await session.refresh(new_image)
    
    return {"filename": new_image.file_budget}