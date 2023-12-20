from app.schemas.client_adress_schemas import ClientAdressCreate
from app.models.client_adress_models import ClientAdress
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import get_hashed_password, create_access_token,create_refresh_token,verify_password, token_client_required
from fastapi import Depends, HTTPException,status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import conn
from sqlalchemy.future import select
from jose import jwt
from datetime import datetime
from typing import List

router=APIRouter()

@router.post("/register-client-adress")
async def register_user(adress: ClientAdressCreate, session: AsyncSession = Depends(conn.get_async_session)):
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
    
    
@router.get("/list-client-adresses")
async def list_client_adresses(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(ClientAdress))
        return result.scalar()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
                    
