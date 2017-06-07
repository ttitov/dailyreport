from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)

POSTGRES = {
    'user': 'dr',
    'pw': 'Valadorus',
    'db': 'dailyreport',
    'host': 'localhost',
    'port': '5432',
}

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
app.config['WTF_CSRF_SECRET_KEY'] = 'random key for form'
app.config['LDAP_PROVIDER_URL'] = 'ldap://ds02.valadorus-soft.com:389/'
app.config['LDAP_PROTOCOL_VERSION'] = 3
db = SQLAlchemy(app)

app.secret_key = 'some_random_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from dr.dailyreport import auth
app.register_blueprint(auth)

db.create_all()
