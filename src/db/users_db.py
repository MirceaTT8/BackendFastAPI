import sqlite3
from src.domain.users import User
from datetime import date, datetime

class UserDB:

    def __init__(self):
        
        self.table = "users"

        self.con = sqlite3.connect("healthy.db")
        self.cur = self.con.cursor()


        self.cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE, email TEXT UNIQUE, height REAL, weight REAL, birthday date)")
        self.con.commit()

    
    def create_user(self, user: User):

        user = user.dict()

        try:
            self.cur.execute(f'INSERT INTO {self.table} (username, email, height, weight, birthday) VALUES ( :username, :email, :height, :weight, :birthday);',user)
            self.con.commit()

            return {"message": f"user added"}

        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return {"error": f"username/email already exists"}
            else:
                return {"error": "An unknown error occurred while adding the user"}

    def read_users(self):

        self.cur.execute(f"SELECT * FROM {self.table};")
        rows = self.cur.fetchall()

        if rows:
            return rows
        else:
            return {"error": "no data found"}
        
        
    def read_user(self, username: str):

        self.cur.execute(f'SELECT username, email, height, weight FROM {self.table} WHERE username = ?', (username,))
        result = self.cur.fetchone()

        if result is None:
            return {"message": f"user not found"}

        self.cur.execute(f'SELECT birthday FROM {self.table} WHERE username = ?', (username,))
        result1 = self.cur.fetchone()
        age = 0

        if result1:
            date_of_birth = datetime.strptime(result1[0], "%Y-%m-%d").date()

            current_date = datetime.now().date()
            age = current_date.year - date_of_birth.year

            if current_date < datetime(current_date.year, date_of_birth.month, date_of_birth.day).date():
                age -= 1
        
        
        user = {
        "username":result[0],
        "email":result[1],
        "height":result[2],
        "weight":result[3],
        "age":age
        }

        return user
    
    def delete_user(self, username: str):
        
        self.cur.execute(f'SELECT username FROM {self.table} WHERE username = ?', (username,))
        result = self.cur.fetchone()
        
        if result is None:
            return {"message": f"user not found"}
        else:
            self.cur.execute(f'DELETE FROM {self.table} WHERE username = ?', (username,))
            self.con.commit()

            return {"message": f"user deleted"}
        

    def update_user(self, username: str, field: str, new_data):

        field_map = {
            "username": "username",
            "email": "email",
            "height": "height",
            "weight": "weight",
        }
        if field not in field_map:
            return {"error": "Field not found!"}

        user_key = field_map[field]

        self.cur.execute(f"UPDATE {self.table} SET {user_key} = ? WHERE username = ?", (new_data, username))
        self.con.commit()

        if self.cur.rowcount > 0:
            return {"message": "User updated successfully"}
        else:
            return {"message": "User not found"}
