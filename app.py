import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response

app = Flask(__name__, static_url_path='/')
app.secret_key = b'_djflajeoflaj'


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
        username = session.get('username', None)
        #username = request.form.get('username', 'Guest')
        password = request.form.get('password', None)
        print(username)
        resp = make_response(redirect(url_for('index')))
        #if username在数据库中，登入成功
        # resp.set_cookie('username', request.form['username'])
        session['username'] = request.form['username']
        return resp
    print(request.args)
    print(request.form)
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'Error'
    return resp


@app.route('/song/id=<int:id>')
def song():
    return f'Hello {id}!'

#@app.route('/login', methods=['GET', 'POST'])
#def login():
#    if request.method == 'PODT':
#        return do_the_login()
#    else:
#        return show_the_login_form()

#@app.route('/')
#def hello_world():
#    return 'Hello <p>Flask</p>!'
#
#@app.route('/')
#def hello_world():
#    return 'Hello <p>Flask</p>!'
#@app.route('/')
#def hello_world():
#    return 'Hello <p>Flask</p>!'
#@app.route('/')
#def hello_world():
#    return 'Hello <p>Flask</p>!'
#
#




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5020')

