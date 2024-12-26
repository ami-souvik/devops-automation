from fastapi import Depends, FastAPI

from .dependencies import get_query_token, get_token_header

# from app.routers import items
from .routers import apps

app = FastAPI()
# app = FastAPI(dependencies=[Depends(get_query_token)])


app.include_router(apps.router, prefix="/apps")