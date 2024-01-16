from fastapi import Depends, HTTPException,status, APIRouter, UploadFile, File

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.schemas.checlist_auto_schemas import CheckListAutoCreate, CheckListAutoUpdate
from app.models.checklist_auto_models import CheckListAuto
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from sqlalchemy.ext.asyncio import AsyncSession
from database import conn
from database.conn import async_session


router = APIRouter()


@token_employee_required
@async_session
@router.post("/create-checklist-auto", responses={
    200: {
        "description": "Checklist para automação criado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                            "employee_id": 1,
                            "rele_type": "duas sessões, trẽs sessões", 
                            "qtd_rele": 2,
                            "qtd_cable": 1,
                            "switch_type": "5 sessões",
                            "qtd_switch": 1,
                            "qtd_hub": 1, 
                            "other_equipament": "rele multiuso"
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def create_checlist_auto(checlistauto: CheckListAutoCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):    
    try: 
        async with session.begin():
            result = await session.execute(select(CheckListAuto).where(CheckListAuto.rele_type == checlistauto.rele_type, CheckListAuto.qtd_rele == checlistauto.qtd_rele, CheckListAuto.qtd_cable == checlistauto.qtd_cable, CheckListAuto.switch_type == checlistauto.switch_type, CheckListAuto.qtd_hub == checlistauto.qtd_hub, CheckListAuto.other_equipament == checlistauto.other_equipament))
            existing_checlistauto = result.scalar()
             
            if existing_checlistauto: 
                return {"message": f"Já temos algo igual no nosso banco de dados {existing_checlistauto.id}"}
            new_checlistauto = CheckListAuto(employee_id=checlistauto.employee_id, rele_type=checlistauto.rele_type, qtd_rele=checlistauto.qtd_rele, qtd_cable=checlistauto.qtd_cable, switch_type=checlistauto.switch_type, qtd_switch=checlistauto.qtd_switch, qtd_hub=checlistauto.qtd_hub, other_equipament=checlistauto.other_equipament)

            session.add(new_checlistauto)
            await session.commit()

            return new_checlistauto
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    
    
@token_employee_required
@async_session
@router.get("/list-checklist-auto", responses={
    200: {
        "description": "Lista de checklist de automação",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "client_id": 1,
                        "adress": "Rua Do Futuro",
                        "number": "04",
                        "state": "PE",
                        "reference_point": "Ao Lado do Pet Shop",
                        "updated_at": "2023-12-15T19:28:23.043687",
                        "id": 1,
                        "employee_id": 7,
                        "city": "Recife",
                        "name_building": "Oscar Duval",
                        "complement": "Prédio Preto",
                        "created_at": "2023-12-15T19:28:23.043765"
  
                    },

                    {   
                        "client_id": 2,
                        "adress": "Rua Maria Bonita",
                        "number": "05",
                        "state": "PE",
                        "reference_point": "Ao Lado da Praia",
                        "updated_at": "2023-12-15T19:28:23.043687",
                        "id": 2,
                        "employee_id": 7,
                        "city": "Recife",
                        "name_building": "Josuita Santos",
                        "complement": "Prédio Azul",
                        "created_at": "2023-12-15T19:28:23.043765"
  
                    }

                ]
            }
        },
        404: {"description": "Não foi possível recuperar checklists de automação"}
}}, status_code=status.HTTP_200_OK)
async def list_checklist_auto(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        async with session.begin():
            query = select(CheckListAuto)
            result = await session.execute(query)
            checklist_auto: List[CheckListAutoCreate] = result.scalars().all()
            return checklist_auto
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-checklist-auto", responses={
    200: {
        "description": "Lista de checklist de automação",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "client_id": 1,
                        "adress": "Rua Do Futuro",
                        "number": "04",
                        "state": "PE",
                        "reference_point": "Ao Lado do Pet Shop",
                        "updated_at": "2023-12-15T19:28:23.043687",
                        "id": 1,
                        "employee_id": 7,
                        "city": "Recife",
                        "name_building": "Oscar Duval",
                        "complement": "Prédio Preto",
                        "created_at": "2023-12-15T19:28:23.043765"
  
                    }

                ]
            }
        },
        404: {"description": "Não foi possível recuperar checklist de automação"}
}}, status_code=status.HTTP_200_OK)
async def get_one_checklist_auto(checklist_auto_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(CheckListAuto).where(CheckListAuto.id == checklist_auto_id))
    try: 
        async with session.begin():
            if checklist_id:
                obj_checklist = checklist_id.scalar_one()
                return obj_checklist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
    
@token_employee_required
@async_session
@router.put('/update-checklist-auto/{checklist_auto_id}', responses={
    200: {
        "description": "Checklist de automação atualizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "client_id": 1,
                        "adress": "Rua Do Futuro",
                        "number": "04",
                        "state": "PE",
                        "reference_point": "Ao Lado do Pet Shop",
                        "updated_at": "2023-12-15T19:28:23.043687",
                        "id": 1,
                        "employee_id": 7,
                        "city": "Recife",
                        "name_building": "Oscar Duval",
                        "complement": "Prédio Preto",
                        "created_at": "2023-12-15T19:28:23.043765"
  
                    }

                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_202_ACCEPTED)
async def update_checklist_auto(checklist_auto_id: int, checklistauto: CheckListAutoUpdate, session: AsyncSession = Depends(conn.get_async_session)):
    try:
        async with session.begin():
            checklist = await session.execute(select(CheckListAuto).where(CheckListAuto.id == checklist_auto_id))
            existing_checklist = checklist.scalars().first()

            if existing_checklist:
                if checklistauto.employee_id is not None:
                    existing_checklist.employee_id = checklistauto.employee_id
                else: 
                    existing_checklist.employee_id = existing_checklist.employee_id

                existing_checklist.rele_type = checklistauto.rele_type
                existing_checklist.qtd_rele = checklistauto.qtd_rele
                existing_checklist.qtd_cable = checklistauto.qtd_cable
                existing_checklist.switch_type = checklistauto.switch_type
                existing_checklist.qtd_switch = checklistauto.qtd_switch
                existing_checklist.qtd_hub = checklistauto.qtd_hub
                existing_checklist.other_equipament = checklistauto.other_equipament
    
                await session.commit()
                return existing_checklist
            else:
                return {"message": "Checklist não encontrado"}
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-checklist-auto", responses={
    200: {
        "description": "Lista de checklist de automação",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "message": "Checklist deletado com sucesso"
                    }

                ]
            }
        },
        404: {"description": "Não foi possível deletar checklist de automação"}
}}, status_code=status.HTTP_200_OK)
async def delete_checklist_auto(checklist_auto_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(CheckListAuto).where(CheckListAuto.id == checklist_auto_id))
    try: 
        async with session.begin():
            if checklist_id:
                obj_checklist = checklist_id.scalar_one()
                await session.delete(obj_checklist)
                await session.commit()
                return {"message": "Checklist de automação deletado com sucesso"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    
    
@token_employee_required
@async_session
@router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(checklist_id: int, file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
    checklist = await session.execute(select(CheckListAuto).where(CheckListAuto.id == checklist_id))
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