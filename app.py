from flask import Flask
from models.models import db, User
import os

app = Flask(__name__, template_folder="templates")

# Get project root
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# DB path inside /models
db_path = os.path.join(BASE_DIR, "models", "parking.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'afd'

# Init DB
db.init_app(app)

# Import models AFTER db is defined
# db.init_app(app)
# app.app_context().push()
# db.create_all()

from controllers.file1 import file1_bp
app.register_blueprint(file1_bp)

# ✅ Function to seed initial data
def seed_data():
    if not User.query.first():  # only seed if table is empty
        users = [
            ('userbot1', 'u1'),
            ('userbot2', 'u2'),
            ('userbot3', 'u3')
        ]

        creators = [
            ('creatorbot1', 'c1'),
            ('creatorbot2', 'c2'),
            ('creatorbot3', 'c3')
        ]

        admins = [
            ('admin', 'admin')
        ]

        for e, p in users:
            u1 = User(email=e, password=p)
            db.session.add(u1)

        for e, p in creators:
            u1 = User(email=e, password=p, isCreator=True)
            db.session.add(u1)

        for e, p in admins:
            u1 = User(email=e, password=p, isAdmin=True)
            db.session.add(u1)
        db.session.commit()
        print("✅ Sample users inserted.")
    else:
        print("ℹ️ Users already exist, skipping seeding.")


# Create tables
with app.app_context():
    db.create_all()
    seed_data()


    
# from __init__ import create_app
# app = create_app()
if __name__ == "__main__":
    app.run(debug=True)
# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True, use_reloader=False)

# if __name__ == "__main__":
#     # create tables only once inside an app context
#     with app.app_context():
#         db.create_all()
    
#     # run without auto-reloader (avoids 2 processes on Windows)
#     app.run(debug=True, use_reloader=False)



