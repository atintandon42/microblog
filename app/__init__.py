import os
from flask import Flask
from config import Config

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment


from logging.handlers import RotatingFileHandler
import logging


app_var = Flask(__name__)
app_var.config.from_object(Config)

db = SQLAlchemy(app_var)
migrate = Migrate(app_var, db)

login = LoginManager(app_var)
login.login_view = 'login'

bootstrap = Bootstrap(app_var)
moment = Moment(app_var)


from app import routes, models, errors

if not app_var.debug:
    # ...

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app_var.logger.addHandler(file_handler)

    app_var.logger.setLevel(logging.INFO)
    app_var.logger.info('Microblog startup')