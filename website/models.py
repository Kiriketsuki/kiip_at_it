from enum import unique
from sqlalchemy.sql.expression import false
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(1000))
    date = db.Column(db.DateTime(timezone = False), default = func.now())
    completed = db.Column(db.Boolean, default = False)
    modifiable = db.Column(db.Boolean, default = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, default = func.now())
    email = db.Column(db.String(128), unique = True)
    password = db.Column(db.String(128))
    username = db.Column(db.String(128), unique = True)
    notes = db.relationship('Note')