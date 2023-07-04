from DB import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(20))
    user_picture = db.Column(db.String(30))
    user_gender = db.Column(db.String(1))
    vip = db.Column(db.Integer, default=0)
    total_cost = db.Column(db.Integer, default=0)

    bills = db.relationship('Bill', back_populates='User')
    user_log = db.relationship('User_log', back_populates='User')
    recommendation = db.relationship('Recommendation', back_populates='User')
    collection = db.relationship("Collect", back_populates='User')

class Music(db.Model):
    __tablename__ = 'musics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    music_name = db.Column(db.String(50), nullable=False)
    music_picture = db.Column(db.String(30))
    lyric = db.Column(db.Text)
    album_name = db.Column(db.String(20))
    musician_id = db.Column(db.Integer, nullable=False)

    user_log = db.relationship('User_log', back_populates='Music')
    recommendation = db.relationship('Recommendation', back_populates='Music')
    collection = db.relationship("Collect", back_populates='Music')

class Musician(db.Model):
    __tablename__ = 'musicians'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    music_name = db.Column(db.String(50), nullable=False)
    music_picture = db.Column(db.String(30))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(50), nullable=False)

class Bill(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_date = db.Column(db.DateTime, default=func.now())
    transaction_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    music_id = db.Column(db.Integer, db.ForeignKey('musics.id'))
    content = db.Column(db.Text)

class Collect(db.Model):
    __tablename__ = 'collects'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    music_id = db.Column(db.Integer, db.ForeignKey('musics.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    song_list_name = db.Column(db.String(30), nullable=True)

class User_log(db.Model):
    __tablename__ = 'user_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    music_id = db.Column(db.Integer, db.ForeignKey('musics.id'))
    command_type = db.Column(db.Integer)
    input_time = db.Column(db.DateTime, default=func.now())

class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    music_id = db.Column(db.Integer, db.ForeignKey('musics.id'))
