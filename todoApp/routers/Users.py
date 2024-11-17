from timeit import default_timer
from typing import Annotated

from fastapi.openapi.utils import status_code_ranges
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, defer
from starlette.exceptions import HTTPException
from starlette.staticfiles import PathLike
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from routers import auth

from models import Todos, Users

from fastapi import APIRouter, Depends , Path
from .auth import get_current_user, bcrypt_context
from sqlalchemy.orm import sessionmaker

import models
from database import  SessionLocal

router = APIRouter(prefix='/user',
    tags=['users'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserVerification(BaseModel):
    password:str
    new_password:str = Field(min_length=6)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]

@router.get("/",status_code=HTTP_200_OK)
async def get_user(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=404,detail='no such information')
    user_id = (user.get('id'))
    return db.query(Users).filter(Users.id==user_id).first()



#@router.put("/change_password/{user_name}/{new_password}",status_code=HTTP_200_OK)
@router.put("/change_password",status_code = HTTP_204_NO_CONTENT )
#async def change_password(user:user_dependency,db:db_dependency,new_password:str):
async def change_password(user:user_dependency,db:db_dependency,user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=404, detail='no such information')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
  #  user_id1 = (user.get('id'))
 #   user_id = db.query(Users).filter(Users.id == user_id1).first()
  #  output = bcrypt_context.hash(new_password),
  #  user_pass = "".join(output)
   # print(type(output))
  #  print(user_id.id)

    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=401,detail='error on password change')
    user_model.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)

#    if user_id is None:
      #  raise HTTPException(status_code=404, detail='no such information')

  #  user_id.hashed_password = user_pass

 #   db.add(user_id)
    db.commit()
 #   return 'updated'

@router.get("/all111",status_code=HTTP_200_OK)
async def get_user1(db:db_dependency):
    return db.query(Users).all()



