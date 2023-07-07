from DB import db
from sqlalchemy.sql import func

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_email = db.Column(db.String(50), nullable=False)
    user_name = db.Column(db.String(100))       #昵称
    password = db.Column(db.String(20))
    user_gender = db.Column(db.String(1), default="O")            #M , F or O:other 未知
    user_signature = db.Column(db.String(200), default="这家伙很懒")   #个性签名

    # vip = db.Column(db.Integer, default=0)       #vip
    # total_cost = db.Column(db.Integer, default=0)#一共冲了多少

    bill = db.relationship('Bill', backref='User')
    user_log = db.relationship('User_log', backref='User')
    recommendation = db.relationship('Recommendation', backref='User')
    collection = db.relationship("Collect", backref='User')

class Music(db.Model):
    __tablename__ = 'music'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    music_name = db.Column(db.String(50), nullable=False)
    lyric = db.Column(db.Text)
    album_name = db.Column(db.String(20))
    musician_id = db.Column(db.Integer, db.ForeignKey('music.id'))
    #vip = db.Column(db.Integer, default=0)

    user_log = db.relationship('User_log', backref='Music')
    recommendation = db.relationship('Recommendation', backref='Music')
    collection = db.relationship("Collect", backref='Music')
    tag = db.relationship("Tag", backref="Music")

class Musician(db.Model):
    __tablename__ = 'musician'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tag_name = db.Column(db.String(50), nullable=False)
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))

# class Bill(db.Model):
#     __tablename__ = 'bill'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     bill_date = db.Column(db.DateTime, default=func.now())
#     transaction_amount = db.Column(db.Integer, nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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
    '''
    o:like the music
    1:listen to that song
    3:user(id) comment that music(il')
    '''
    log_time = db.Column(db.DateTime, default=func.now())


class Recommendation(db.Model):
    __tablename__ = 'recommendation'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    music_id = db.Column(db.Integer, db.ForeignKey('music.id'))
