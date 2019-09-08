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
- Create login route to accept the credentials of the Users
- Using wtforms build a login form
- After login success redirect the user to his main page

##### Add currency account for currency

- Give user the ability to create and edit the currency account
- Using wtforms and validator and create custom validation to set account details

##### Submit transaction to system

- Give the user who has the currency account to submit transaction to the system
- Using wtforms and validator and create custom validation to accept the transaction request
- display the transaction history
- Let the user know if the transaction success or fail

##### Implement a transaction processor that can run in parallel to the backend service and processes transactions

- Flask-Executor use concurrent.futures to launch parallel tasks
- `https://flask-executor.readthedocs.io/en/latest/`
- `https://docs.python.org/3/library/concurrent.futures.html#module-concurrent.futures`
- Created a function that work in the background and validate each transaction request and update each transaction

##### Protect all public endpoints against unauthorised access in some way.

- User login_required decorator
- checked if the current user is authenticated

## Database Installation on Heroku

1. Create App on Heroku.

2. On your app’s “Overview” page, click the “Configure Add-ons” button.

3. In the “Add-ons” section of the page, type in and select “Heroku Postgres.

4. Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision..

5. Click the “Heroku Postgres :: Database” link.

6. Click on “Settings”, and then “View Credentials.”. This information to hock my App to the DB

7. Run `heroku run python create.py` in order to convert the SQLAlchemy class to DB table and load the data to that table.

## Project Files

- models.py: Contain the class representation for DB table.

- create.py: File to build to DB tables

- views.py: application file

- wtform_fields: Contain wtforms class for each forms and validator

- Procfile: To  declare the process type, in this app the type is "web" and Identify thread operation

- tests Folder: contain test files

- requirements.txt: Contain a list of items to be installed, use the command to install all of items `pip install -r requirements.txt`
