
from fastapi import FastAPI

from auth import auth_router
# from models import models_router

app = FastAPI()

app.include_router(auth_router)
# app.include_router(models_router)


@app.get("/")
async def landing():
    return {"message": "This is landing page"}
