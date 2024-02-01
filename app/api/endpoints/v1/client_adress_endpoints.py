from fastapi import Depends, HTTPException,status, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.schemas.client_adress_schemas import ClientAdressCreate, ClientAdressUpdate
from app.models.client_adress_models import ClientAdress
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from database.conn import async_session
from database import conn


router = APIRouter()


@token_employee_required
@async_session
@router.post("/register-client-adress", responses={
    200: {
        "description": "Endereço do cliente cadastrado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                            "client_id": 1,
                            "employee_id": 1,
                            "adress": "Rua das Ninfas",
                            "number": "04",
                            "city": "Recife",
                            "state": "PE",
                            "name_building": "Jardim Oliveira",
                            "reference_point": "Ao lado do petshop",
                            "complement": "Depois de sair da BR, continue à esquerda"
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def register_client_adress(adress: ClientAdressCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        new_adress = ClientAdress(client_id=adress.client_id, employee_id=adress.employee_id, adress=adress.adress, number=adress.number, cep=adress.cep, city=adress.city, state=adress.state, name_building=adress.name_building, reference_point=adress.reference_point, complement=adress.complement)

        session.add(new_adress)
        await session.commit()

        return {"message":"Endereço do cliente registrado com sucesso"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-client-adresses", status_code=status.HTTP_200_OK)
async def list_client_adresses(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        query = select(ClientAdress)
        result = await session.execute(query)
        client_adress: List[ClientAdressCreate] = result.scalars().all()
        return client_adress
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-client-adress", status_code=status.HTTP_200_OK)
async def get_one_client_adress(client_adress_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    adress_id = await session.execute(select(ClientAdress).where(ClientAdress.id == client_adress_id))
    try: 
        if adress_id:
            obj_adress = adress_id.scalar_one()
            return obj_adress
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    
    
@token_employee_required
@async_session
@router.get("/get-one-client-adress-by-client-id", status_code=status.HTTP_200_OK)
async def get_one_client_adress(client_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    adress_id = await session.execute(select(ClientAdress).where(ClientAdress.client_id == client_id))
    try: 
        if adress_id:
            obj_adress = adress_id.scalar_one()
            return obj_adress
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.put('/update-client-adress/{client_adress_id}', responses={
    200: {
        "description": "Endereço do cliente atualizado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "client_id": 1,
                        "employee_id": 1,
                        "adress": "Rua das Ninfas",
                        "number": "04",
                        "city": "Recife",
                        "state": "PE",
                        "name_building": "Jardim Oliveira",
                        "reference_point": "Ao lado do petshop",
                        "complement": "Depois de sair da BR, continue à esquerda"

                    }

                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_202_ACCEPTED)
async def update_client_adress(client_adress_id: int, clientadress: ClientAdressUpdate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try:
        async with session.begin():
            adress = await session.execute(select(ClientAdress).where(ClientAdress.id == client_adress_id))
            existing_adress = adress.scalars().first()

            if existing_adress:
                if clientadress.employee_id is not None:
                    existing_adress.employee_id = clientadress.employee_id
                else: 
                    existing_adress.employee_id = existing_adress.employee_id

                if clientadress.client_id is not None:
                    existing_adress.client_id = clientadress.client_id
                else: 
                    existing_adress.client_id = existing_adress.client_id

                if clientadress.adress is not None:
                    existing_adress.adress = clientadress.adress
                else: 
                    existing_adress.adress = existing_adress.adress

                if clientadress.number is not None:
                    existing_adress.number = clientadress.number
                else: 
                    existing_adress.number = existing_adress.number

                if clientadress.cep is not None:
                    existing_adress.cep = clientadress.cep
                else:
                    existing_adress.cep = existing_adress.cep
                
                if clientadress.city is not None:
                    existing_adress.city = clientadress.city
                else: 
                    existing_adress.city = existing_adress.city
                
                if clientadress.state is not None:
                    existing_adress.state = clientadress.state
                else: 
                    existing_adress.state = existing_adress.state

                existing_adress.name_building = clientadress.name_building
                existing_adress.reference_point = clientadress.reference_point 
                existing_adress.complement = clientadress.complement

                await session.commit()
                return existing_adress
            else:
                return {"message": "Endereço não encontrado"}
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-client-adress", status_code=status.HTTP_200_OK)
async def delete_client_adress(client_adress_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    adress_id = await session.execute(select(ClientAdress).where(ClientAdress.id == client_adress_id))
    try: 
        if adress_id:
            obj_adress = adress_id.scalar_one()
            await session.delete(obj_adress)
            await session.commit()
            return {"message": "Endereço deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    

