from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User
from datetime import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [ # Fake posts array
            {
                'author': {'nickname': 'John'},
                'body': 'Beautiful day in Chi Town!'
            },
            {
                'author': {'nickname': 'Susan'},
                'body': 'The new Star Wars movie was cool!'
            },
            {
                'author': {'nickname': 'Larry'},
                'body': '''Lorem ipsum dolor sit amet, consectetur adipisicing
                elit, sed do eiusmod tempor incididunt ut labore et dolore magna
                 aliqua. Ut enim ad minim veniam, quis nostrud exercitation
                 ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis
                 aute irure dolor in reprehenderit in voluptate velit esse
                 cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat
                  cupidatat non proident, sunt in culpa qui officia deserunt
                  mollit anim id est laborum.'''
            }
            ]
    return render_template('index.html',
                            title='Home',
                            user=user,
                            posts=posts)


@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                            title='Sign In',
                            form=form,
                            providers=app.config['OPENID_PROVIDERS'])


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or resp.nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated:
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post 1'},
        {'author': user, 'body': 'Test post 2'}
    ]
    return render_template('user.html',
                            user=user,
                            posts=posts)
