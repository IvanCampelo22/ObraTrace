from app.schemas.construction_schemas import ConstructionCreate
from app.models.constructions_models import Constructions
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import get_hashed_password, create_access_token,create_refresh_token,verify_password, token_client_required, token_employee_required
from fastapi import Depends, HTTPException,status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import conn
from database.conn import async_session
from sqlalchemy.future import select
from jose import jwt
from datetime import datetime
from typing import List

router=APIRouter()


@token_employee_required
@async_session
@router.post("/register-construction", status_code=status.HTTP_201_CREATED)
async def register_construction(construction: ConstructionCreate, dependencies=Depends(JWTBearer()), session: AsyncSession = Depends(conn.get_async_session)):
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
    

@token_employee_required
@async_session
@router.get("/list-construction", status_code=status.HTTP_200_OK)
async def list_constructions(dependencies=Depends(JWTBearer()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        result = await session.execute(select(Constructions))
        return result.scalar()
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-construction", status_code=status.HTTP_200_OK)
async def get_one_checklist(construction_id: int = None, dependencies=Depends(JWTBearer()), session: AsyncSession = Depends(conn.get_async_session)):
    maintenance_id = await session.execute(select(Constructions).where(Constructions.id == construction_id))
    try: 
        if maintenance_id:
            obj_construction = maintenance_id.scalar_one()
            return obj_construction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-construction", status_code=status.HTTP_200_OK)
async def delete_construction(construction_id: int = None, dependencies=Depends(JWTBearer()), session: AsyncSession = Depends(conn.get_async_session)):
    construction = await session.execute(select(Constructions).where(Constructions.id == construction_id))
    try: 
        if construction:
            obj_construction = construction.scalar_one()
            await session.delete(obj_construction)
            await session.commit()
            return {"message": "Obra deletada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")