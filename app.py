from functools import wraps
import firebase_admin
from firebase_admin import auth, credentials
from flask import Flask, request, redirect, jsonify, after_this_request
from static.Sudoku.Generator import Generator
import queue
import threading

app = Flask(__name__)
firebase_admin.initialize_app(credentials.Certificate('gcloud.json'))


def makeBoard(difficulty):
    with app.app_context():
        difficulties = {
            'Easy': (35, 0),
            'Medium': (81, 5),
            'Hard': (81, 10),
            'Extreme': (81, 15)
        }
        gen = Generator()
        gen.randomize(100)
        pair = difficulties[difficulty]
        gen.reduce_via_logical(pair[0])
        if pair[1] != 0:
            gen.reduce_via_random(pair[1])
        final = gen.board.copy()
        sudoku_boards[difficulty].put(jsonify(final.stringify()))


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


@app.route('/sudoku', methods=['POST'])
# @firebase_auth
def sudoku():
    @after_this_request
    def after_request(response):
        thread = threading.Thread(target=makeBoard, args=(arg,))
        thread.start()
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    arg = request.args.get('difficulty')
    board = sudoku_boards[arg].get()
    return board


@app.route('/test')
@firebase_auth
def test():
    return 'firebase auth'


sudoku_boards = {}
for difficulty in ('Easy', 'Medium', 'Hard', 'Extreme'):
    sudoku_boards[difficulty] = queue.LifoQueue()
for key in sudoku_boards:
    for i in range(2):  # change number to change number of boards to store
        makeBoard(key)
        print("Generated board " + str(i) + " for " + key)
