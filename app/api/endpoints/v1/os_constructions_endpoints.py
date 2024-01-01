from fastapi import APIRouter, File, UploadFile, Depends, status, HTTPException

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List


from app.schemas.os_constructions_schemas import OsConstructionsCreate
from app.models.os_constructions_models import OsConstructions
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from database import conn
from database.conn import async_session


router = APIRouter()


@token_employee_required
@async_session
@router.post("/register-os-construction", status_code=status.HTTP_201_CREATED)
async def register_os_construction(osconstruction: OsConstructionsCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(OsConstructions).where(OsConstructions.client_id == osconstruction.client_id, OsConstructions.employee_id == osconstruction.employee_id, 
                                                                 OsConstructions.construction_id == osconstruction.construction_id, OsConstructions.checklist_auto_id == osconstruction.checklist_auto_id, 
                                                                 OsConstructions.checklist_cam_id == osconstruction.checklist_cam_id, OsConstructions.checklist_sound_id == osconstruction.checklist_sound_id, 
                                                                 OsConstructions.other_checklist_id == osconstruction.other_checklist_id,
                                                                 OsConstructions.sale == osconstruction.sale, OsConstructions.scheduling == osconstruction.scheduling, OsConstructions.signature_client == osconstruction.signature_client,
                                                                 OsConstructions.signature_emplooye == osconstruction.signature_emplooye, OsConstructions.solution == osconstruction.solution, OsConstructions.info == osconstruction.info,
                                                                 OsConstructions.end_date == osconstruction.end_date))
    existing_os_construction = result.scalar()
    if existing_os_construction: 
        raise HTTPException(status_code=400, detail="Já temos essa ordem de serviço registrada")
    
    try: 
        new_os_construction = OsConstructions(client_id=osconstruction.client_id, employee_id=osconstruction.employee_id, construction_id=osconstruction.construction_id, 
                                              checklist_auto_id=osconstruction.checklist_auto_id, checklist_cam_id=osconstruction.checklist_cam_id, checklist_sound_id=osconstruction.checklist_sound_id,
                                              other_checklist_id=osconstruction.other_checklist_id, sale=osconstruction.sale, scheduling=osconstruction.scheduling, signature_client=osconstruction.signature_client,
                                              signature_emplooye=osconstruction.signature_emplooye, solution=osconstruction.solution, info=osconstruction.info, end_date=osconstruction.end_date)

        session.add(new_os_construction)
        await session.commit()

        return {"message":"Ordem de serviço para obra criada com sucesso"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-os-construction")
async def list_os_osconstructions(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        query = select(OsConstructions)
        result = await session.execute(query)
        osconstruction: List[OsConstructionsCreate] = result.scalars().all()
        return osconstruction
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-os-constructions", status_code=status.HTTP_200_OK)
async def get_one_os_constructions(dependencies=Depends(JWTBearerEmployee()), os_construction_id: int = None, session: AsyncSession = Depends(conn.get_async_session)):
    os_constructions_id = await session.execute(select(OsConstructions).where(OsConstructions.id == os_construction_id))
    try: 
        if os_constructions_id:
            obj_os_construction = os_constructions_id.scalar_one()
            return obj_os_construction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-os-constructions", status_code=status.HTTP_200_OK)
async def delete_os_constructions(os_constructions_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    constructions_id = await session.execute(select(OsConstructions).where(OsConstructions.id == os_constructions_id))
    try: 
        if constructions_id:
            obj_os_constructions = constructions_id.scalar_one()
            await session.delete(obj_os_constructions)
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