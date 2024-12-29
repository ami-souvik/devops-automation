from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import get_query_token, get_token_header

# from app.routers import items
from .routers import apps

app = FastAPI()
# app = FastAPI(dependencies=[Depends(get_query_token)])

origins = [
    "http://localhost",
    "http://0.0.0.0",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(apps.router, prefix="/apps")