from flask import session, request, render_template, flash, redirect, url_for, Blueprint, g
from dr import app, db, login_manager
import ldap
from flask_login import current_user, login_user, logout_user, login_required
from dr.auth.models import User, LoginForm


auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@auth.before_request
def get_current_user():
    g.user = current_user


@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login',  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.')
        return render_template('user.html')

    form = LoginForm(request.form)

    if request.method == 'POST' and form.validate():
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            User.try_login(username, password)
        except ldap.INVALID_CREDENTIALS:
            flash(
                'Invalid username or password. Please try again.',
                'danger')
            return render_template('user.html', form=form)

        user = User.query.filter_by(username=username).first()

        if not user:
            user = User(username, password)
            db.session.add(user)
            db.session.commit()
        login_user(user)
        flash('You have successfully logged in.', 'success')
        return redirect(url_for('index'))

    if form.errors:
        flash(form.errors, 'danger')
    return render_template('user.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')



