from fastapi import APIRouter, File, UploadFile, Depends, status, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.schemas.checlist_sound_schemas import CheckListSoundCreate
from app.models.checklist_sound_models import CheckListSound
from app.auth.auth_bearer_employee import JWTBearerEmployee
from app.auth.auth_handle import token_employee_required
from database import conn
from database.conn import async_session


router = APIRouter()


@token_employee_required
@async_session
@router.post("/create-checklist-sound", responses={
    200: {
        "description": "Checklist para som criado com sucesso",
        "content": {
            "application/json": {
                "example": [
                    {   
                            "qtd_sound_box": 6,
                            "qtd_cable": 2,
                            "qtd_conn": 2,
                            "qtd_ampli": 1,
                            "qtd_receiver": 0,
                            "other_equipament": "Microfone"
                    }
                ]
            }
        },
        404: {"description": "Insira dados válidos"}
}}, status_code=status.HTTP_201_CREATED)
async def create_checlist_sound(checlistsound: CheckListSoundCreate, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):    

    result = await session.execute(select(CheckListSound).where(CheckListSound.qtd_sound_box == checlistsound.qtd_sound_box, CheckListSound.qtd_cable == checlistsound.qtd_cable, CheckListSound.qtd_conn == checlistsound.qtd_conn, CheckListSound.qtd_ampli == checlistsound.qtd_ampli, CheckListSound.qtd_receiver == checlistsound.qtd_receiver,  CheckListSound.other_equipament == checlistsound.other_equipament))
    existing_checlistsound = result.scalar()
    if existing_checlistsound: 
        return {"message": f"Já temos algo igual no nosso banco de dados {existing_checlistsound.id}"}
    try: 
        new_checlistsound = CheckListSound(employee_id=checlistsound.employee_id, qtd_sound_box=checlistsound.qtd_sound_box, qtd_cable=checlistsound.qtd_cable, qtd_conn=checlistsound.qtd_conn, qtd_ampli=checlistsound.qtd_ampli, qtd_receiver=checlistsound.qtd_receiver, other_equipament=checlistsound.other_equipament)

        session.add(new_checlistsound)
        await session.commit()
        await session.refresh()

        return {"message":"Checklist para instalação de som criado com sucesso!"}
    
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/list-checklist-sound", status_code=status.HTTP_200_OK)
async def list_checklist_sound(dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    try: 
        query = select(CheckListSound)
        result = await session.execute(query)
        checklist_sound: List[CheckListSoundCreate] = result.scalars().all()
        return checklist_sound
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'{e}')
    

@token_employee_required
@async_session
@router.get("/get-one-checklist-sound", status_code=status.HTTP_200_OK)
async def get_one_checklist_sound(checklist_sound_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(CheckListSound).where(CheckListSound.id == checklist_sound_id))
    try: 
        if checklist_id:
            obj_checklist = checklist_id.scalar_one()
            return obj_checklist
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")
    

@token_employee_required
@async_session
@router.delete("/delete-checklist-sound", status_code=status.HTTP_200_OK)
async def delete_checklist_sound(checklist_sound_id: int = None, dependencies=Depends(JWTBearerEmployee()), session: AsyncSession = Depends(conn.get_async_session)):
    checklist_id = await session.execute(select(CheckListSound).where(CheckListSound.id == checklist_sound_id))
    try: 
        if checklist_id:
            obj_checklist = checklist_id.scalar_one()
            await session.delete(obj_checklist)
            await session.commit()
            return {"message": "Checklist deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


# @async_session
# @router.post("/uploadfile/", status_code=status.HTTP_200_OK)
# async def create_upload_file(file: UploadFile = File(...), session: AsyncSession = Depends(conn.get_async_session)):
#     file_location = f"/home/ivan/Downloads/{file.filename}"
#     with open(file_location, "wb+") as file_object:
#         file_object.write(file.file.read())
    
#     new_image = CheckListSound(file_budget=file_location)
#     session.add(new_image)
#     await session.commit()
#     await session.refresh(new_image)
    
#     return {"filename": new_image.file_budget}