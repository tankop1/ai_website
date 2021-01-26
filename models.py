from flask_login import UserMixin
from app import db 

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), index=True, unique=False)
    last_name = db.Column(db.String(30), index=True, unique=False)
    username = db.Column(db.String(20), index=True, unique=True)
    password = db.Column(db.String(80), index=True, unique=True)
    email = db.Column(db.String(50), index=True, unique=False)