import sqlite3
import plotly.graph_objs as go
from fastapi.responses import FileResponse
import pytz
from datetime import date, datetime, timedelta

class Nutrition:

    def __init__(self):
        
        self.table = "nutrition"

        self.con = sqlite3.connect("healthy.db")
        self.cur = self.con.cursor()

        self.cur.execute("CREATE TABLE IF NOT EXISTS nutrition (username NOT NULL, date, name, calories, serving_size, fat_total, fat_saturated, protein, sodium, potassium, cholesterol, carbohydrates, fiber, sugar);")
        self.con.commit()
        #   Example of a row:
        #         [
        #    {
        #     "username":"Marian",
        #     "date":"2003-07-17",
        #     "name": "fries",
        #     "calories": 317.7,
        #     "serving_size_g": 100,
        #     "fat_total_g": 14.8,
        #     "fat_saturated_g": 2.3,
        #     "protein_g": 3.4,
        #     "sodium_mg": 212,
        #     "potassium_mg": 124,
        #     "cholesterol_mg": 0,
        #     "carbohydrates_total_g": 41.1,
        #     "fiber_g": 3.8,
        #     "sugar_g": 0.3
        #   }
        # ]


    def add_meal(self, data: dict):
        
        self.cur.execute(f'SELECT username FROM users WHERE username = ?', (data['username'],))
        result = self.cur.fetchone()

        if result is None:
            return {"message": f"user not found"}
        # We search a row based on username name & date

        self.cur.execute(f"SELECT * FROM {self.table} WHERE username = ? AND date = ? AND name = ?", (data['username'], data['username'], data['username']))
        fetched_meal = self.cur.fetchone()

        self.cur.execute(f'INSERT INTO {self.table} (username, date, name, calories, serving_size, fat_total, fat_saturated, protein, sodium, potassium, cholesterol, carbohydrates, fiber, sugar) VALUES ( :username, :date, :name, :calories, :serving_size_g, :fat_total_g, :fat_saturated_g, :protein_g, :sodium_mg, :potassium_mg, :cholesterol_mg, :carbohydrates_total_g, :fiber_g, :sugar_g);', data)
        self.con.commit()

        return {"message": "meal added"}


    def delete_meal(self, username:str, meal:str):

        self.cur.execute(f'SELECT username FROM {self.table} WHERE username = ?', (username,))
        result = self.cur.fetchone()

        if result is None:
            return {"message": f"user doesnt have meals"}
        
        self.cur.execute(f'SELECT name FROM {self.table} WHERE name = ? AND username = ?', (meal,username,))
        result = self.cur.fetchone()

        if result is None:
            return {"message": f"meal not found"}
        else:
            self.cur.execute(f'DELETE FROM {self.table} WHERE name = ? AND username = ?', (meal,username,))
            self.con.commit()

            return {"message": f"meal deleted"}

    def have_meal(self, username: str, meal_date: str, meal:str):

        self.cur.execute(f'SELECT username FROM {self.table} WHERE username = ?', (username,))
        result = self.cur.fetchone()

        if result is None:
            return {"message": f"user doesnt exist"}    

        meal=meal.lower()
        
        if meal_date == "today":
            meal_date = datetime.now(pytz.timezone('Europe/Bucharest')).date()
        elif meal_date == "yesterday":
            meal_date = datetime.now(pytz.timezone('Europe/Bucharest')).date() - timedelta(days = 1)
        else:
            return {"message": f"select date of meal as yesterday or today"}

        self.cur.execute(f'SELECT serving_size FROM {self.table} WHERE name = ? AND username = ? AND date = ?', (meal,username,meal_date,))
        result = self.cur.fetchone()
        
        if result is None:
            return {"message": f"user doesnt have that meal on that date"}

        return True
    
    def update_meal_from_today_or_yesterday(self, username: str, data: str, dict: dict):

        if data == "today":
            data = datetime.now(pytz.timezone('Europe/Bucharest')).date()
        elif data == "yesterday":
            data = datetime.now(pytz.timezone('Europe/Bucharest')).date() - timedelta(days=1)
        else:
            return {"message": "enter today or yesterday!"}
        response_dict = {
            'username': username,
            'date': data,
            **dict
        }

        self.cur.execute(f'DELETE FROM {self.table} WHERE name = ? AND username = ? AND date = ?', (response_dict["name"], username, data))
        self.con.commit()

        self.cur.execute(f'INSERT INTO {self.table} (username, date, name, calories, serving_size, fat_total, fat_saturated, protein, sodium, potassium, cholesterol, carbohydrates, fiber, sugar) VALUES ( :username, :date, :name, :calories, :serving_size_g, :fat_total_g, :fat_saturated_g, :protein_g, :sodium_mg, :potassium_mg, :cholesterol_mg, :carbohydrates_total_g, :fiber_g, :sugar_g);', response_dict)
        self.con.commit()

        return {"message": "meal updated"}

    def see_day(self, username: str, day: date):

        self.cur.execute(f'SELECT username FROM {self.table} WHERE username = ?', (username,))
        result = self.cur.fetchone()

        if result is None:
            return {"message": f"username not found"}
        
        self.cur.execute(f"SELECT SUM(calories), SUM(fat_total), SUM(fat_saturated), SUM(protein), SUM(sodium), SUM(potassium), SUM(cholesterol), SUM(carbohydrates), SUM(fiber), SUM(sugar) FROM {self.table} WHERE username = ? AND date = ?", (username, day,))
        result = self.cur.fetchone()

        if result[0] is None:
            return {"message": f"user doesnt have meals"}

        calories, fat_total, fat_saturated, protein, sodium, potassium, cholesterol, carbohydrates, fiber, sugar = result

        data = {
            "calories": calories,
            "fat_total": fat_total,
            "fat_saturated": fat_saturated,
            "protein": protein,
            "sodium": sodium,
            "potassium": potassium,
            "cholesterol": cholesterol,
            "carbohydrates": carbohydrates,
            "fiber": fiber,
            "sugar": sugar
        }

        return data

    def see_chart(self, username: str, start: date, end: date):

        self.cur.execute(f'SELECT username FROM {self.table} WHERE username = ?', (username,))
        result = self.cur.fetchone()

        if result is None:
            return {"message": f"user doesnt have meals"}
        
        dates = []
        calories = []
        fat_total = []
        fat_saturated = []
        protein = []
        sodium = []
        potassium = []
        cholesterol = []
        carbohydrates = []
        fiber = []
        sugar = []

        current_date = start
        while current_date <= end:
            self.cur.execute(f"SELECT SUM(calories), SUM(fat_total), SUM(fat_saturated), SUM(protein), SUM(sodium), SUM(potassium), SUM(cholesterol), SUM(carbohydrates), SUM(fiber), SUM(sugar) FROM {self.table} WHERE username = ? AND date = ?", (username, str(current_date)))
            result = self.cur.fetchone()
            
            caloriesq, fat_totalq, fat_saturatedq, proteinq, sodiumq, potassiumq, cholesterolq, carbohydratesq, fiberq, sugarq = result

            if any(result):
                calories.append(caloriesq)
                fat_total.append(fat_totalq)
                fat_saturated.append(fat_saturatedq)
                protein.append(proteinq)
                sodium.append(sodiumq)
                potassium.append(potassiumq)
                cholesterol.append(cholesterolq)
                carbohydrates.append(carbohydratesq)
                fiber.append(fiberq)
                sugar.append(sugarq)
                dates.append(str(current_date))
                
            current_date += timedelta(days=1)

        # trace for nutritional information    

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=calories, mode='lines', name='Calories (g)'))
        fig.add_trace(go.Scatter(x=dates, y=fat_total, mode='lines', name='Total Fat (g)'))
        fig.add_trace(go.Scatter(x=dates, y=fat_saturated, mode='lines', name='Saturated Fat (g)'))
        fig.add_trace(go.Scatter(x=dates, y=protein, mode='lines', name='Protein (g)'))
        fig.add_trace(go.Scatter(x=dates, y=sodium, mode='lines', name='Sodium (mg)'))
        fig.add_trace(go.Scatter(x=dates, y=potassium, mode='lines', name='Potassium (mg)'))
        fig.add_trace(go.Scatter(x=dates, y=cholesterol, mode='lines', name='Cholesterol (mg)'))
        fig.add_trace(go.Scatter(x=dates, y=carbohydrates, mode='lines', name='Carbohydrates (g)'))
        fig.add_trace(go.Scatter(x=dates, y=fiber, mode='lines', name='Fiber (g)'))
        fig.add_trace(go.Scatter(x=dates, y=sugar, mode='lines', name='Sugar (g)'))

        fig.update_layout(
            title="Nutritional Facts/Time",
            xaxis_title="Date",
            yaxis_title="Amount",
            hovermode="x unified"
        )

        fig.write_image("/home/syneto-lab-dark-side/src/db/nutrition.png")

        return FileResponse("/home/syneto-lab-dark-side/src/db/nutrition.png")
