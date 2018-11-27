from flask import Flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

import os

# Config for using Postgres database if running on Heroku, otherwise uses local
# sqlite database.
if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fleetreport.db"    
    app.config["SQLALCHEMY_ECHO"] = True

# Object for handling the database
db = SQLAlchemy(app)

# Import views and models
from application.auth import models 
from application.auth import views

from application.factions import models
from application.factions import views

from application.ships import models
from application.ships import views

from application.weapons import models
from application.weapons import views

# Initialization for login functionality
from application.auth.models import User
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Please log in to use this functionality."

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Create db tables
try: 
    db.create_all()
except:
    pass