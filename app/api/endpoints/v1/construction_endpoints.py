from fastapi import Depends, HTTPException,status, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound

from psycopg2.errors import ForeignKeyViolation
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
    201: {
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
        400: {"description": "Insira dados válidos"}
}},  status_code=status.HTTP_201_CREATED)
async def register_construction(construction: ConstructionCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try:  
        result = await session.execute(select(Constructions).where(Constructions.client_id == construction.client_id, Constructions.employee_id == construction.employee_id, Constructions.client_adress_id == construction.client_adress_id))
        existing_adress = result.scalar()
        
        if existing_adress:
            await session.rollback() 
            return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Já temos essa obra registrada")                 

        new_adress = Constructions(client_id=construction.client_id, employee_id=construction.employee_id, client_adress_id=construction.client_adress_id)
        
        if not new_adress.client_id or not new_adress.employee_id or not new_adress.client_adress_id: 
            await session.rollback()
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insira dados válidos")
        
        session.add(new_adress)
        await session.commit()

        return {"message":"Obra registrada com sucesso"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')


@token_employee_required
@async_session
@router.get("/list-construction", status_code=status.HTTP_200_OK, response_model=None)
async def list_constructions(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)) -> any:
    try:
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')

    
@token_employee_required
@async_session
@router.get("/get-one-construction", status_code=status.HTTP_200_OK)
async def get_one_checklist(construction_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        construction = await session.execute(select(Constructions).where(Constructions.id == construction_id).options(joinedload(Constructions.client_adress)).\
                                                options(joinedload(Constructions.employee)).\
                                                options(joinedload(Constructions.os_construction)).\
                                                options(joinedload(Constructions.client)))
        
        construction = construction.unique()
        obj_construction = construction.scalar_one()
        return obj_construction
        
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Obra não encontrada'})  
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    

@token_employee_required
@async_session
@router.put('/update-construction/{construction_id}', status_code=status.HTTP_201_CREATED)
async def update_construction(construction_id: int, construction: ConstructionUpdate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try:
        constructions = await session.execute(select(Constructions).where(Constructions.id == construction_id))
        existing_construction = constructions.scalars().first()

        existing_construction.is_done = construction.is_done

        if not existing_construction.client_id or not existing_construction.employee_id or not existing_construction.client_adress_id: 
            await session.rollback()
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Insira dados válidos")

        await session.commit()
        return existing_construction
        
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Obra não encontrada'}) 
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-construction", status_code=status.HTTP_200_OK)
async def delete_construction(construction_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        construction = await session.execute(select(Constructions).where(Constructions.id == construction_id))
        
        obj_construction = construction.scalar_one()
        await session.delete(obj_construction)
        await session.commit()
        return {"message": "Obra deletada com sucesso"}
        
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Obra não encontrada'}) 
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")