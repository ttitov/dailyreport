from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'This is daily report page.'


@app.route('/user/<username>')
def user_private_page(username):
    return 'Add your daily report, %s!' % username


if __name__ == '__main__':
    app.run()
