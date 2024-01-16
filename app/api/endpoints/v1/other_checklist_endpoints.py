from fastapi import Depends, HTTPException,status, APIRouter, UploadFile, File

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.models.other_checklist_models import OtherCheckList
from app.schemas.other_checklist_schemas import OtherCheckListCreate, OtherCheckListUpdate
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from database.conn import async_session
from database import conn


router = APIRouter()


@token_employee_required
@async_session
@router.post("/create-other-checklist", responses={
    200: {
        "description": "Checklist criada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "employee_id": 1,
                        "equipment": "Uma caixa de cabo UTP, um switch de 8 portas, e 12 conectores RJ"
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}},  status_code=status.HTTP_201_CREATED)
async def create_other_checklist(otherchecklist: OtherCheckListCreate, 
                                 dependencies=Depends(JWTBearerEmployee()), 
                                 session: AsyncSession = Depends(conn.get_async_session)):    
    try: 
        async with session.begin():
            result = await session.execute(select(OtherCheckList).where(OtherCheckList.equipment == otherchecklist.equipment))
            existing_otherchecklist = result.scalar()

            if existing_otherchecklist: 
                return {"message": f"Já temos algo igual no nosso banco de dados {existing_otherchecklist.id}"}
            
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
        async with session.begin():
            query = select(OtherCheckList)
            result = await session.execute(query)
            otherchecklist: List[OtherCheckListCreate] = result.scalars().all()
            return otherchecklist
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-other-checklist", status_code=status.HTTP_200_OK)
async def get_one_other_checklist(other_checklist_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(OtherCheckList).where(OtherCheckList.id == other_checklist_id))
    try: 
        async with session.begin():
            if checklist_id:
                obj_os_construction = checklist_id.scalar_one()
                return obj_os_construction
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    
    
@token_employee_required
@async_session
@router.put('/update-other-checklist/{other_checklist_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_construction(other_checklist_id: int, other_checklist: OtherCheckListUpdate, session: AsyncSession = Depends(conn.get_async_session)):
    try:

        async with session.begin():
            checklist = await session.execute(select(OtherCheckList).where(OtherCheckList.id == other_checklist_id))
            existing_checklist = checklist.scalars().first()

            if existing_checklist:
                if other_checklist.employee_id is not None:
                    existing_checklist.employee_id = other_checklist.employee_id
                else: 
                    existing_checklist.employee_id = existing_checklist.employee_id
                existing_checklist.equipment = other_checklist.equipment

                await session.commit()
                return existing_checklist
            else:
                return {"message": "Obra não encontrada"}
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-other-checklist", status_code=status.HTTP_200_OK)
async def delete_other_checklist(other_checklist_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(OtherCheckList).where(OtherCheckList.id == other_checklist_id))
    try: 
        async with session.begin():
            if checklist_id:
                obj_other_checklist = checklist_id.scalar_one()
                await session.delete(obj_other_checklist)
                await session.commit()
                return {"message": "checklist deletada com sucesso"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@token_employee_required
@async_session
@router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(checklist_id: int, file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
    checklist = await session.execute(select(OtherCheckList).where(OtherCheckList.id == checklist_id))
    existing_checklist = checklist.scalars().first()
    try:
        file_location = f"/home/ivan/Projects/homelabs/backend-homelabs-app{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        existing_checklist.file_budget=file_location

        await session.commit()
        
        return existing_checklist.file_budget

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")