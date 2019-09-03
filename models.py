import sys, os
from datetime import datetime
from pytz import utc

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    """ User model """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512), nullable=False)
    Description = db.Column(db.String(1000))
    email = db.Column(db.String(1000), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key=True)
    bitcoin_id =  db.Column(db.Integer)
    bitcoin_balance =  db.Column(db.String(1000000), nullable=False)
    ethereum_id =  db.Column(db.Integer)
    ethereum_balance =  db.Column(db.String(1000000), nullable=False)
    max_amount = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)


class Transaction(db.Model):
    __tablename__ = 'transaction'

    id = db.Column(db.Integer, primary_key=True)
    currency_amount = db.Column(db.Float, nullable=False)
    currency_Type = db.Column(db.String(), nullable=False)
    target_user = db.Column(db.Integer, nullable=False)
    time_created = db.Column(db.String(250), default=datetime.now(utc))
    time_processed = db.Column(db.String(250), default=datetime.now(utc))
    state = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
