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

# Implementation for user roles in the @login_required-decorator. Must be
# placed before view imports in this file
from functools import wraps

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user:
                return login_manager.unauthorized()
          
            if not current_user.is_authenticated():
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
                
                for user_role in current_user.roles():
                    if user_role == role:
                        unauthorized = False
                        break

            if unauthorized:
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


# Import views and models
from application.auth import models 
from application.auth import views

from application.factions import models
from application.factions import views

from application.ships import models
from application.ships import views

from application.weapons import models
from application.weapons import views

# Create db tables
try: 
    db.create_all()
except:
    pass