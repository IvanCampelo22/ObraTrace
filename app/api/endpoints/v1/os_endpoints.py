from fastapi import APIRouter, File, UploadFile, Depends, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from typing import List

from app.schemas.os_schemas import OsCreate
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from app.models.os_models import Os
from database import conn
from database.conn import async_session


router = APIRouter()


@token_employee_required
@async_session
@router.post("/register-os", responses={
    200: {
        "description": "Ordem de serviço criada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "employee_id": 1,
                        "client_id": 1,
                        "client_adress_id": 1,
                        "os_type": "Manutenção",
                        "checklist_cam_id": 1,
                        "checklist_auto_id": 1,
                        "checklist_sound_id": 1,
                        "other_checklist_id": 1,
                        "scheduling": '2024-01-01',
                        "end_date": "2024-01-02",
                        "info": "Há três câmeras queimadas, de 16",
                        "solution": "Não há como consertar as câmeras, é necessário a troca",
                        "sale": "O cliente quer 3 câmeras para subtituir e quer expandir para 24 câmeras.",
                        "signature_emplooye": "João Roberto",
                        "signature_client": "John Doe",
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def register_os_(os: OsCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(Os).where(Os.client_id == os.client_id, Os.employee_id == os.employee_id, 
                                                                 Os.client_adress_id == os.client_adress_id, Os.os_type == os.os_type, Os.checklist_auto_id == os.checklist_auto_id, 
                                                                 Os.checklist_cam_id == os.checklist_cam_id, Os.checklist_sound_id == os.checklist_sound_id, 
                                                                 Os.other_checklist_id == os.other_checklist_id,
                                                                 Os.sale == os.sale, Os.scheduling == os.scheduling, Os.signature_client == os.signature_client,
                                                                 Os.signature_emplooye == os.signature_emplooye, Os.solution == os.solution, Os.info == os.info,
                                                                 Os.end_date == os.end_date))
    existing_os_construction = result.scalar()
    if existing_os_construction: 
        raise HTTPException(status_code=400, detail="Já temos essa ordem de serviço registrada")
    
    try: 
        new_os = Os(client_id=os.client_id, employee_id=os.employee_id, client_adress_id=os.client_adress_id, os_type=os.os_type,
                                              checklist_auto_id=os.checklist_auto_id, checklist_cam_id=os.checklist_cam_id, checklist_sound_id=os.checklist_sound_id,
                                              other_checklist_id=os.other_checklist_id, sale=os.sale, scheduling=os.scheduling, signature_client=os.signature_client,
                                              signature_emplooye=os.signature_emplooye, solution=os.solution, info=os.info, end_date=os.end_date)

        session.add(new_os)
        await session.commit()

        return {"message":"Ordem de serviço para manutenção criada com sucesso"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-os", status_code=status.HTTP_200_OK)
async def list_os(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        query = select(Os).options(joinedload(Os.client))
        result = await session.execute(query)
        result = result.unique()
        os: List[OsCreate] = result.scalars().all()
        return os
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-os", status_code=status.HTTP_200_OK)
async def get_one_os(os_id: int = None, session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        async with session.begin():
            os = await session.execute(select(Os).where(Os.id == os_id).options(joinedload(Os.client)))                    
            os = os.unique()

            if os_id:
                obj_construction = os.scalar_one()
                return obj_construction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-os", status_code=status.HTTP_200_OK)
async def delete_os(os__id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    os_id = await session.execute(select(Os).where(Os.id == os__id))
    try: 
        if os_id:
            obj_os = os_id.scalar_one()
            await session.delete(obj_os)
            await session.commit()
            return {"message": "Ordem de Serviço deletada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


# @async_session
# @router.post("/uploadfile/", status_code=status.HTTP_200_OK)
# async def create_upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
#     file_location = f"some/directory/{file.filename}"
#     with open(file_location, "wb+") as file_object:
#         file_object.write(file.file.read())
    
#     new_image = OsConstructions(image=file_location)
#     await session.add(new_image)
#     await session.commit()
#     await session.refresh(new_image)
    
#     return {"filename": new_image.image}