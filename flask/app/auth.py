from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
import functools

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif User.query.filter_by(username=username).first():
            error = f"User {username} is already registered."

        if error is None:
            # Simpan password hash biar aman
            new_user = User(
                username=username,
                password=generate_password_hash(password)
            )
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful! You can now log in.')
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            user = User.query.filter_by(username=username).first()
            if user is None or not check_password_hash(user.password, password):
                error = 'Incorrect username or password.'

        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('blog.index'))

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

def login_required(view):
    """Decorator to ensure user is logged in."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash('You need to be logged in to access this page.')
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
