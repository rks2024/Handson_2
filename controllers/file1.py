from flask import Flask, render_template, request, session, redirect, url_for, flash, Blueprint
from models.models import db, User, Song
from functools import wraps

file1_bp = Blueprint("file1", __name__)

def get_curr_user():
    id = session.get('id', None)
    u = None
    if id:
        u = User.query.filter_by(id=id).first()
    return u

# Here is a custom decorator that verifies the JWT is present in the request,
# as well as insuring that the JWT has a claim indicating that this user is
# an administrator

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = get_curr_user()
            if user and user.isAdmin:
                return fn(*args, **kwargs)
            else:
                flash('Authorization Denied', 'danger')
                return redirect(url_for('file1.access'))

        return decorator

    return wrapper

def creator_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = get_curr_user()
            if user and user.isCreator:
                return fn(*args, **kwargs)
            else:
                flash('Authorization Denied', 'danger')
                return redirect(url_for('file1.access'))

        return decorator

    return wrapper

def user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user = get_curr_user()
            if user and user.isUser:
                return fn(*args, **kwargs)
            else:
                flash('Authorization Denied', 'danger')
                return redirect(url_for('file1.access'))

        return decorator

    return wrapper

@file1_bp.route('/')
@user_required()
def home():
    user = get_curr_user()
    song_id=request.args.get('song_id')
    song= Song.query.filter_by(id=song_id).first()
    songs =Song.query.filter_by(isBlacklisted=False).all()
    if user:
        playlists=user.playlists
    else:
        playlists=[]
    return render_template('home.html', user=user, song=song, playlists=playlists, songs=songs)
    
@file1_bp.route('/nav')
def nav():
    return render_template('navbar.html')

@file1_bp.route('/playlist')
def playlist():
    curr_usr = get_curr_user()
    return render_template('playlist.html', user=curr_usr)

@file1_bp.route('/access')
def access():
    return render_template('access.html')

@file1_bp.route('/login', methods=['POST'])
def login():
    e = request.form.get('email', None)
    p = request.form.get('password', None)

    if e and p:
        u = User.query.filter_by(email=e, password=p).first()
        if u:
            session['id'] = u.id
            flash(f"Login is successful for you FOOL KOOMAR {u.email}", 'success')
            return redirect(url_for('file1.home'))

        else:
            flash(f"baadam khaale idiot, bhul gya username password {e}", 'danger')
            return redirect(url_for('file1.access'))
    else:
        flash(f"LOL ho gya, abey kuchh likh to sahi bimbi", 'warning')
        return redirect(url_for('file1.access'))

    
@file1_bp.route('/register', methods=['POST'])
def register():
    e = request.form.get('email', None)
    p = request.form.get('password', None)
    cp = request.form.get('ConfirmPassword', None)

    if e and p and p == cp:
        if not User.query.filter_by(email=e, password=p).first():
            u1 = User(email=e, password=p, isCreator=True)
            db.session.add(u1)
            db.session.commit()

    return redirect(url_for('file1.access'))

@file1_bp.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('file1.access'))

@file1_bp.route('/songs')
@creator_required()
def songs():
    curr_usr = get_curr_user()
    songs = curr_usr.songs
    song_id = request.args.get('song_id')
    song =Song.query.filter_by(id=song_id).first()
    return render_template('songs.html', user = curr_usr, songs=songs, song=song)

@file1_bp.route('/upload_song', methods=['POST'])
def upload_song():
    curr_user = get_curr_user()
    title = request.form.get('title')
    duration = request.form.get('duration')
    date = request.form.get('date')
    lyrics = request.form.get('lyrics')
    file = request.files.get('file')
    
    if title and file:

        songObj = Song(title=title, lyrics=lyrics, duration=duration, date=date, user_id=curr_user.id)

        db.session.add(songObj)
        db.session.commit()

        filename=f'{songObj.id}' + '.mp3'
        file.save(f'./static/songs/{filename}')
        flash("abey ho gya upload", 'success')
    else:
        flash("title and file field can not be empty", 'danger')

    return redirect(url_for('file1.songs'))

@file1_bp.route('/flag')
def flag():
    return "this feature will be added soon"

@file1_bp.route('/add_to_playlist')
def add_to_playlist():
    return "coming soon"

@file1_bp.route('/rating', methods=['POST'])
def rating():
    return f"{request.form.get('rating')}"

# @app.route('./show_home_songs')
# def show_home_songs():
#     curr_usr = get_curr_user()
#     songs = curr_usr.songs
#     return render_template('show_home_songs.html', user = curr_usr, songs=songs)