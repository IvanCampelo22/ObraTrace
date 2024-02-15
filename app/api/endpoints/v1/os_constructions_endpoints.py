from fastapi import APIRouter, File, UploadFile, Depends, status, HTTPException

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound

from typing import List


from app.schemas.os_constructions_schemas import OsConstructionsCreate, OsConstructionsUpdate
from app.models.os_constructions_models import OsConstructions
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from database import conn
import os
import threading
from database.conn import async_session
from supabase import Client, create_client

url: str = os.environ.get('SUPABASE_URL')
key: str = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(url, key)



router = APIRouter()


@token_employee_required
@async_session
@router.post("/register-os-construction", responses={
    201: {
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
        400: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def register_os_construction(osconstruction: OsConstructionsCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try:
        result = await session.execute(select(OsConstructions).where(OsConstructions.client_id == osconstruction.client_id, OsConstructions.employee_id == osconstruction.employee_id, 
                                                                    OsConstructions.construction_id == osconstruction.construction_id, OsConstructions.checklist == osconstruction.checklist,
                                                                    OsConstructions.sale == osconstruction.sale, OsConstructions.scheduling == osconstruction.scheduling, OsConstructions.signature_client == osconstruction.signature_client,
                                                                    OsConstructions.signature_emplooye == osconstruction.signature_emplooye, OsConstructions.info == osconstruction.info,
                                                                    OsConstructions.end_date == osconstruction.end_date))
        existing_os_construction = result.scalar()
        
        if existing_os_construction: 
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já temos essa ordem de serviço registrada")
        
        
        new_os_construction = OsConstructions(client_id=osconstruction.client_id, employee_id=osconstruction.employee_id, construction_id=osconstruction.construction_id, 
                                                checklist=osconstruction.checklist,
                                                sale=osconstruction.sale, scheduling=osconstruction.scheduling, signature_client=osconstruction.signature_client,
                                                signature_emplooye=osconstruction.signature_emplooye, info=osconstruction.info, end_date=osconstruction.end_date)


        if not new_os_construction.client_id or not new_os_construction.construction_id or not new_os_construction.employee_id: 
            await session.rollback()
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insira dados válidos")


        session.add(new_os_construction)
        await session.commit()

        return {"message":"Ordem de serviço para obra criada com sucesso"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
    

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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-os-constructions", status_code=status.HTTP_200_OK)
async def get_one_os_constructions(dependencies=Depends(JWTBearerEmployee()), os_construction_id: int = None, session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        os_constructions_id = await session.execute(select(OsConstructions).where(OsConstructions.id == os_construction_id))

        obj_os_construction = os_constructions_id.scalar_one()
        return obj_os_construction
    
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Ordem de Serviço não encontrada'})
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    
    
@token_employee_required
@async_session
@router.put('/update-os-constructions/{os_constructions_id}', responses={
    201: {
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
        404: {"description": "Não foi possível encontrar ordem de serviço"}
}}, status_code=status.HTTP_202_ACCEPTED)
async def update_os_construction(os_construction_id: int, os_construction_update: OsConstructionsUpdate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try:

        os = await session.execute(select(OsConstructions).where(OsConstructions.id == os_construction_id))
        existing_os = os.scalars().first()

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

        if not existing_os.client_id or not existing_os.construction_id or not existing_os.employee_id: 
            await session.rollback()
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insira dados válidos")

        await session.commit()
        return existing_os
    
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Ordem de Serviço não encontrada'})
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-os-constructions", status_code=status.HTTP_200_OK)
async def delete_os_constructions(os_constructions_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        constructions_id = await session.execute(select(OsConstructions).where(OsConstructions.id == os_constructions_id))
        
        obj_os_constructions = constructions_id.scalar_one()
        await session.delete(obj_os_constructions)
        await session.commit()
        return {"message": "Ordem de Serviço deletada com sucesso"}
    
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Ordem de Serviço não encontrada'})
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")


@token_employee_required
@async_session
@router.post("/uploadfile/", status_code=status.HTTP_201_CREATED)
async def create_upload_file(os_id: int, file: UploadFile, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try:
        os = await session.execute(select(OsConstructions).where(OsConstructions.id == os_id))
        existing_os = os.scalars().first()

        file_path = await file.read()

        def upload():
            supabase.storage.from_('files').upload(file=file_path, path=file.filename, file_options={"content-type": "image/png"})
        
        thread = threading.Thread(target=upload)
        thread.start()
        thread.join(3)
        
        file_url = supabase.storage.from_('files').get_public_url(file.filename)

        existing_os.image = file_url
        await session.commit()

        return {'message': 'upload de imagem realizado com sucesso'}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    