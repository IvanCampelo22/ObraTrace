from fastapi import APIRouter, File, UploadFile, Depends, status, HTTPException

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from app.schemas.os_constructions_schemas import OsConstructionsCreate, OsConstructionsUpdate
from app.models.os_constructions_models import OsConstructions
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from database import conn
from database.conn import async_session


router = APIRouter()


@token_employee_required
@async_session
@router.post("/register-os-construction", responses={
    200: {
        "description": "Ordem de Serviço para obra criada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "checklist": "Lista de equipamentos",
                        "scheduling": "2024-01-01", 
                        "end_date": "2024-01-02",
                        "info": "Instalação de caixas de som, de câmeras e de automação",
                        "sale": "O cliente precisa de uma câmera a mais no lado oeste da casa",
                        "signature_emplooye": "Jorge Mazarate",
                        "signature_client": "John Done"
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def register_os_construction(osconstruction: OsConstructionsCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(OsConstructions).where(OsConstructions.client_id == osconstruction.client_id, OsConstructions.employee_id == osconstruction.employee_id, 
                                                                 OsConstructions.construction_id == osconstruction.construction_id, OsConstructions.checklist == osconstruction.checklist,
                                                                 OsConstructions.sale == osconstruction.sale, OsConstructions.scheduling == osconstruction.scheduling, OsConstructions.signature_client == osconstruction.signature_client,
                                                                 OsConstructions.signature_emplooye == osconstruction.signature_emplooye, OsConstructions.info == osconstruction.info,
                                                                 OsConstructions.end_date == osconstruction.end_date))
    existing_os_construction = result.scalar()
    if existing_os_construction: 
        raise HTTPException(status_code=400, detail="Já temos essa ordem de serviço registrada")
    
    try: 
        new_os_construction = OsConstructions(client_id=osconstruction.client_id, employee_id=osconstruction.employee_id, construction_id=osconstruction.construction_id, 
                                              checklist=osconstruction.checklist,
                                              sale=osconstruction.sale, scheduling=osconstruction.scheduling, signature_client=osconstruction.signature_client,
                                              signature_emplooye=osconstruction.signature_emplooye, info=osconstruction.info, end_date=osconstruction.end_date)

        session.add(new_os_construction)
        await session.commit()

        return {"message":"Ordem de serviço para obra criada com sucesso"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-os-construction")
async def list_os_osconstructions(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        query = select(OsConstructions)
        result = await session.execute(query)
        osconstruction: List[OsConstructionsCreate] = result.scalars().all()
        return osconstruction
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-os-constructions", status_code=status.HTTP_200_OK)
async def get_one_os_constructions(dependencies=Depends(JWTBearerEmployee()), os_construction_id: int = None, session: AsyncSession = Depends(conn.get_async_session)):
    os_constructions_id = await session.execute(select(OsConstructions).where(OsConstructions.id == os_construction_id))
    try: 
        if os_constructions_id:
            obj_os_construction = os_constructions_id.scalar_one()
            return obj_os_construction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
    
@token_employee_required
@async_session
@router.put('/update-os-constructions/{os_constructions_id}', responses={
    200: {
        "description": "Ordem de Serviço para obra atualizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "employee_id": 1,
                        "client_id": 1,
                        "client_adress_id": 1, 
                        "checklist": "teste",
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
async def update_os_construction(os_construction_id: int, os_construction_update: OsConstructionsUpdate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try:
        os = await session.execute(select(OsConstructions).where(OsConstructions.id == os_construction_id))
        existing_os = os.scalars().first()

        if existing_os:
            if os_construction_update.employee_id is not None:
                existing_os.employee_id = os_construction_update.employee_id
            else: 
                existing_os.employee_id = existing_os.employee_id
        
            if os_construction_update.client_id is not None: 
                existing_os.client_id = os_construction_update.client_id
            else: 
                existing_os.client_id = existing_os.client_id

            if os_construction_update.construction_id is not None:
                existing_os.construction_id = os_construction_update.construction_id
            else: 
                existing_os.construction_id = existing_os.construction_id


            existing_os.checklist = os_construction_update.checklist
            existing_os.scheduling = os_construction_update.scheduling 
            existing_os.end_date = os_construction_update.end_date
            existing_os.info = os_construction_update.info
            existing_os.sale = os_construction_update.sale
            existing_os.signature_emplooye = os_construction_update.signature_emplooye
            existing_os.signature_client = os_construction_update.signature_client
    
            await session.commit()
            return existing_os
        else:
            return {"message": "Ordem de Serviço para obra não encontrada"}
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-os-constructions", status_code=status.HTTP_200_OK)
async def delete_os_constructions(os_constructions_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    constructions_id = await session.execute(select(OsConstructions).where(OsConstructions.id == os_constructions_id))
    try: 
        if constructions_id:
            obj_os_constructions = constructions_id.scalar_one()
            await session.delete(obj_os_constructions)
            await session.commit()
            return {"message": "Ordem de Serviço deletada com sucesso"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")


@token_employee_required
@async_session
@router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(osconstruction_id: int, dependencies=Depends(JWTBearerEmployee()), file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
    os = await session.execute(select(OsConstructions).where(OsConstructions.id == osconstruction_id))
    existing_os = os.scalars().first()
    try:
        file_location = f"/home/ivan/Projects/homelabs/backend-homelabs-app{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())

        existing_os.image = file_location
        await session.commit()
        
        return existing_os.image

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")