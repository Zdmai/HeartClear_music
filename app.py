import sqlite3
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


@app.cli.command()
def createdata():
    db.drop_all()
    db.create_all()

@app.cli.command()
def insdb():
    user=User()
    user.user_email = "2580324258@qq.com"
    user.gender = "M"
    user.user_picture = "./static/img/happydog.jpg"
    user.password = '12345'
    user.id = 0
    db.session.add(user)
    db.session.commit()


@app.route('/profile')
def profile():
    name = session.get('username')
    return render_template('profile.html', name=name)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    username = session.get('username', "guest")
    if username != 'guest':
        username = username.split('@')[0]
    return render_template('index.html')

@app.route('/user')
def user():
    return render_template('user.html')


#用户登录逻辑
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', None)
        #username = request.form.get('username', 'Guest')
        password = request.form.get('password', None)
        print(username)
        if query(User).filter('user_email').first:
            flash('Yes!')
        else:
            flash('NO!')
        resp = make_response(redirect(url_for('index')))
        #if username在数据库中，登入成功
        # resp.set_cookie('username', request.form['username'])
        session['username'] = request.form['username']
        return resp
    ser = UserService()
    print(ser.get_all_user())
    print(request.args)
    print(request.form)
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session['user_name'] = None
    flash("Logout succeed!")
    return render_template('logout.html')

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'Error'
    return resp


@app.route('/song/id=<int:id>')
def song():
    return f'Hello {id}!'






if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5020')

