from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException,status, APIRouter, UploadFile, File
from sqlalchemy.future import select

from app.models.other_checklist_models import OtherCheckList
from app.schemas.other_checklist_schemas import OtherCheckListCreate
from database.conn import async_session
from database import conn
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle_employee import token_employee_required


router = APIRouter()


@token_employee_required
@async_session
@router.post("/create-other-checklist", status_code=status.HTTP_201_CREATED)
async def create_other_checklist(otherchecklist: OtherCheckListCreate, 
                                 dependencies=Depends(JWTBearerEmployee()), 
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
async def list_other_checklist(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(OtherCheckList))
        return result.scalar()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-other-checklist", status_code=status.HTTP_200_OK)
async def get_one_other_checklist(other_checklist_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
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
async def delete_other_checklist(other_checklist_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
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