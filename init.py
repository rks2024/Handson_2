from app import db, User

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
    db.session.commit()

for e, p in creators:
    u1 = User(email=e, password=p, isCreator=True)
    db.session.add(u1)
    db.session.commit()

for e, p in admins:
    u1 = User(email=e, password=p, isAdmin=True)
    db.session.add(u1)
    db.session.commit()