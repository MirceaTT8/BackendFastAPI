In this project, you will see the implementation of a Gateway API which will help you manage a healthy way of life by computing your calories and nutritional intake based on the meals you had in span of one or more days.

Skills used in this project: Python3, FastAPI, SQLite3, Docker, Git.

Features implemented in this project:
- **User class**:
    * Can create a user with username, email, height, weight, and birth date. Username & email must be unique, all fields are mandatory.
    * Can list all the users, with their username & email only
    * Display a single user based on its username with all the info and their age (compute it from their birth date)
    * Delete a user based on its username
    * Edit a user. All fields are editable except the username
- **Nutrition class**:
    * The user can add meals to their profile. A meal contains the name, date, calories, and other nutritional values. This API will be used to gather the info https://api-ninjas.com/api/nutrition.
    * We can query a user's meals over a period of time. Give the start date and end date to the API as query params.
    * The user can delete one of its meals from the same day.
    * The user can edit a meal from the same day or the day before.
    * The user can see the calories & nutritional values of all the meals from a given day.
    * The user can see the calories & nutritional values of a given period of time as a chart

The code is structured this way:

    - main.py is used to get the API routers
    - using Repository Design Pattern
        -> in the domain folder we are holding the User class and the CRUD (create, read, update, delete) interface. The persistence attribute is used to choose between using a database or a JSON file. The JSON file is not implemented yet!
        -> in the db folder we have the implementations of the user interface: the operations for the User class + the operations for the Nutrition class. The chart of a given period with the meals consumed by a person is also present here
        -> In the API folder we set up a FastAPI router with endpoints to the implemented operations, here we can change the persistence value which for now only works for db!

    http://127.0.0.1:8000/docs#/
