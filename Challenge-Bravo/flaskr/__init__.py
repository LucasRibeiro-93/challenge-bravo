# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 22:03:23 2021

@author: lucas
"""


import os

from flask import Flask
from flask_apscheduler import APScheduler


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.add_job(func=scheduled_task, trigger="interval", seconds="1")
    scheduler.start()

    from . import db
    db.init_app(app)

    from . import exchange_price
    app.register_blueprint(exchange_price.bp)

    return app