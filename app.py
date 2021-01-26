from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'supersecretkeyrightheredfshdjh'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myDatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

with app.app_context():
    db.create_all()

import routes