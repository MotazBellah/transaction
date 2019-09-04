# from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from models import *
# from time import gmtime, strftime
# from flask_login import LoginManager, login_user, current_user, login_required, logout_user
# from flask import session as login_session
# from wtform_fields import *
# import os
# import json
# import threading
#
# from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
# from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# jobstores = {
#             'default': SQLAlchemyJobStore(url=app.config['SQLALCHEMY_DATABASE_URI'])
#         }
# executors = {
#             'default': ThreadPoolExecutor(20),
#             'processpool': ProcessPoolExecutor(5)
#         }
# job_defaults = {
#             'coalesce': True,
#             'max_instances': 1
#             # 'replace_existing':True,
#
#         }
# scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
#
#
# def transaction_run():
#     x = Transaction.query.filter_by(done=False).first
#     if x:
#         x.done = True
#         db.merge(x)
#         db.commit()
#
#
# scheduler.add_job(transaction_run, 'interval', seconds=7)
# scheduler.start()

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minutes.')


sched.start()
