from flaskext.sqlalchemy import SQLAlchemy
from flaskext.login import UserMixin

from .users import db

class User(db.Model, UserMixin):
    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    email  = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(40))

    def __init__(self, email, password):
        self.email = email
        self.password = password
