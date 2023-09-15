from fastapi import APIRouter
import requests
from fastapi.responses import FileResponse, HTMLResponse
import sqlite3
from src.db.nutrition import Nutrition
from datetime import date, datetime, timedelta
import pytz

nutrition_router = APIRouter(prefix="/nutrition", tags=["nutrition"])

#instantiate object for Nutrition class

nutrition = Nutrition()

api_url = 'https://api.api-ninjas.com/v1/nutrition'

api_key = 'qUG+ziBjk1B2yCw3rbFzNQ==Mlr8pXLnMxPmCLFu'


@nutrition_router.post("/add_meal/{username}/{meal}")
async def add_meal(username: str, meal:str, data: date = datetime.now(pytz.timezone('Europe/Bucharest')).date()):
    
    query = meal
    
    response = requests.get(api_url, headers={'X-Api-Key': api_key}, params={"query": query})
    response =  response.json()
    
    if not response:
        return {"error": "API error"}
    
    response_dict = {
        'username': username,
        'date': data,
        **dict(response[0])
            }

    return nutrition.add_meal(response_dict)

@nutrition_router.delete("/delete_meal/{username}/{meal}")
async def delete_meal(username:str, meal: str):

    return nutrition.delete_meal(username, meal)

@nutrition_router.put("/update_meal/{username}/{data}/{meal}/{serving_size}")
async def update_serving_size_meal(username:str, data: str, meal: str, serving_size: float):

    value = nutrition.have_meal(username, data, meal)
    
    if value is False:
        {"error":"API error at finding the meal"}
        
    query = str(int(serving_size)) + "g " + meal
    response = requests.get(api_url,headers={'X-Api-Key': api_key},params={"query": query})
    
    response = response.json()

    if not response:
        return {"error": "API error"}

    return nutrition.update_meal_from_today_or_yesterday(username, data, response[0])

@nutrition_router.get("/see_day/{username}")
async def see_meals_from_day(username: str, day: str = str(datetime.now(pytz.timezone('Europe/Bucharest')).date())):

    return nutrition.see_day(username, day)

@nutrition_router.get("/see_chart/{username}/{start_date}")
async def see_meals_from_given_period_as_chart(username: str, start_date: date, end_date: date = datetime.now(pytz.timezone('Europe/Bucharest')).date()):

    return nutrition.see_chart(username, start_date, end_date)


