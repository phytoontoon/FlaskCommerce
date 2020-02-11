from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager
from flask_marshmallow import Marshmallow 
app=Flask(__name__)
app.config['SECRET_KEY']='1234'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
ma = Marshmallow(app)

from ProiectPa.models import User , Pizza , Pastas, Salads,Drinks , Sauce, Ingredients , Post , CustomPizza

from ProiectPa import routes