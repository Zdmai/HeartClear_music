#encoding: utf-8
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response
from DB import db, query
from model.entity import *
from service.service import *
import pandas as pd
from ItemCF import recommend_music
import random



app = Flask(__name__, static_url_path='/')
app.secret_key = b'_djflajeoflaj'
app.config.from_pyfile('config.py')


db.app = app
db.init_app(app=app)


@app.route('/add/<id>')
def add_music(id):
    user_id = session.get('user_id')
    if user_id:
        CollectService.add_music(user_id=user_id, music_id=id)
        print('add succeed')
        return redirect(url_for('song', id=id))
    else:
        return redirect(url_for('login'))
    return redirect(url_for('song', id=id))




@app.route('/profile')
def profile():
    name = session.get('username')
    return render_template('profile.html', name=name)



@app.route('/search/<text>')
def search(text):
    user_id = session.get('user_id')
    one = UserService.get_user_by_id(user_id)
    musics = MusicService.get_music_by_name(text)
    u = MusicianService.get_musician_id_by_name(text)
    musics += MusicService.get_music_by_musician_id(u)
    print('\n========================\n', u)
    many = []
    for i in musics:
        many += [MusicService.get_all_by_id(i.id)]
        print(many)
    return render_template('search.html', musics=many, user=one)


@app.route('/user/show/<id>')
def user(id):
    one = UserService.get_user_by_id(id)
    return render_template('person_show.html', user=one)


@app.route('/user/modify/<id>')
def modify(id):
    one = UserService.get_user_by_id(id)
    if request.method == "POST":
        sex = request.form.get('sex')
        name = request.form.get('username')
        sign = request.form.get('user_signature')
        picture = request.files.get('picture')
        picture.save('../static/img/user/' + one.id + '.jpg')
        print(type(picture), '---------here----------', picture)
        UserService.user_modify(id, sex, name, sign, picture)
        return redirect(url_for('uer_home', id=id))
    return render_template('user_modify.html', user=one)


@app.route('/user/home/<id>')
def user_home(id):
    one = UserService.get_user_by_id(id)
    musics = CollectService.get_collection_by_userid(id)
    return render_template('person_home.html', user=one, musics=musics)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    user_id = session.get('user_id')
    one = UserService.get_user_by_id(user_id)
    collection = CollectService.get_collection_by_userid(user_id)
    print('\\\\\\\\\\\\\\\\\\\\\\', collection)
    search = request.args.get('search')
    if search:
        return redirect(url_for('search', text=search))

    id = user_id
    N = 5
    recoms = recommend_music()
    if id not in recoms.keys():
        id=list(recoms.keys())[0]
    li = recoms.get(id)
    len_li = len(li)
    if len_li < 10:
        print("/////////////////", li)
        recoms = list(recoms.get(id)) + random.choices(MusicService.get_all(), k = N - len_li)
    else:
        recoms = li
    print('!!!!!!!!!!!!!!!!!!!!!!!!!', recoms)
    lst = []
    for i in recoms:
        if isinstance(i, int):
            lst += [MusicService.get_music_by_id(i)]
        else:
            lst += [MusicService.get_music_by_id(i[0])]
    print(lst)
    return render_template('index.html', user=one, collection=collection, li=lst)



@app.route('/sign_up', methods=["GET", "POST"])
def sign_up():
    if request.method =='POST':
        useremail = request.form.get('useremail', 'Guest@mail.com')
        password = request.form.get('passward')
        username = request.form.get('username')
        one = UserService.get_user_by_email(useremail)
        if one:
            flash("This email have signed up!")
            return redirect(url_for("login"))
        elif useremail != "Guest@mail.com" and password != '':
            user = User(user_email=useremail, user_name=username, password=password)
            db.session.add(user)
            db.session.commit()
            session['user_id'] = UserService.get_user_id_by_email(useremail).id
            print(session.get('user_id'))
            return redirect(url_for('index'))
        else:
            return redirect(url_for('sign_up'))
    return render_template('sign_up.html')


#用户登录逻辑
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        useremail = request.form.get('useremail')
        password = request.form.get('password')
        user = UserService.get_user_by_email(useremail)
        if user:
            if user.password == password:
                flash('Welcome to HeartClearMusic!')
            else:
                flash('Password error!')
                return redirect(url_for('login'))
        else:
            flash('There is something error! Please sign up first')
            return redirect(url_for('sign_up'))
        #if username在数据库中，登入成功
        # resp.set_cookie('username', request.form['username'])
        session['user_id'] = user.id
        return redirect((url_for('index')))
    print(request.args)
    print(request.form)
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    flash("Logout succeed!")
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'Error'
    return resp


@app.route('/recommend/<id>', methods=["GET", "POST"])
def recommend(id):
    N = 20
    one = UserService.get_user_by_id(id)
    recoms = recommend_music()
    if id not in recoms.keys():
        id=list(recoms.keys())[0]
    li = recoms.get(id)
    len_li = len(li)
    if len_li < 10:
        print("/////////////////", li)
        recoms = list(recoms.get(id)) + random.choices(MusicService.get_all(), k = N - len_li)
    else:
        recoms = li
    print('!!!!!!!!!!!!!!!!!!!!!!!!!', recoms)
    lst = []
    for i in recoms:
        if isinstance(i, int):
            lst += [MusicService.get_music_by_id(i)]
        else:
            lst += [MusicService.get_music_by_id(i[0])]
    search = request.args.get('search')
    search = request.args.get('search')
    if search:
        return redirect(url_for('search', text=search))
    return render_template('album.html', user=one, li=lst)


@app.route('/song/<id>', methods=['GET', 'POST'])
def song(id):
    one = UserService.get_user_by_id(session.get('user_id'))
    music = MusicService.get_all_by_id(id)
    print(music)
    if request.method=="POST":
        print("add")
    search = request.args.get('search')
    search = request.args.get('search')
    if search:
        return redirect(url_for('search', text=search))
    return render_template('detail.html', user=one, music=music)

# @app.route('/album_list')
# def album_list():
#
#     return render_template('album_list.html', user=user)

# @app.route('/album/<name>')
# def album(name):
#     musics = MusicService.get_music_by_albmu_name(name)
#     return render_template('album_detail.html', user=user, musics=musics)

@app.route('/user/forget')
def forget():
    if request.method == 'POST':
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(password2, password1)
        if password1 != password2:
            flash("密码不一致")
            return render_template('forget.html')
        else:
            id = session.get('user_id')
            one = UserService.get_user_by_id(id)
            one.password = password1
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("forget.html")


@app.route('/succeed')
def succeed():
    return "Succeed!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5020')















#------------------------------------------

# @app.cli.command()
# def importdata():
#     a = pd.read_csv('./musician.csv', delimiter=';')
#     for i in range(len(a['musician_name'])):
#         musician = Musician(id = a['musician_id'][i], name=a['musician_name'][i])
#         db.session.add(musician)
#         db.session.commit()
# @app.cli.command()
# def importdata1():
#     a = pd.read_csv('./tag.csv')

@app.cli.command()
def collect():
    li = ['63570', '66823', '365661004', '108795', '165339', '186421']
    for i in li:
        col = Collect()
        print(i)
        col.user_id = 1
        col.music_id = i
        db.session.add(col)
        db.session.commit()

@app.cli.command()
def create1():
    user = User()
    user.user_email = "test@qq.com"
    user.user_gender = "M"
    user.password = '12345'
    user.id = 1
    user.user_name = 'test'
    db.session.add(user)
    db.session.commit()


@app.cli.command()
def create():

    musician = Musician()
    musician.id = 1
    musician.name = "许嵩"
    db.session.add(musician)
    db.session.commit()
    # bill = Bill()
    # bill.id = 1
    # bill.bill_date = "2023.2.23"
    # bill.transaction_amount = 30
    # bill.user_id = 1
    # db.session.add(bill)

    music = Music()
    music.music_name = "许嵩"
    music.lyric = '''
    djlfj
    浪费空间扫放假啊开始减肥了卡睡觉了
    【撒‘姜i家啊大家
    啊好’姜阿水；姜安静；姜
    安静安静k啊‘阿萨德看啊jasj'asokas’hands
    a
     '''
    music.album_name = "卡拉芭比大海"
    music.picture = '/img/music/xr.jpg'
    music.musician_id = 1
    db.session.add(music)
    music=Music()
    music.music_name = "许江东父老就阿拉丁"
    music.lyric = '''
    啊好 姜阿水；姜安静；姜
    安静安静k啊‘阿萨德看啊 hands
     '''
    music.album_name = "大海"
    music.vip = 9
    music.picture = '/img/music/xr.jpg'
    music.musician_id = 1
    db.session.add(music)


    collect = Collect()
    collect.id = 2
    collect.song_list_name = "我的最爱"
    collect.music_id = 1
    collect.user_id = 1
    db.session.add(collect)
    db.session.commit()


@app.cli.command()
def dfg():
    tag = Tag()
    tag.music_id = 1
    tag.tag_name = "青春"
    db.session.add(tag)

    recommendation = Recommendation()
    recommendation.music_id = 1
    recommendation.user_id = 1
    db.session.add(recommendation)

    comment = Comment()
    comment.id = 1
    comment.user_id = 1
    comment.music_id = 1
    comment.content = "夜空中最亮的星！"
    comment.comment_date = "2020.2.20"
    db.session.add(comment)

    user_log = User_log()
    user_log.id = 1
    user_log.user_id = 1
    user_log.music_id = 1
    user_log.command_type = 1
    user_log.log_time = "2023.2.23"
    db.session.add(user_log)

    db.session.commit()



@app.cli.command()
def createdata():
    db.drop_all()
    db.create_all()

@app.cli.command()
def insdb():
    user=User()
    user.user_email = "zzz@qq.com"
    user.user_name = user.user_email.split("@")[0]
    user.gender = "M"
    user.user_picture = "./static/img/happydog.jpg"
    user.password = 'zzz'
    db.session.add(user)
    db.session.commit()



#------------------------------------------
