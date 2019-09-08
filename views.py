from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from time import gmtime, strftime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask import session as login_session
from wtform_fields import *
from models import db as d
import os
from datetime import datetime
from time import sleep
from flask_executor import Executor


app = Flask(__name__)
app.secret_key="sdfdsuperfdlkngflkjnlkbgirlsdhjdrefsdfucfgfgfhhyah!!!!!dfghhm;glhjkhjl,.jk"
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///currency.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# configure flask_login
login = LoginManager()
login.init_app(app)
app.config['LOGIN_DISABLED'] = False

# Flask-Executor use concurrent.futures to launch parallel tasks
# https://flask-executor.readthedocs.io/en/latest/
# https://docs.python.org/3/library/concurrent.futures.html#module-concurrent.futures
executor = Executor(app)
app.config['EXECUTOR_TYPE'] = 'thread'
app.config['EXECUTOR_MAX_WORKERS'] = 25


def transaction_run():
    """Get the transaction request and decide
    if it will success or not"""
    print('working...')
    # Get all transaction
    transactions = executor.submit(Transaction.query.filter_by(done=False).all)
    print(transactions.result())
    # Check if thier a transactions
    if transactions.result():
        # Go through each transaction
        for tran in transactions.result():
            print("Looping...")
            # print(trans)
            # Get the currency account for the source user
            currency = executor.submit(Currency.query.filter_by(user_id=tran.user_id).first).result()
            print(currency)
            # target_user = executor.submit(User.query.filter_by(id=tran.target_user).first).result()
            # print(target_user)
            # Get the currency account for the target user
            target = executor.submit(Currency.query.filter_by(user_id=tran.target_user).first).result()
            # Get the transaction account for the target user
            trans_target = executor.submit(Transaction.query.filter_by(user_id=tran.target_user).first).result()
            ### # TODO:
            trans_source = executor.submit(Transaction.query.filter_by(user_id=tran.user_id).first).result()
            # update replace all tran with trans_source

            print(tran)
            # print(target_user)
            print(target)
            print(trans_target)
            # Check if the target user has account
            if target:
                # If the user send to himself fail the transaction
                if tran.user_id == tran.target_user:
                    tran.state = "Transaction faild."
                    db.session.merge(tran)
                    db.session.commit()
                    db.session.remove()
                else:
                    # If the currency type is bitcoin
                    # Check if the user has a bitcoin ID
                    if tran.currency_Type.lower() == "bitcoin":
                        if not currency.bitcoin_id:
                            tran.state = "Transaction faild."
                            # trans_source.state = "Transaction faild. You don't have a bitcoin account!"
                            db.session.merge(tran)
                            db.session.commit()
                            db.session.remove()
                        # If user has a bitcoin ID
                        # Check if transfared money greater than his balance or not
                        # Check if transfared money greater than the max amount per transaction or not
                        else:
                            if tran.currency_amount > currency.bitcoin_balance:
                                tran.state = "Transaction faild."
                                db.session.merge(tran)
                                db.session.commit()
                                db.session.remove()
                            elif tran.currency_amount > currency.max_amount:
                                tran.state = "Transaction faild."
                                db.session.merge(tran)
                                db.session.commit()
                                db.session.remove()
                            # Everything ok, then subtract the transfared money from source user
                            # Add transfare maney to target user
                            else:
                                balance = currency.bitcoin_balance - tran.currency_amount
                                # updated_balance = str(balance)
                                currency.bitcoin_balance = balance
                                db.session.merge(currency)
                                db.session.commit()
                                db.session.remove()

                                balance_target = target.bitcoin_balance + tran.currency_amount
                                target.bitcoin_balance = balance_target
                                db.session.merge(target)
                                db.session.commit()
                                db.session.remove()

                                tran.state = "Transaction success."
                                tran.time_processed = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                                db.session.merge(tran)
                                db.session.commit()
                                db.session.remove()

                    # If the currency type is ethereum
                    # Check if the user has a ethereum ID
                    elif tran.currency_Type.lower() == "ethereum":
                        if not currency.ethereum_id:
                            tran.state = "Transaction faild."
                            # trans_source.state = "Transaction faild. You don't have a ethereum account!"
                            db.session.merge(tran)
                            db.session.commit()
                            db.session.remove()
                        # If user has a ethereum ID
                        # Check if transfared money greater than his balance or not
                        # Check if transfared money greater than the max amount per transaction or not
                        else:
                            if tran.currency_amount > currency.ethereum_balance:
                                tran.state = "Transaction faild."
                                # trans_source.state = "Transaction faild. You don't have enough money!"
                                db.session.merge(tran)
                                db.session.commit()
                                db.session.remove()
                            elif tran.currency_amount > currency.max_amount:
                                tran.state = "Transaction faild."
                                # trans_source.state = "Transaction faild. You exceed the max amount!"
                                db.session.merge(tran)
                                db.session.commit()
                                db.session.remove()
                            # Everything ok, then subtract the transfared money from source user
                            # Add transfare maney to target
                            else:
                                balance = currency.ethereum_balance - tran.currency_amount
                                currency.ethereum_balance = balance
                                db.session.merge(currency)
                                db.session.commit()
                                db.session.remove()
                                tran.state = "Transaction success."
                                # tran.time_processed = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)"))
                                db.session.merge(tran)
                                db.session.commit()
                                db.session.remove()

                                balance_target = target.ethereum_balance + tran.currency_amount
                                target.ethereum_balance = balance_target
                                db.session.merge(target)
                                db.session.commit()
                                db.session.remove()
                    # if the currency type not bitcoin or ethereum
                    else:
                        tran.state = "Transaction faild."
                        db.session.merge(tran)
                        db.session.commit()
                        db.session.remove()
            # If the user has no currency account
            else:
                tran.state = "Transaction faild."
                db.session.merge(tran)
                db.session.commit()
                db.session.remove()


            # Finish the transaction request
            print(tran)
            tran.done = True
            db.session.merge(tran)
            db.session.commit()
            db.session.remove()
        print('Done!!!!')


# manage a database connection
# To avaid  connection time out errors
@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.close()
    db.session.remove()
    d.session.remove()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
@app.route('/register', methods=['GET', 'POST'])
def login_form():
    """Home page """
    # use executor to run the function in the background
    executor.submit(transaction_run)
    # Registartion Form
    reg_form = RegistartionForm()
    # Allow register if the validation success
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        email = reg_form.email.data
        password = reg_form.password.data
        # use hashed password to store it in the database
        hashed_pswd = pbkdf2_sha256.hash(password)
        # Add user to DB
        user = User(name=username, email=email, password=hashed_pswd)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()

        flash('Registered successfully. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template('log.html', form=reg_form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    # Use executor to run the Transaction in the background
    executor.submit(transaction_run)
    login_form = LoginForm()

    # Allow login if validation success
    if login_form.validate_on_submit():
        user_object = User.query.filter_by(email=login_form.email.data).first()
        login_user(user_object)
        # set the user_id value of login_session to be user id
        login_session['user_id'] = user_object.id
        flash('You are logged in', 'success')
        return redirect(url_for('mainPage', user_id=login_session['user_id']))

    return render_template("login.html", form=login_form)


@app.route('/logout')
@login_required
def logout():
    executor.submit(transaction_run)
    logout_user()
    return redirect(url_for('login'))


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def mainPage(user_id):
    """Main user page that display the information
    about the user account and give the user the ability to create/edit
    currency account and transfare money to someone else"""
    # Run transactions in the background
    executor.submit(transaction_run)
    user_id = login_session['user_id']
    # Get the currency information and display it on the page
    currency = Currency.query.filter_by(user_id=user_id).first()
    return render_template('user_page.html', user_id=user_id, currency=currency)


@app.route('/currency-account/<int:user_id>', methods=['GET', 'POST'])
def currencyAccount(user_id):
    """Create currency account form"""
    # Check if the login_required is disabled `in case of testing`
    if not app.config['LOGIN_DISABLED']:
        # If login required, check if the user is authenticated
        # Redirect the user to login page if he is not authenticated
        if not current_user.is_authenticated:
            flash("You are not logged in!", 'error')
            return redirect(url_for('login'))

    executor.submit(transaction_run)
    currency_form = CurrencyForm()

    # Allow create currency account if validation success
    if currency_form.validate_on_submit():
        bitcoin_id = currency_form.bitcoin_id.data
        bitcoin_balance = currency_form.bitcoin_balance.data
        ethereum_id = currency_form.ethereum_id.data
        ethereum_balance = currency_form.ethereum_balance.data
        max_amount = currency_form.max_amount.data
        # Check if the user already has currency account
        # Redirect him to main user page
        if Currency.query.filter_by(user_id=user_id).first():
            flash("This user has already an account", 'error')
            return redirect(url_for('mainPage', user_id=user_id))
        # Add currency to DB
        currency = Currency(bitcoin_id=bitcoin_id, bitcoin_balance=bitcoin_balance,
                            ethereum_id=ethereum_id, ethereum_balance=ethereum_balance,
                            max_amount=max_amount, user_id=user_id)
        db.session.add(currency)
        db.session.commit()

        flash('Created currency account successfully.', 'success')
        return redirect(url_for('mainPage', user_id=user_id))
    return render_template("currency_account.html",
                           form=currency_form,
                           user_id=user_id
                           )


@app.route('/edit-account/<int:user_id>', methods=['GET', 'POST'])
def editCurrency(user_id):
    """Edit currency account for the user"""
    # Check if the login_required is disabled `in case of testing`
    if not app.config['LOGIN_DISABLED']:
        # If login required, check if the user is authenticated
        # Redirect the user to login page if he is not authenticated
        if not current_user.is_authenticated:
            flash("You are not logged in!", 'error')
            return redirect(url_for('login'))
    # Run the transaction in the background
    executor.submit(transaction_run)
    currency_form = EditCurrencyForm()
    # Get the account that will be edited
    editedAccount = Currency.query.filter_by(user_id=user_id).first()
    # Check if this account not exsits
    # Redirect the user to create currency account page
    if not editedAccount:
        flash('You have to create an account first .', 'error')
        return redirect(url_for('currencyAccount', user_id=user_id))
    # Allow edit if validation success
    if currency_form.validate_on_submit():
        # check if bitcoin_id is changed
        if currency_form.bitcoin_id.data:
            editedAccount.bitcoin_id = currency_form.bitcoin_id.data
            db.session.merge(editedAccount)
            db.session.commit()
            db.session.close()
        # check if bitcoin_balance is changed
        if currency_form.bitcoin_balance.data:
            editedAccount.bitcoin_balance = currency_form.bitcoin_balance.data
            db.session.merge(editedAccount)
            db.session.commit()
            db.session.close()
        # check if max_amount is changed
        if currency_form.max_amount.data:
            editedAccount.max_amount = currency_form.max_amount.data
            db.session.merge(editedAccount)
            db.session.commit()
            db.session.close()
        # check if ethereum_id is changed
        if currency_form.ethereum_id.data:
            editedAccount.bitcoin_id = currency_form.bitcoin_id.data
            db.session.merge(editedAccount)
            db.session.commit()
            db.session.close()
        # check if ethereum_balance is changed
        if currency_form.ethereum_balance.data:
            editedAccount.ethereum_balance = currency_form.ethereum_balance.data
            db.session.merge(editedAccount)
            db.session.commit()
            db.session.close()

        flash('Edited currency account successfully.', 'success')
        return redirect(url_for('mainPage', user_id=user_id))
    return render_template("edit_currency.html",
                           form=currency_form,
                           user_id=login_session['user_id']
                           )



@app.route('/transaction/<int:user_id>', methods=['GET', 'POST'])
def transaction(user_id):
    """Transfare money page, allow the user to
    transfare money if validation success"""
    # Check if the login_required is disabled `in case of testing`
    if not app.config['LOGIN_DISABLED']:
        # If login required, check if the user is authenticated
        # Redirect the user to login page if he is not authenticated
        if not current_user.is_authenticated:
            flash("You are not logged in!", 'error')
            return redirect(url_for('login'))
    # Run the transaction in the background
    executor.submit(transaction_run)
    trans_form = TransactionForm()
    # Send transaction request if validation success
    if trans_form.validate_on_submit():
        currency_amount = trans_form.currency_amount.data
        currency_Type = trans_form.currency_Type.data
        target_user = trans_form.target_user.data
        # Add transaction to DB
        # `transaction_run` will decide if the transaction will success or not
        transaction = Transaction(currency_amount=currency_amount,
                               currency_Type=currency_Type,
                               target_user=target_user,
                               user_id=user_id)
        db.session.add(transaction)
        db.session.commit()
        # Get the transaction account for the target user
        target_tran = Transaction.query.filter_by(user_id=target_user).first()
        # Check if the target user does not has a transaction account
        # Create one for him in order to be able to recieve the transfared money
        if not target_tran:
            target_transaction = Transaction(user_id=target_user)
            db.session.add(target_transaction)
            db.session.commit()

        flash('Transaction request sent successfully.', 'success')
        return redirect(url_for('mainPage', user_id=user_id))
    return render_template("transaction.html",
                           form=trans_form,
                           user_id=user_id
                           )


@app.route('/transaction-history/<int:user_id>', methods=['GET', 'POST'])
@login_required
def transaction_history(user_id):
    """History page display the transaction information"""
    # Run the transaction in the background
    executor.submit(transaction_run)
    user_id = login_session['user_id']
    # Get all transaction made by all the users
    user_tran = Transaction.query.filter_by(done=True).filter_by(user_id=user_id).all()
    target_tran = Transaction.query.filter_by(done=True).filter_by(target_user=user_id).all()
    user_curr = Currency.query.filter_by(user_id=user_id).first()

    return render_template('trans_history.html',
                           transactions=user_tran + target_tran,
                           currency=user_curr)


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=PORT)
