from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    isBlacklisted = db.Column(db.Boolean, default=False)
    isCreator = db.Column(db.Boolean, default=False)
    isAdmin = db.Column(db.Boolean, default=False)
    isUser = db.Column(db.Boolean, default=True)