from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *
from time import gmtime, strftime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask import session as login_session
from wtform_fields import *


app = Flask(__name__)
app.secret_key="sdfdsuperfdlkngflkjnlkbgirlsdhjdrefsdfucfgfgfhhyah!!!!!dfghhm;glhjkhjl,.jk"
app.config['WTF_CSRF_SECRET_KEY'] = "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

# app.config['SQLALCHEMY_DATABASE_URI']=os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///currency.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# configure flask_login
login = LoginManager(app)
login.init_app(app)
