from flask import session, redirect, url_for, escape, request, render_template
from dr import app


@app.route('/')
def index():
    if 'username' in session:
        return 'Logged in as %s <p><input type=submit value=Logout>' % escape(session['username'])

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('login'))
    return render_template('user.html')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'



