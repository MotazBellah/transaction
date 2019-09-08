# from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from models import *
from time import gmtime, strftime
from datetime import datetime
from time import sleep
from flask_executor import Executor
from flask import session as login_session
from wtform_fields import *
import os
from views import app, db


# executor = Executor(app)
# app.config['EXECUTOR_TYPE'] = 'thread'
# app.config['EXECUTOR_MAX_WORKERS'] = 25


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

                                balance_target = target.ethereum_balance + tran.currency_amount
                                target.ethereum_balance = balance_target
                                db.session.merge(target)
                                db.session.commit()
                                db.session.remove()

                                tran.state = "Transaction success."
                                tran.time_processed = datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")
                                db.session.merge(tran)
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
