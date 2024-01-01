from fastapi import APIRouter, File, UploadFile, Depends, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.schemas.os_maintenance_schemas import OsMaintenanceCreate
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from app.models.os_maintenance_models import OsMaintenance
from database import conn
from database.conn import async_session


router = APIRouter()


@token_employee_required
@async_session
@router.post("/register-os-maintenance", status_code=status.HTTP_201_CREATED)
async def register_os_maintenance(osmaintenance: OsMaintenanceCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    result = await session.execute(select(OsMaintenance).where(OsMaintenance.client_id == osmaintenance.client_id, OsMaintenance.employee_id == osmaintenance.employee_id, 
                                                                 OsMaintenance.client_adress_id == osmaintenance.client_adress_id, OsMaintenance.checklist_auto_id == osmaintenance.checklist_auto_id, 
                                                                 OsMaintenance.checklist_cam_id == osmaintenance.checklist_cam_id, OsMaintenance.checklist_sound_id == osmaintenance.checklist_sound_id, 
                                                                 OsMaintenance.other_checklist_id == osmaintenance.other_checklist_id,
                                                                 OsMaintenance.sale == osmaintenance.sale, OsMaintenance.scheduling == osmaintenance.scheduling, OsMaintenance.signature_client == osmaintenance.signature_client,
                                                                 OsMaintenance.signature_emplooye == osmaintenance.signature_emplooye, OsMaintenance.solution == osmaintenance.solution, OsMaintenance.info == osmaintenance.info,
                                                                 OsMaintenance.end_date == osmaintenance.end_date))
    existing_os_construction = result.scalar()
    if existing_os_construction: 
        raise HTTPException(status_code=400, detail="Já temos essa ordem de serviço registrada")
    
    try: 
        new_os_maintenance = OsMaintenance(client_id=osmaintenance.client_id, employee_id=osmaintenance.employee_id, client_adress_id=osmaintenance.client_adress_id, 
                                              checklist_auto_id=osmaintenance.checklist_auto_id, checklist_cam_id=osmaintenance.checklist_cam_id, checklist_sound_id=osmaintenance.checklist_sound_id,
                                              other_checklist_id=osmaintenance.other_checklist_id, sale=osmaintenance.sale, scheduling=osmaintenance.scheduling, signature_client=osmaintenance.signature_client,
                                              signature_emplooye=osmaintenance.signature_emplooye, solution=osmaintenance.solution, info=osmaintenance.info, end_date=osmaintenance.end_date)

        session.add(new_os_maintenance)
        await session.commit()

        return {"message":"Ordem de serviço para manutenção criada com sucesso"}
    
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-os-maintenance", status_code=status.HTTP_200_OK)
async def list_os_maintenance(session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        query = select(OsMaintenance)
        result = await session.execute(query)
        osmaintenance: List[OsMaintenanceCreate] = result.scalars().all()
        return osmaintenance
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-os-maintenance", status_code=status.HTTP_200_OK)
async def get_one_os_maintenance(os_maintenance_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    maintenance_id = await session.execute(select(OsMaintenance).where(OsMaintenance.id == os_maintenance_id))
    try: 
        if maintenance_id:
            obj_os_construction = maintenance_id.scalar_one()
            return obj_os_construction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-os-maintenance", status_code=status.HTTP_200_OK)
async def delete_os_maintenance(os_maintenance_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    maintenance_id = await session.execute(select(OsMaintenance).where(OsMaintenance.id == os_maintenance_id))
    try: 
        if maintenance_id:
            obj_os_maintenance = maintenance_id.scalar_one()
            await session.delete(obj_os_maintenance)
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