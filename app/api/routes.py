from fastapi.routing import APIRouter
from app.api.endpoints.v1 import os_endpoints, construction_endpoints, os_constructions_endpoints
from app.api.endpoints.v1 import client_endpoints
from app.api.endpoints.v1 import employees_endpoints
from app.api.endpoints.v1 import client_adress_endpoints
api_router = APIRouter()

api_router.include_router(client_endpoints.router, prefix='/client', tags=['clients'])
api_router.include_router(employees_endpoints.router, prefix='/employee', tags=['employees'])
api_router.include_router(client_adress_endpoints.router, prefix='/client_adress', tags=['cliente_adresses'])
api_router.include_router(construction_endpoints.router, prefix="/constructions", tags=['constructions'])
api_router.include_router(os_constructions_endpoints.router, prefix="/os_constructions", tags=['os_constructions'])
api_router.include_router(os_endpoints.router, prefix="/os", tags=['os'])


