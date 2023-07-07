#encoding: utf-8
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response
from DB import db, query
from model.entity import *
from service.service import *


app = Flask(__name__, static_url_path='/')
app.secret_key = b'_djflajeoflaj'
app.config.from_pyfile('config.py')

db.app = app
db.init_app(app=app)





@app.route('/profile')
def profile():
    name = session.get('username')
    return render_template('profile.html', name=name)



@app.route('/search/<text>')
def search(text):
    musics = MusicService.get_music_by_name(text)
    user_id = session.get('user_id')
    one = UserService.get_user_by_id(user_id)
    musics += MusicService.get_music_by_musician_id(MusicianService.get_musician_id_by_name(text))
    return render_template('search.html', musics=musics, user=one)


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
        sign = request.fotm.get('user_signature')
        picture = request.form.get('picture')
        print(type(picture), '---------here----------', picture)
        UserService.user_modify(id, sex, name, sign, picture)
        return redirect(url_for('uer_home', id=id))
    return render_template('user_modify.html', user=one)


@app.route('/user/home/<id>')
def user_home(id):
    one = UserService.get_user_by_id(id)
    return render_template('person_home.html', user=one)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #session['user_id'] = 5
    user_id = session.get('user_id')
    one = UserService.get_user_by_id(user_id)
    search = request.args.get('search')
    if search:
        return redirect(url_for('search', text=search))
    print(search)
    return render_template('index.html', user=one)



@app.route('/sign_up')
def sign_up():
    useremail = request.form.get('useremail', 'Guest@mail.com')
    # if '@' not in useremail:
    #     return sign_up()
    password = request.form.get('passward')
    one = UserService.get_user_by_email(useremail)
    if one:
        flash("This email have signed up!")
    else:
        user = User(user_email=useremail, user_name=useremail.split('@')[0], password=password)
        print(user)
        db.session.add(user)
        db.session.commit()
        session['user_id'] = UserService.get_user_id_by_email(useremail)
        return redirect(url_for('index'))
    return render_template('sign_up.html')


#用户登录逻辑
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        useremail = request.form.get('useremail', 'Guest')
        password = request.form.get('password', None)
        user = UserService.get_user_id_by_email(useremail)
        if user:
            flash('Welcome to HeartClearMusic!')
        else:
            flash('There is something error!')
            return redirect(url_for('sign_up'))
        #if username在数据库中，登入成功
        # resp.set_cookie('username', request.form['username'])
        session['useremail'] = useremail
        session['id'] = user.id
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


@app.route('/song/<id>')
def song(id):
    music = MusicService.get_music_by_id(id)
    return render_template('detail.html', music=music)


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
            return redirect(url_for(index))
    return render_template("forget.html")


@app.route('/succeed')
def succeed():
    return "Succeed!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5020')















#------------------------------------------

# @app.cli.command()
# def modify():
#     id = '2'
#     one = UserService.get_user_by_id(id)
#     one.user_picture = '../static/img/2.jpg'
#     UserService.user_modify(one)

@app.cli.command()
def create1():
    user = User()
    user.user_email = "test@qq.com"
    user.user_gender = "M"
    user.user_picture = "./img/user/happy_dog.jpg"
    user.password = '12345'
    user.id = 1
    db.session.add(user)
    db.session.commit()


@app.cli.command()
def create():

    # bill = Bill()
    # bill.id = 1
    # bill.bill_date = "2023.2.23"
    # bill.transaction_amount = 30
    # bill.user_id = 1
    # db.session.add(bill)

    music = Music()
    music.id = 1
    music.music_name = "许嵩"
    music.lyric = "巴拉巴拉巴拉"
    music.album_name = "卡拉芭比大海"
    music.vip = 9
    music.musician_id = 1
    db.session.add(music)

    musician = Musician()
    musician.id = 1
    musician.name = "许嵩"
    db.session.add(musician)

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



@app.cli.command()
def get():
    print(UserService.get_user_by_id('1').user_email)


@app.cli.command()
def zx():
    print(UserService.get_user_by_id('1').password)


@app.cli.command()
def cv():
    print(UserService.get_user_by_id('1').user_picture)


@app.cli.command()
def cxk():
    print(UserService.get_user_by_id('1').user_gender)


@app.cli.command()
def cll():
    print(UserService.get_user_by_id('1').user_signature)


@app.cli.command()
def fcc():
    print(UserService.get_user_by_id('1').vip)


@app.cli.command()
def ycj():
    print(UserService.get_user_by_id('1').total_cost)


# @app.cli.command()
# def bill():
#     print(BillService.get_bills(id='1')[0].transaction_amount)
#

# @app.cli.command()
# def bill1():
#     print(BillService.get_bills(id='1')[0].user_id)
#
#
# @app.cli.command()
# def bill2():
#     print(BillService.get_bills(id='1')[0].bill_date)
#

@app.cli.command()
def zzx1():
    print(MusicService.get_music_by_id(1).album_name)


@app.cli.command()
def zzx2():
    print(MusicService.get_music_by_id(1).music_name)


@app.cli.command()
def zzx3():
    print(MusicService.get_music_by_id(1).music_name)


@app.cli.command()
def zzx4():
    print(MusicService.get_music_by_id(1).lyric)


@app.cli.command()
def zzx5():
    print(MusicService.get_music_by_id(1).vip)


@app.cli.command()
def zzx6():
    print(MusicService.get_music_by_id(1).musician_id)


@app.cli.command()
def zzz1():
    print(MusicianService.get_musician_by_id('1')[0].name)


@app.cli.command()
def yyy1():
    print(TagService.get_music_tag('1')[0].tag_name)



#------------------------------------------