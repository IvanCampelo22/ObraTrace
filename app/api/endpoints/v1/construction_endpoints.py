from app.schemas.construction_schemas import ConstructionCreate
from app.models.constructions_models import Constructions
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

@router.post("/register-construction")
async def register_construction(construction: ConstructionCreate, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Constructions).where(Constructions.client_id == construction.client_id, Constructions.employee_id == construction.employee_id, Constructions.client_adress_id == construction.client_adress_id))
    existing_adress = result.scalar()
    if existing_adress: 
        raise HTTPException(status_code=400, detail="Já temos essa obra registrada")
    
    try: 
        new_adress = Constructions(client_id=construction.client_id, employee_id=construction.employee_id, client_adress_id=construction.client_adress_id)

        session.add(new_adress)
        await session.commit()

        return {"message":"Obra registrada com sucesso"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    
    
@router.get("/list-construction")
async def list_constructions(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(Constructions))
        return result.scalar()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')