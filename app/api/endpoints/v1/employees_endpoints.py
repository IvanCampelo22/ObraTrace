from app.schemas.employee_schemas import EmployeeCreate, TokenEmployeeSchema, requestdetails, changepassword
from app.models.employees_models import Employees, TokenTableEmployees
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import get_hashed_password, create_access_token,create_refresh_token,verify_password, token_employee_required
from fastapi import Depends, HTTPException,status, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from database import conn
from sqlalchemy.future import select
from jose import jwt
from datetime import datetime
from typing import List

ACCESS_TOKEN_EXPIRE_MINUTES = 30 
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

router=APIRouter()

@router.post("/register")
async def register_user(employee: EmployeeCreate, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Employees).where(Employees.email == employee.email))
    existing_user = result.scalar()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(employee.password)

    new_user = Employees(username=employee.username, email=employee.email, password=encrypted_password )

    session.add(new_user)
    await session.commit()

    return {"message":"cliente criado com sucesso"}


@router.post('/login' ,response_model=TokenEmployeeSchema)
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
@router.get('/getusers', response_model=List[EmployeeCreate])
async def getusers(dependencies=Depends(JWTBearer()), db: AsyncSession = Depends(conn.get_async_session)):
    async with db as session:
        query = select(Employees)
        result = await session.execute(query)
        user: List[EmployeeCreate] = result.scalars().unique().all()

        return user
    

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
@router.post('/logout')
async def logout(dependencies=Depends(JWTBearer()), session: AsyncSession = Depends(conn.get_async_session)):
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
            await session.delete()
        
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