from src.domain.users import User
from src.api.users import users_router
from src.api.nutrition import nutrition_router
from fastapi import FastAPI

app = FastAPI()
app.include_router(users_router)
app.include_router(nutrition_router)