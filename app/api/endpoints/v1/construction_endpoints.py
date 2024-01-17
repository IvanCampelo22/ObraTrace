from fastapi import Depends, HTTPException,status, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List

from app.schemas.construction_schemas import ConstructionCreate, ConstructionSchema, ConstructionUpdate
from app.models.constructions_models import Constructions
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from database import conn
from database.conn import async_session


router = APIRouter()


@token_employee_required
@async_session
@router.post("/register-construction", responses={
    200: {
        "description": "Obra cadastrada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "employee_id": 1,
                        "client_id": 1,
                        "client_adress_id": 1,
                        "is_done": True
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}},  status_code=status.HTTP_201_CREATED)
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
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')


@token_employee_required
@async_session
@router.get("/list-construction", status_code=status.HTTP_200_OK, response_model=None)
async def list_constructions(session: AsyncSession = Depends(conn.get_async_session)) -> any:
    try:

        async with session.begin():
            query = select(Constructions).options(joinedload(Constructions.client_adress)).\
            options(joinedload(Constructions.employee)).\
            options(joinedload(Constructions.os_construction)).\
            options(joinedload(Constructions.client))
            result = await session.execute(query)
            result = result.unique()
            constructions: List[ConstructionSchema] = result.scalars().all()
            return constructions
        
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')

    
@token_employee_required
@async_session
@router.get("/get-one-construction", status_code=status.HTTP_200_OK)
async def get_one_checklist(construction_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 

        async with session.begin():
            construction = await session.execute(select(Constructions).where(Constructions.id == construction_id).options(joinedload(Constructions.client_adress)).\
                                                   options(joinedload(Constructions.employee)).\
                                                    options(joinedload(Constructions.os_construction)).\
                                                    options(joinedload(Constructions.client)))
            construction = construction.unique()

            if construction:
                obj_construction = construction.scalar_one()
                return obj_construction
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.put('/update-construction/{construction_id}', status_code=status.HTTP_202_ACCEPTED)
async def update_construction(construction_id: int, construction: ConstructionUpdate, session: AsyncSession = Depends(conn.get_async_session)):
    try:

        async with session.begin():
            constructions = await session.execute(select(Constructions).where(Constructions.id == construction_id))
            existing_construction = constructions.scalars().first()

            if existing_construction:
                existing_construction.is_done = construction.is_done
                await session.commit()
                return existing_construction
            else:
                return {"message": "Obra não encontrada"}
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-construction", status_code=status.HTTP_200_OK)
async def delete_construction(construction_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    construction = await session.execute(select(Constructions).where(Constructions.id == construction_id))
    try: 

        async with session.begin():
            construction = await session.execute(select(Constructions).where(Constructions.id == construction_id))

            if construction:
                obj_construction = construction.scalar_one()
                await session.delete(obj_construction)
                await session.commit()
                return {"message": "Obra deletada com sucesso"}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")