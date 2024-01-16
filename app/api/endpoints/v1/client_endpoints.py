from fastapi import Depends, HTTPException,status, APIRouter

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from jose import jwt
from datetime import datetime
from typing import List

from app.schemas.client_schemas import ClientCreate, ClientUpdate, TokenClientSchema, requestdetails, changepassword
from app.models.client_models import Client, TokenTableClient
from app.auth.auth_bearer_client import JWTBearerClient
from app.auth.auth_handle import get_hashed_password, create_access_token,create_refresh_token,verify_password, token_client_required
from database import conn
from database.conn import async_session


ACCESS_TOKEN_EXPIRE_MINUTES = 30 
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"


router = APIRouter()

 
@router.post("/register", responses={
    200: {
        "description": "Cliente cadastrado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "username": "John Doe",
                        "email": "johndoe@gmail.com", 
                        "password": "12345678",
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def register_user(client: ClientCreate, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Client).where(Client.email == client.email))
    existing_user = result.scalar()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(client.password)

    new_user = Client(username=client.username, email=client.email, password=encrypted_password )

    session.add(new_user)
    await session.commit()

    return new_user.id


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
}}, response_model=TokenClientSchema)
async def login(request: requestdetails, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Client).where(Client.email == request.email))
    client = result.scalar()
    if client is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email incorreto")
    hashed_pass = client.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Senha incorreta"
        )
    
    access=create_access_token(client.id)
    refresh = create_refresh_token(client.id)

    token_db = TokenTableClient(user_id=client.id,  access_toke=access,  refresh_toke=refresh, status=True)
    session.add(token_db)
    await session.commit()

    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@token_client_required
@router.get('/getusers', status_code=status.HTTP_200_OK)
async def getusers(dependencies=Depends(JWTBearerClient()), db: AsyncSession = Depends(conn.get_async_session)):
    async with db as session:
        query = select(Client)
        result = await session.execute(query)
        user: List[ClientCreate] = result.scalars().unique().all()

        return user
    

@token_client_required
@async_session
@router.put('/update-client/{client_id}', responses={
    200: {
        "description": "Cliente atualizado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "username": "João",
                        "email": "joão@gmail.com"
  
                    }

                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_202_ACCEPTED)
async def update_client(client_id: int, client_update: ClientUpdate, session: AsyncSession = Depends(conn.get_async_session)):
    try:
        async with session.begin():
            client = await session.execute(select(Client).where(Client.id == client_id))
            existing_client = client.scalars().first()

            if existing_client:
                if client_update.username is not None:
                    existing_client.username = client_update.username
                else: 
                    existing_client.username = existing_client.username

                if client_update.email is not None:
                    existing_client.email = client_update.email
                else: 
                    existing_client.email = existing_client.email                
    
                await session.commit()
                return existing_client
            else:
                return {"message": "Cliente não encontrado"}
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    

@router.post('/change-password', status_code=status.HTTP_202_ACCEPTED)
async def change_password(request: changepassword, session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Client).where(Client.email == request.email))
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Client não encontrado")
    
    if not verify_password(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha antiga inválida")
    
    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    session.commit()
    
    return {"message": "Senha alterada com sucesso"}


@token_client_required
@router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(dependencies=Depends(JWTBearerClient()), session: AsyncSession = Depends(conn.get_async_session)):
    token = dependencies
    payload = jwt.decode(token, JWT_SECRET_KEY, ALGORITHM)
    user_id = payload['sub']
    info = []
    result = await session.execute(select(TokenTableClient))
    token_record = result.scalars().all()

    for record in token_record :
        print("record",record)
        if (datetime.utcnow() - record.created_date).days >1:
            info.append(record.user_id)
    
    if info:
        result = await session.execute(select(TokenTableClient).where(TokenTableClient.user_id.in_(info)))
        existing_tokens = result.scalars().all()

        for token in existing_tokens:
            await session.delete()
        
    result = await session.execute(
    select(TokenTableClient).where(
        TokenTableClient.user_id == int(user_id),
        TokenTableClient.access_toke == str(token)
    )
    )
    existing_token = result.scalars().first()
    
    if existing_token:
        existing_token.status = False
        await session.commit()
        await session.refresh(existing_token)

    return {"message": "Logout realizado com sucesso"}


@token_client_required
@async_session
@router.get('/get-clients', status_code=status.HTTP_200_OK)
async def list_users(is_activate: bool = None, is_deactivate: bool = None, dependencies=Depends(JWTBearerClient()), session: AsyncSession = Depends(conn.get_async_session)):
    client_is_activate = await session.execute(select(Client).where(Client.is_active == True))
    client_is_deactivate = await session.execute(select(Client).where(Client.is_active == False))
    result = await session.execute(select(Client))
    try:
        if is_activate == True:
            return client_is_activate.scalar()
        elif is_deactivate == True:
            return client_is_deactivate.scalar()
        else: 
            return result.scalar()

    except Exception as e:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")


@token_client_required
@async_session
@router.delete('/deactivate-client', status_code=status.HTTP_200_OK)
async def deactivate_client(client_id: int = None, dependencies=Depends(JWTBearerClient()), session: AsyncSession = Depends(conn.get_async_session)):
    client = await session.execute(select(Client).where(Client.id == client_id))
    try: 
        if client:
            obj_client = client.scalar_one()
            obj_client.is_active = False
            return {"message": "funcionário desativado"}
    except Exception as e:
        HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")