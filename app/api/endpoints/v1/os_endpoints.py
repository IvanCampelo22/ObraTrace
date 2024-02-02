from fastapi import APIRouter, File, UploadFile, Depends, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List

from app.schemas.os_schemas import OsCreate, OsUpdate
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from app.models.os_models import Os
from database import conn
from database.conn import async_session


router = APIRouter()


@token_employee_required
@async_session
@router.post("/register-os", responses={
    200: {
        "description": "Ordem de serviço criada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "employee_id": 1,
                        "client_id": 1,
                        "client_adress_id": 1,
                        "os_type": "Manutenção",
                        "checklist": "lista de equipamentos",
                        "scheduling": '2024-01-01',
                        "end_date": "2024-01-02",
                        "info": "Há três câmeras queimadas, de 16",
                        "solution": "Não há como consertar as câmeras, é necessário a troca",
                        "sale": "O cliente quer 3 câmeras para subtituir e quer expandir para 24 câmeras.",
                        "signature_emplooye": "João Roberto",
                        "signature_client": "John Doe",
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def register_os_(os: OsCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Os).where(Os.client_id == os.client_id, Os.employee_id == os.employee_id, 
                                                                 Os.client_adress_id == os.client_adress_id, Os.os_type == os.os_type, Os.checklist == os.checklist,
                                                                 Os.sale == os.sale, Os.scheduling == os.scheduling, Os.signature_client == os.signature_client,
                                                                 Os.signature_emplooye == os.signature_emplooye, Os.solution == os.solution, Os.info == os.info,
                                                                 Os.end_date == os.end_date))
    existing_os_construction = result.scalar()
    if existing_os_construction: 
        raise HTTPException(status_code=400, detail="Já temos essa ordem de serviço registrada")
    
    try: 
        new_os = Os(client_id=os.client_id, employee_id=os.employee_id, client_adress_id=os.client_adress_id, os_type=os.os_type,
                                              checklist=os.checklist, sale=os.sale, scheduling=os.scheduling, signature_client=os.signature_client,
                                              signature_emplooye=os.signature_emplooye, solution=os.solution, info=os.info, end_date=os.end_date)

        session.add(new_os)
        await session.commit()

        return {"message":"Ordem de serviço para manutenção criada com sucesso"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-os", status_code=status.HTTP_200_OK)
async def list_os(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        query = select(Os).options(joinedload(Os.client)).options(joinedload(Os.client_adress))
        result = await session.execute(query)
        result = result.unique()
        os: List[OsCreate] = result.scalars().all()
        return os
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-os", status_code=status.HTTP_200_OK)
async def get_one_os(dependencies=Depends(JWTBearerEmployee()), os_id: int = None, session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        os = await session.execute(select(Os).where(Os.id == os_id).options(joinedload(Os.client)).options(joinedload(Os.client_adress)))                   
        os = os.unique()

        if os_id:
            obj_construction = os.scalar_one()
            return obj_construction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
    
@token_employee_required
@async_session
@router.put('/update-os/{os_id}', responses={
    200: {
        "description": "Ordem de Serviço atualizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "employee_id": 1,
                        "client_id": 1,
                        "client_adress_id": 1, 
                        "checklist": "lista de equipamentos",
                        "os_type": "Instalação",
                        "scheduling": "2024-01-01",
                        "end_date": "2024-01-12",
                        "info": "instalar duas câmeras",
                        "solution": "As duas câmeras foram instaladas",
                        "sale": "O cliente precisa de um hd maior",
                        "signature_emplooye": "Maria",
                        "signature_client": "João",
                        "update_at": "2024-01-03 10:12:49.17512",
                        "created_at": "2024-01-03 10:12:49.17512",
                        "is_active": True
                    }

                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_202_ACCEPTED)
async def update_os(os_id: int, os_update: OsUpdate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try:
        os = await session.execute(select(Os).where(Os.id == os_id))
        existing_os = os.scalars().first()

        if existing_os:
            if os_update.employee_id is not None:
                existing_os.employee_id = os_update.employee_id
            else: 
                existing_os.employee_id = existing_os.employee_id
        
            if os_update.client_id is not None: 
                existing_os.client_id = os_update.client_id
            else: 
                existing_os.client_id = existing_os.client_id

            if os_update.client_adress_id is not None:
                existing_os.client_adress_id = os_update.client_adress_id
            else: 
                existing_os.client_adress_id = existing_os.client_adress_id

            if os_update.os_type is not None: 
                existing_os.os_type = os_update.os_type
            else:
                existing_os.os_type = existing_os.os_type


            existing_os.checklist = os_update.checklist
            existing_os.scheduling = os_update.scheduling 
            existing_os.end_date = os_update.end_date
            existing_os.solution = os_update.solution
            existing_os.info = os_update.info
            existing_os.sale = os_update.sale
            existing_os.signature_emplooye = os_update.signature_emplooye
            existing_os.signature_client = os_update.signature_client
            existing_os.is_active = os_update.is_active
    
            await session.commit()
            return existing_os
        else:
            return {"message": "Ordem de Serviço não encontrada"}
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-os", status_code=status.HTTP_200_OK)
async def delete_os(os__id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    os_id = await session.execute(select(Os).where(Os.id == os__id))
    try: 
        if os_id:
            obj_os = os_id.scalar_one()
            await session.delete(obj_os)
            await session.commit()
            return {"message": "Ordem de Serviço deletada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@token_employee_required
@async_session
@router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(os_id: int, dependencies=Depends(JWTBearerEmployee()), file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
    os = await session.execute(select(Os).where(Os.id == os_id))
    existing_os = os.scalars().first()
    try:
        file_location = f"/home/ivan/Projects/homelabs/backend-homelabs-app{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        existing_os.image=file_location
        await session.commit()
        
        return existing_os.image

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")