from functools import wraps
import json
import os
import random

import firebase_admin
from firebase_admin import auth, credentials
from flask import Flask, request, redirect, jsonify

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
    if difficulty < 1 or difficulty > 5:
        return jsonify({
            'status': 'error',
            'message': 'invalid difficulty'
        })

    level = ['easy', 'medium', 'hard', 'harder', 'hardest'][difficulty - 1]
    board_dir = os.path.join('static', 'sudoku_boards', level)

    choice = random.randint(1, len(os.listdir(board_dir)))

    with open(os.path.join(board_dir, f'{choice}.json')) as open_file:
        return jsonify(json.load(open_file))


@app.route('/test')
@firebase_auth
def test():
    return 'firebase auth'
