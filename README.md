# Money Transaction Website

App URL on Heroku https://transaction-s.herokuapp.com/

## Code style

- This project is written in python 3.
- Use Flask framework.
- Use Bootstrap in front-end

## Tasks:

#### Model and structure the following data in a "database" of your choice

- Used SQLAlchemy database to generate tables(user, currency, transaction )by represent each table with User class, Currency class, and Transaction class set relationship between them using ForeignKey, where User class contain the main information about the users like email, name,..., Currency class contain the information about the user currency account like bitcoin ID, bitcoin Balance, max amount per transfare,...
and connected between them using ForeignKey, Transaction class contain the main information should transaction request has like target user and max-amount
- Run `python create.py` in order to create database using `db.create_all` and transfare classes to database tables

#### Implement a backend service that provides the following endpoints / handlers
##### Create user (with basic user details)

- Create Flask route to register function
- Using wtforms, build form for registration
- Add the new user to database after validation success
- Create login route to accept the crenditionals of the Users
- After login success redirect the user to his main page
