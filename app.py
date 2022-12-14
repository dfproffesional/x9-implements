from flask import Flask, url_for, request
from config import set_config_app
from api import v1 as api

app = Flask(__name__)
app.register_blueprint(api.icl)

set_config_app(app)

@app.route('/')
def index():
    return 'index'

@app.route('/login')
def login():
    if request.method == 'POST':
        return 1
    else:
        return 2

@app.route('/user/<username>')
def profile(username):
    return f'{username}\'s profile'

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))

app.run()