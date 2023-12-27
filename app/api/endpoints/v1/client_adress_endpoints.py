from fastapi import Depends, HTTPException,status, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.schemas.client_adress_schemas import ClientAdressCreate
from app.models.client_adress_models import ClientAdress
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from database.conn import async_session
from database import conn


router=APIRouter()


@token_employee_required
@async_session
@router.post("/register-client-adress", status_code=status.HTTP_201_CREATED)
async def register_client_adress(adress: ClientAdressCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(ClientAdress).where(ClientAdress.adress == adress.adress, ClientAdress.city == adress.city, ClientAdress.number == adress.number, ClientAdress.state == adress.state, ClientAdress.name_building == adress.name_building, ClientAdress.reference_point == adress.reference_point, ClientAdress.complement == adress.complement))
    existing_adress = result.scalar()
    if existing_adress: 
        raise HTTPException(status_code=400, detail="Já temos esse endereço registrado")
    
    try: 
        new_adress = ClientAdress(client_id=adress.client_id, employee_id=adress.employee_id, adress=adress.adress, number=adress.number, city=adress.city, state=adress.state, name_building=adress.name_building, reference_point=adress.reference_point, complement=adress.complement)

        session.add(new_adress)
        await session.commit()

        return {"message":"Endereço do cliente registrado com sucesso"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-client-adresses", status_code=status.HTTP_200_OK)
async def list_client_adresses(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        obj = await session.execute(select(ClientAdress))
        return obj.scalar()
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
@router.delete("/delete-client-adress", status_code=status.HTTP_200_OK)
async def delete_client_adress(construction_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    adress_id = await session.execute(select(ClientAdress).where(ClientAdress.id == construction_id))
    try: 
        if adress_id:
            obj_adress = adress_id.scalar_one()
            await session.delete(obj_adress)
            await session.commit()
            return {"message": "Endereço deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    

# @router.put('update-client-adress{adress_id}')
# async def update_client_adress(adress_id: int = None, session: AsyncSession = Depends(conn.get_async_session)):
#     result = await session.execute(select(ClientAdress).filter_by(ClientAdress.id))
#     return result
