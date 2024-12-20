
from routers import auth,todos,admin,Users

from fastapi import FastAPI

import models
from database import engine

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(Users.router)
