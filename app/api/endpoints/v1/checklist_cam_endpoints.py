from fastapi import APIRouter, File, UploadFile, Depends, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.schemas.checlist_cam_schemas import CheckListCamCreate, CheckListCamUpdate
from app.models.checklist_cam_models import CheckListCam
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from database import conn
from database.conn import async_session


router = APIRouter()


@token_employee_required
@async_session
@router.post("/create-checklist-cam", responses={
    200: {
        "description": "Checklist para câmeras criado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                            "employee_id": 1,
                            "qtd_cam": 2,
                            "qtd_box_cable": 1,
                            "qtd_rca": 8,
                            "qtd_p4": 4,
                            "qtd_dvr": 1,
                            "qtd_hd": 1,
                            "hds_size": 1,
                            "other_equipament": "cabo utp, dois conectores rj"
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def create_checlist_cam(checlistcam: CheckListCamCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):    
    try: 
        async with session.begin():
            result = await session.execute(select(CheckListCam).where(CheckListCam.qtd_cam == checlistcam.qtd_cam, CheckListCam.qtd_box_cable == checlistcam.qtd_box_cable, CheckListCam.qtd_rca == checlistcam.qtd_rca, CheckListCam.qtd_p4 == checlistcam.qtd_p4, CheckListCam.qtd_dvr == checlistcam.qtd_dvr, CheckListCam.qtd_hd == checlistcam.qtd_hd, CheckListCam.hds_size == checlistcam.hds_size, CheckListCam.other_equipament == checlistcam.other_equipament))
            existing_checlistcam = result.scalar()
            if existing_checlistcam: 
                return {"message": f"Já temos algo igual no nosso banco de dados {existing_checlistcam.id}"}
            
            new_checlistcam = CheckListCam(employee_id=checlistcam.employee_id, qtd_cam=checlistcam.qtd_cam, qtd_box_cable=checlistcam.qtd_box_cable, qtd_rca=checlistcam.qtd_rca, qtd_p4=checlistcam.qtd_p4, qtd_dvr=checlistcam.qtd_dvr, qtd_hd=checlistcam.qtd_hd, hds_size=checlistcam.hds_size, other_equipament=checlistcam.other_equipament)

            session.add(new_checlistcam)
            await session.commit()

            return {"message":"Checklist para instalação de câmeras criado com sucesso!"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-checklist-auto", responses={
    200: {
        "description": "Checklist para câmeras criado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {       
                            "id": 1, 
                            "employee_id": 1,
                            "qtd_cam": 2,
                            "qtd_box_cable": 1,
                            "qtd_rca": 8,
                            "qtd_p4": 4,
                            "qtd_dvr": 1,
                            "qtd_hd": 1,
                            "hds_size": 1,
                            "other_equipament": "cabo utp, dois conectores rj"
                    }, 
                    {       
                            "id": 2,
                            "employee_id": 2,
                            "qtd_cam": 3,
                            "qtd_box_cable": 1,
                            "qtd_rca": 8,
                            "qtd_p4": 4,
                            "qtd_dvr": 1,
                            "qtd_hd": 1,
                            "hds_size": 1,
                            "other_equipament": "cabo utp, dois conectores rj"
                    }

                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_200_OK)
async def list_checklist_cam(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        async with session.begin:
            query = select(CheckListCam)
            result = await session.execute(query)
            checklist_cam: List[CheckListCamCreate] = result.scalars().all()
            return checklist_cam
        
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-checklist-cam", responses={
    200: {
        "description": "Checklist para câmeras criado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {       
                            "id": 1,
                            "employee_id": 1,
                            "qtd_cam": 2,
                            "qtd_box_cable": 1,
                            "qtd_rca": 8,
                            "qtd_p4": 4,
                            "qtd_dvr": 1,
                            "qtd_hd": 1,
                            "hds_size": 1,
                            "other_equipament": "cabo utp, dois conectores rj"
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_200_OK)
async def get_one_checklist_cam(checklist_cam_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(CheckListCam).where(CheckListCam.id == checklist_cam_id))
    try: 
        async with session.begin:
            if checklist_id:
                obj_checklist = checklist_id.scalar_one()
                return obj_checklist
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    
@token_employee_required
@async_session
@router.put('/update-checklist-cam/{checklist_cam_id}', responses={
    200: {
        "description": "Checklist de câmera atualizada com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                        "employee_id": 1,
                        "qtd_cam": 2,
                        "qtd_box_cable": 1,
                        "qtd_rca": 8,
                        "qtd_p4": 4,
                        "qtd_dvr": 1,
                        "qtd_hd": 1,
                        "hds_size": 1,
                        "other_equipament": "cabo utp, dois conectores rj"
                    }

                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_202_ACCEPTED)
async def update_checklist_cam(checklist_cam_id: int, checklistcam: CheckListCamUpdate, session: AsyncSession = Depends(conn.get_async_session)):
    try:
        async with session.begin():
            checklist = await session.execute(select(CheckListCam).where(CheckListCam.id == checklist_cam_id))
            existing_checklist = checklist.scalars().first()

            if existing_checklist:
                if checklistcam.employee_id is not None:
                    existing_checklist.employee_id = checklistcam.employee_id
                else: 
                    existing_checklist.employee_id = existing_checklist.employee_id

                existing_checklist.qtd_cam = checklistcam.qtd_cam
                existing_checklist.qtd_box_cable = checklistcam.qtd_box_cable
                existing_checklist.qtd_rca = checklistcam.qtd_rca
                existing_checklist.qtd_p4 = checklistcam.qtd_p4
                existing_checklist.qtd_dvr = checklistcam.qtd_dvr
                existing_checklist.qtd_hd = checklistcam.qtd_hd
                existing_checklist.hds_size = checklistcam.hds_size
                existing_checklist.other_equipament = checklistcam.other_equipament

                await session.commit()
                return existing_checklist
            else:
                return {"message": "Checklist não encontrado"}
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")
    
    
@token_employee_required
@async_session
@router.delete("/delete-checklist-cam", responses={
    200: {
        "description": "Checklist para câmeras criado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {       
                            "message": "Checklist deletado com sucesso"
                    }
                ]
            }
        },
        404: {"description": "Não foi possível deletar o checklist"}
}}, status_code=status.HTTP_200_OK)
async def delete_checklist_cam(checklist_cam_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(CheckListCam).where(CheckListCam.id == checklist_cam_id))
    try: 
        async with session.begin:
            if checklist_id:
                obj_checklist = checklist_id.scalar_one()
                await session.delete(obj_checklist)
                await session.commit()
                return {"message": "Checklist deletado com sucesso"}
            
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")


@token_employee_required
@async_session
@router.post("/uploadfile/", status_code=status.HTTP_200_OK)
async def create_upload_file(checklist_id: int, file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
    checklist = await session.execute(select(CheckListCam).where(CheckListCam.id == checklist_id))
    existing_checklist = checklist.scalars().first()
    try:
        file_location = f"/home/ivan/Projects/homelabs/backend-homelabs-app{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        new_image = CheckListCam(employee_id=existing_checklist.employee_id, file_budget=file_location)
        session.add(new_image)
        await session.commit()
        await session.refresh(new_image)
        
        return {"filename": new_image.file_budget}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"{e}")