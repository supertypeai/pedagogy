from flask import Flask
from flask_caching import Cache
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
import logging
from logging.handlers import SMTPHandler
import altair as alt

app = Flask(__name__)
app.config.from_object(Config)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)

migrate = Migrate(app, db)
login = LoginManager(app)
admin = Admin(app, name='pedagogy')
mail = Mail(app)
cache = Cache(app)


# define the vega theme with altair
def default_pedagogy_theme():
    return {
        'background': 'null'
    }


alt.themes.register('default_pedagogy_theme', default_pedagogy_theme)
alt.themes.enable('default_pedagogy_theme')
alt.renderers.set_embed_options(actions=False)

# let Flask-Login know which page (function name) handles login
login.login_view = 'login'

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = ()

from app import routes, models, adminconf, users, errors
