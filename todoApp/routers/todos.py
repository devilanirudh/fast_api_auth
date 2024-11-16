from timeit import default_timer
from typing import Annotated

from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, defer
from starlette.exceptions import HTTPException
from starlette.staticfiles import PathLike
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from routers import auth

from models import Todos

from fastapi import APIRouter, Depends , Path
from .auth import get_current_user
from sqlalchemy.orm import sessionmaker

import models
from database import  SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

class TodoRequest(BaseModel):
    title:str = Field(min_length=3)
    description:str=Field(min_length=3,max_length=100)
    priority:int = Field(gt=-1,lt=6)
    complete:bool


@router.get("/")
async def read_all(user:user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='could not validate user.')
    return db.query(Todos).filter(Todos.owner_id==user.get('id')).all()


@router.get("/todo/{todo_id}",status_code= HTTP_200_OK)
async def read_todo(user :user_dependency,db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='could not validate user.')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail='todo not found')


@router.post("/todo",status_code=HTTP_201_CREATED)
async def create_todo(user:user_dependency,db:db_dependency , todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=401,detail='authentication failed')
    todo_model = Todos(**todo_request.model_dump(),owner_id=user.get('id'))
    db.add(todo_model)
    db.commit()


@router.put("/todo/{todo_id}" , status_code=HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency,db:db_dependency,todo_id:int,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='authentication failed')

    todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()


    if todo_model is None:
        raise HTTPException(status_code=404,detail='no content')
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}",status_code=HTTP_204_NO_CONTENT)
async def delete_todo(db:db_dependency,todo_id:int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='todo not found')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()