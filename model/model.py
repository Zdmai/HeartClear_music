from DB import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(50), nullable=False)
    password=db.Column(db.String(20))
    user_picture = db.Column(db.String(30))
    user_gender = db.Column(db.String(1))
    vip = db.Column(db.Integer, default=0)
    total_cost = db.Column(db.Integer, default=0)

    bill = db.relationship('Bill', backref='User')
    user_log = db.relationship('User_log', backref='User')
    recommendation = db.relationship('Recommendation', backref='User')
    collection = db.relationship("Collect", backref='User')

class Music(db.Model):
    __tablename__ = 'music'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    music_name = db.Column(db.String(50), nullable=False)
    music_picture = db.Column(db.String(30))
    lyric = db.Column(db.Text)
    album_name = db.Column(db.String(20))
    musician_id = db.Column(db.Integer, db.ForeignKey('music.id'))

    user_log = db.relationship('User_log', backref='Music')
    recommendation = db.relationship('Recommendation', backref='Music')
    collection = db.relationship("Collect", backref='Music')

class Musician(db.Model):
    __tablename__ = 'musician'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    music_name = db.Column(db.String(50), nullable=False)
    music_picture = db.Column(db.String(30))

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(50), nullable=False)

class Bill(db.Model):
    __tablename__ = 'bill'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    bill_date = db.Column(db.DateTime, default=func.now())
    transaction_amount = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
    content = db.Column(db.Text)
    comment_date = db.Column(db.DateTime, default=func.mow())

class Collect(db.Model):
    __tablename__ = 'collect'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    song_list_name = db.Column(db.String(30), nullable=True)

class User_log(db.Model):
    __tablename__ = 'user_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
    command_type = db.Column(db.Integer)
    log_time = db.Column(db.DateTime, default=func.now())


class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
