from functools import wraps
import firebase_admin
from firebase_admin import auth, credentials
from flask import Flask, request, redirect

app = Flask(__name__)
firebase_admin.initialize_app(credentials.Certificate('gcloud.json'))


def firebase_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('authorization', None)
        if auth_header is None:
            # print('no auth token')
            return redirect('/')
        id_token = auth_header.split(' ', 1)[1]
        try:
            auth.verify_id_token(id_token)
        except BaseException:
            # print('invalid token')
            # print(e)
            return redirect('/')
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/g2p')
def grapheme_to_phoneme():
    return 'g2p'


@app.route('/uno')
def uno():
    return 'uno'


@app.route('/sudoku/<int:difficulty>')
@firebase_auth
def sudoku(difficulty):
    return "{board:[[9, , 8, 2, 1, , 6, , ],[1, 3, 4, , 9, 6, , , 2]," \
           "[2, , 7, , 5, , 1, , ],[ , 1, 3, 7, , , 9, 2, 5],[ , , 9, , 2, , 7, , ]," \
           "[ , , , 9, 3, 5, 8, , 6],[ , 2, , , , 9, 3, , 7],[ , , 1, , , , 4, 8, ]," \
           "[4, , 6, , , , , , 1]]}"


@app.route('/test')
@firebase_auth
def test():
    return 'firebase auth'
