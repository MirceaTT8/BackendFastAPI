In this project you will see the implementation of a Gateway API which will help you manage a healthy way of life by computing your calories and nutritional intakes based on the meals you had in a period of one or more days.

Skills used in this project: Python3, FastAPI, sqlite3, Docker, Git.

Features implemented in this project:
User class: 1. Can create a user with username, email, height, weight and birth date. Username & email must be unique, all fields are mandatory. 2. Can list all the users, with their username & email only 3. Display a single user based on its username with all the info and their age (compute it from their birth date) 4. Delete a user based on its username 5. Edit a user. All fields are editable except username
Nutrition class: 6. A user can add meals to its profile. A meal contains the name, date, calories and other nutritional values. This API will be used to gather the info https://api-ninjas.com/api/nutrition. 7. We can query a user's meals on a period of time. Give start date and end date to the API as query params. 8. A user can delete one of its meals from the same day. 9. A user can edit a meal from the same day or the day before. 10. A user can see the calories & nutritional values of all the meals from a given day. 11. A user can see the calories & nutritional values of a given period of time as a chart

The code is structured this way:

    - main.py is used to get the API routers
    - using Repository Design Pattern
        -> in domain folder we are holding the User class and the CRUD (create,read,update,delete) interface. The persistance attribute is used to choose between using a database or a json file. The json file is not implemented yet!
        -> in db folder we have the implementations of the user interface: the operations for the User class + the operations for Nutrition class. The chart of a given period with the meals consumed by a person is also present here
        -> in api folder we set upt a FastAPI router with endpoints to the implemented operations, here we can change the persistance value which for now only works for db!

    http://127.0.0.1:8000/docs#/
