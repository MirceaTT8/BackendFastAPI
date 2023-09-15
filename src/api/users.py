from fastapi import APIRouter
from src.domain.users import User
from src.domain.user_repo import UserRepository
import json
from src.db.users_db import UserDB

users_router = APIRouter(prefix="/users")

persistance = None

user_persistance = "db"

if(user_persistance == "db"):
    persistance = UserDB()
elif(user_persistance == "file"):
    persistance = UserJson()

user_repo = UserRepository(persistance)

@users_router.post("/create")
async def create_user(new_user: User):
    return user_repo.create_user(new_user)


@users_router.get("/read_all")
async def read_all():
    return user_repo.read_users()


@users_router.get("/read_one_user/{username}")
async def read_one_user(username:str):
    return user_repo.read_user(username)  


@users_router.delete("/delete/{username}")
async def delete_user(username: str):
    return user_repo.delete_user(username)


@users_router.put("/{username}/{field}/{new_data}")
async def update_field(username: str, field: str, new_data):
    return user_repo.update_user(username, field, new_data)
