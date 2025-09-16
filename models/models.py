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
    playlists = db.relationship('Playlist', backref='user', lazy=True)
    albums = db.relationship('Album', backref='user', lazy=True)
    
    def __repr__(self):
        return f"<User {self.name}>"



SongInPlaylist = db.Table(
    'song_in_playlist',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
)

SongInAlbum = db.Table(
    'song_in_album',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True)
)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    lyrics = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, default='')
    date = db.Column(db.String, default='')
    rating = db.Column(db.String, default='')
    isBlacklisted = db.Column(db.String, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    playlists = db.relationship('Playlist', secondary=SongInPlaylist, backref=db.backref('songs', lazy=True), lazy='subquery' )
    albums = db.relationship('Album', secondary=SongInAlbum, backref=db.backref('songs', lazy=True), lazy='subquery' )

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    genre = db.Column(db.String, default='')
    artist=db.Column(db.String, default='')
    isBlacklisted = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class UserRating(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    rating_id = db.Column(db.Integer, nullable=False)