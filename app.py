from flask import Flask, render_template, request, session, redirect, url_for, flash
from models import db, User, Song

app = Flask(__name__, template_folder="templates")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'
app.config['SECRET_KEY'] = 'afd'

db.init_app(app)
app.app_context().push()
db.create_all()


# class User():
#     def __init__(self):
#         self.isCreator = True

def get_curr_user():
    id = session.get('id', None)
    u = None
    if id:
        u = User.query.filter_by(id=id).first()
    return u

@app.route('/')
def home():
    user = get_curr_user()
    return render_template('home.html', user=user)
    
@app.route('/nav')
def nav():
    return render_template('navbar.html')

@app.route('/playlist')
def playlist():
    curr_usr = get_curr_user()
    return render_template('playlist.html', user=curr_usr)

@app.route('/access')
def access():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    e = request.form.get('email', None)
    p = request.form.get('password', None)

    if e and p:
        u = User.query.filter_by(email=e, password=p).first()
        if u:
            session['id'] = u.id
            flash(f"Login is successful for you FOOL KOOMAR {u.email}", 'success')
            return redirect(url_for('home'))

        else:
            flash(f"baadam khaale idiot, bhul gya username password {e}", 'danger')
            return redirect(url_for('access'))
    else:
        flash(f"LOL ho gya, abey kuchh likh to sahi bimbi", 'warning')
        return redirect(url_for('access'))

    
@app.route('/register', methods=['POST'])
def register():
    e = request.form.get('email', None)
    p = request.form.get('password', None)
    cp = request.form.get('ConfirmPassword', None)

    if e and p and p == cp:
        if not User.query.filter_by(email=e, password=p).first():
            u1 = User(email=e, password=p, isCreator=True)
            db.session.add(u1)
            db.session.commit()

    return redirect(url_for('access'))

@app.route('/logout')
def logout():
    session.pop('id', None)
    return redirect(url_for('access'))

@app.route('/songs')
def songs():
    curr_usr = get_curr_user()
    songs = curr_usr.songs
    song_id = request.args.get('song_id')
    song =Song.query.filter_by(id=song_id).first()
    return render_template('songs.html', user = curr_usr, songs=songs, song=song)

@app.route('/upload_song', methods=['POST'])
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

    return redirect(url_for('songs'))


app.run(debug=True)


