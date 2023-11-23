from fastapi import FastAPI
import logging
from loguru import logger 
import sys
from fastapi import FastAPI
# from app.api.routes import api_router


app = FastAPI(title='Ordem De Serviço')
# app.include_router(api_router)

logger.add("logs/logs.log",  serialize=False)
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>", backtrace=True, diagnose=True)
logger.opt(colors=True)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
