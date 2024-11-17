from timeit import default_timer
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, defer
from starlette.exceptions import HTTPException
from starlette.staticfiles import PathLike
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from routers import auth

from models import Todos, Users

from fastapi import APIRouter, Depends , Path
from .auth import get_current_user
from sqlalchemy.orm import sessionmaker

import models
from database import  SessionLocal

router = APIRouter(prefix='/auth',
    tags=['admin'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/todo",status_code=HTTP_200_OK)
async def read_all(user:user_dependency,db:db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401,detail='authentication failed')
    return db.query(Users).all()

@router.delete("/todo/{todo_id}",status_code=HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency,db:db_dependency,todo_id:int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401,detail='authentication failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='todo not found')
    db.query(Todos).filter(Todos.id==todo_id).delete()
    db.commit()