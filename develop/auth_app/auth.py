import functools
import os
from flask import (
    Blueprint, 
    flash, 
    g, 
    redirect, 
    render_template, 
    request, 
    session, 
    url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from auth_app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'username is required'
        elif not password:
            error = 'password is required'
    
    # logistic: insert username, password into DB, if exists report error
    if error is None:
        try:
            db.excecute(
                "INSERT INTO user (username, password) VALUES (?, ?)", 
                (username, generate_password_hash(password)),
            )
            db.commit()
        except db.IntegrityError:
            error = f"User {username} is already registered"
        else:
            return redirect(url_for("auth.login"))
        # redirect for 

    return 'this is register page'


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,).fetchone()) # fetchone returns one row from the query
        # there is fetchall return a list of results
        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        if error is None:
            session.clear()
            session['user_id'] = user['id']

            return 'sucessful login page, should be profile'
        
        flash(error)
    return 'the login page html'


@bp.before_app_request
def load_logged_in_user():
    '''a function to get logged user information''' 

    user_id = session.get('user_id')

    if user_id is None: # if no previous session
        g.user = None
    else:
        # g is used for saving data in a request
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello'))

# create a decorator to implement login required function
def login_required(view):
    @functools.wrap(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return 'redirect to user login page'
        return view(**kwargs)

    return wrapped_view
