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
    songs = db.relationship('Song', backref='user', lazy=True)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    lyrics = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, default='')
    date = db.Column(db.String, default='')
    rating = db.Column(db.String, default='')
    isBlacklisted = db.Column(db.String, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)