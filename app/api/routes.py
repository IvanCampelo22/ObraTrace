from fastapi.routing import APIRouter
from app.api.endpoints.v1 import checklist_auto_endpoints, checklist_cam_endpoints, checklist_sound_endpoints
from app.api.endpoints.v1 import client_endpoints
from app.api.endpoints.v1 import employees_endpoints
from app.api.endpoints.v1 import client_adress_endpoints
api_router = APIRouter()

api_router.include_router(client_endpoints.router, prefix='/client', tags=['clients'])
api_router.include_router(employees_endpoints.router, prefix='/employee', tags=['employees'])
api_router.include_router(client_adress_endpoints.router, prefix='/client_adress', tags=['cliente_adresses'])
api_router.include_router(checklist_auto_endpoints.router, prefix='/checklist_auto', tags=['checklist_auto_endpoints'])
api_router.include_router(checklist_cam_endpoints.router, prefix='/checklist_cam', tags=['checklist_cam_endpoints'])
api_router.include_router(checklist_sound_endpoints.router, prefix='/checklist_sound', tags=['checklist_sound_endpoints'])


