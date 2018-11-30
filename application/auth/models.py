from application import db
from flask_login import UserMixin

class User(db.Model, UserMixin):

    # "user" is a reserved word in Postgres, so set the name of the db table based on this to be "account"
    __tablename__ = "account"
  
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False)
    password = db.Column(db.String(144), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False)

    # Attributes required by flask_login
    is_authenticated = True
    is_active = True
    is_anonymous = False

    def __init__(self, name, username, password):
        self.name = name
        self.username = username
        self.password = password
        self.is_admin = False
  
    def get_id(self):
        return self.id

    def role(self):
        if self.is_admin:
            return "ADMIN"
        return "USER"