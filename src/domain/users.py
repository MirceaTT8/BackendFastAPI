from datetime import date
from pydantic import BaseModel

class User(BaseModel):
    username: str
    email: str
    height: float
    weight: float
    birthday: date
