from fastapi import Depends, HTTPException,status, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.future import select

from jose import jwt
from datetime import datetime
from typing import List

from app.schemas.employee_schemas import EmployeeCreate, EmployeeUpdate, TokenEmployeeSchema, requestdetails, changepassword
from app.models.employees_models import Employees, TokenTableEmployees
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from app.auth.auth_handle import get_hashed_password, create_access_token,create_refresh_token,verify_password
from database import conn
from database.conn import async_session


ACCESS_TOKEN_EXPIRE_MINUTES = 30 
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"


router = APIRouter()


@router.post("/register", responses={
    201: {
        "description": "Funcionário cadastrado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "username": "John Doe",
                        "email": "johndoe@gmail.com", 
                        "password": "12345678",
                        "work_type": "Comercial"
                    }
                ]
            }
        },
        400: {"description": "Insira dados válidos"}
}})
async def register_user(employee: EmployeeCreate, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Employees).where(Employees.email == employee.email))
    existing_user = result.scalar()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(employee.password)

    new_user = Employees(username=employee.username, email=employee.email, password=encrypted_password, work_type=employee.work_type )

    session.add(new_user)
    await session.commit()

    return {"message":"funcionário criado com sucesso"}


@router.post('/login', responses={
    200: {
        "description": "Login realizado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "email": "johndoe@gmail.com", 
                        "password": "12345678",
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}},response_model=TokenEmployeeSchema)
async def login(request: requestdetails, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Employees).where(Employees.email == request.email))
    employee = result.scalar()
    if employee is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email incorreto")
    hashed_pass = employee.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha incorreta"
        )
    
    access=create_access_token(employee.id)
    refresh = create_refresh_token(employee.id)

    token_db = TokenTableEmployees(user_id=employee.id,  access_toke=access,  refresh_toke=refresh, status=True)
    session.add(token_db)
    await session.commit()

    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@token_employee_required
@router.get('/getusers', status_code=status.HTTP_200_OK)
async def getusers(dependencies=Depends(JWTBearerEmployee()), db: AsyncSession = Depends(conn.get_async_session)):
    async with db as session:
        query = select(Employees)
        result = await session.execute(query)
        user: List[EmployeeCreate] = result.scalars().unique().all()

        return user
    

@token_employee_required
@async_session
@router.get("/get-one-employee", status_code=status.HTTP_200_OK)
async def get_one_employee(employee_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        employee = await session.execute(select(Employees).where(Employees.id == employee_id))
        
        obj_adress = employee.scalar_one()
        return obj_adress
        
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Funcionário não encontrado'}) 
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    

@token_employee_required
@async_session
@router.put('/update-employee/{employee_id}', responses={
    201: {
        "description": "Funcionários atualizado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "username": "João",
                        "email": "joão@gmail.com",
                        "work_type": "Comercial"
                    }

                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def update_employee(employee_id: int, employee_update: EmployeeUpdate, session: AsyncSession = Depends(conn.get_async_session)):
    try:
        employee = await session.execute(select(Employees).where(Employees.id == employee_id))
        existing_employee = employee.scalars().first()

        if employee_update.username is not None:
            existing_employee.username = employee_update.username
        else: 
            existing_employee.username = existing_employee.username

        if employee_update.email is not None:
            existing_employee.email = employee_update.email
        else: 
            existing_employee.email = existing_employee.email            

        if employee_update.work_type is not None:
            existing_employee.work_type = employee_update.work_type
        else:
            existing_employee.work_type = existing_employee.work_type    

        await session.commit()
        return existing_employee
    
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Funcionário não encontrado'}) 
         
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    

@router.post('/change-password')
async def change_password(request: changepassword, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Employees).where(Employees.email == request.email))
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client não encontrado")
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha antiga inválida")
    
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    session.commit()
    
    return {"message": "Senha alterada com sucesso"}


@token_employee_required
@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    info = []
    result = await session.execute(select(TokenTableEmployees))
    token_record = result.scalars().all()

    for record in token_record :
        print("record",record)
        if (datetime.utcnow() - record.created_date).days >1:
            info.append(record.user_id)
    
    if info:
        result = await session.execute(select(TokenTableEmployees).where(TokenTableEmployees.user_id.in_(info)))
        existing_tokens = result.scalars().all()

        for token in existing_tokens:
            await session.delete(token)
        
    result = await session.execute(
    select(TokenTableEmployees).where(
        TokenTableEmployees.user_id == int(user_id),
        TokenTableEmployees.access_toke == str(token)
    )
    )
    existing_token = result.scalars().first()
    
    if existing_token:
        existing_token.status = False
        await session.commit()
        await session.refresh(existing_token)

    return {"message": "Logout realizado com sucesso"}


@token_employee_required
@async_session
@router.get('/get-employees', status_code=status.HTTP_200_OK)
async def list_users(is_activate: bool = None, is_deactivate: bool = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try:
        employee_is_activate = await session.execute(select(Employees).where(Employees.is_active == True))
        employee_is_deactivate = await session.execute(select(Employees).where(Employees.is_active == False))
        result = await session.execute(select(Employees))

        if is_activate == True:
            return employee_is_activate.scalar()
        elif is_deactivate == True:
            return employee_is_deactivate.scalar()
        else: 
            return result.scalar()
        
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Funcionário não encontrado'})
    
    except Exception as e:
        await session.rollback()
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")


@token_employee_required
@async_session
@router.delete('/deactivate-employee', status_code=status.HTTP_200_OK)
async def deactivate_employee(employee_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    employee = await session.execute(select(Employees).where(Employees.id == employee_id))
    try: 
        obj_employee = employee.scalar_one()
        obj_employee.is_active = False
        return {"message": "funcionário desativado"}
    
    except NoResultFound:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Funcionário não encontrado'}) 
    except Exception as e:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")