# Coffee Shop
A Coffee Shop web application which allows you to to sign in and according to the authentication privileges 

# Getting Started
## Frontend
> _tip_: this frontend is designed to work with [Flask-based Backend](../backend). It is recommended you stand up the backend first, test using Postman, and then the frontend should integrate smoothly.

### Angular
The frontend of the project is build on Angular for more information on <a href="https://angular.io/">Angular click here </a>

### Running the server
```
npm start
```

## Backend
### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

# Features

1) Display graphics representing the ratios of ingredients in each drink.
2) Allow public users to view drink names and graphics.
3) Allow the shop baristas to see the recipe information.
4) Allow the shop managers to create new drinks and edit existing drinks.

# Parts of the Project

1. [`./backend/`](./backend/README.md)
2. [`./frontend/`](./frontend/README.md)

## Backend
The `./backend` directory contains Flask server with a SQLAlchemy module. It has a Flask API to know more about the endpoints: [click here](./backend/README.md) to open the backend README for more information.

## Frontend
The `./frontend` directory contains a complete Ionic frontend to consume the data from the Flask server. The frontend of the project is provided by FSND which is the Full Stack Nanodegree by Udacity.

[View the README.md within ./frontend for more details.](./frontend/README.md)


