# Import Flask
from flask import Flask
app = Flask(__name__)

# Import and config SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///fleetreport.db"
# This makes SQLAlchemy print all SQL queries
app.config["SQLALCHEMY_ECHO"] = True

# Object for handling the database
db = SQLAlchemy(app)

# Import views and models
from application.auth import models 
from application.auth import views

from application.ships import models
from application.ships import views

# Create db tables
db.create_all()