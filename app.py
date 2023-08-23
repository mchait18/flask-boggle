from flask import Flask, request, render_template, session, jsonify
from boggle import Boggle
# from flask_debugtoolbar import DebugToolbarExtension

boggle_game = Boggle()

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh so secret"
# app.debug = True

# toolbar = DebugToolbarExtension(app)

@app.route('/')
def home_page():
    """Show Boggle board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)
    return render_template('home.html', board=board,
                           highscore=highscore,
                           nplays=nplays)

@app.route('/check-word')
def check_word():
    """checks if word is valid and returns result as json string
    if ok, not-on-board, or not-word"""
    board = session['board']
    word = request.args['word']
    result = boggle_game.check_valid_word(board, word)
    return jsonify ({"result":result})

@app.route('/post-score', methods=["POST"])
def post_score():
    """ checks score and updates "nplays", 
    and recalls/replaces high score. Returns boolean whether broke record"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
    