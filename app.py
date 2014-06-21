
import manager
import brain
import json
from flask import Flask, request, render_template


app = Flask(__name__)

@app.route("/", methods=["GET"])
def main_page():
    """
    show list of games
    """
    games = manager.get_all_games()
    return render_template("index.html",item_list = games)

@app.route("/gameview", methods=["GET"])
def game_page():
    """
    show list of games
    """
    game_id = request.args.get('game_id')
    game = manager.join_game(game_id)
    print game
    return render_template("game.html",game_data = game , game_json = json.dumps(game.current_state, default=lambda o: o.__dict__))


@app.route("/api/update", methods=["GET","POST"])
def update_game_state():
    game_id = request.args.get('id')
    game = brain.get_game(game_id)
    return json.dumps(game,default=lambda o: o.__dict__)

@app.route("/api/letter", methods=["GET"])
def new_letter():
    new_letter = request.args.get('new_letter')
    game_id = request.args.get('id')
    data = manager.flip_new_letter(game_id, new_letter)
    return json.dumps(data,default=lambda o: o.__dict__)

@app.route("/api/validate", methods=["GET"])
def validate():

    letters_used = request.args.get('letters_used')
    new_word = request.args.get('new_word')
    old_word = request.args.get('old_word')
    game_id = request.args.get('id')
    print letters_used, new_word, old_word
    manager.validate_solution(game_id,new_word,old_word,letters_used)
    game = brain.get_game(game_id)
    return json.dumps(game.current_state,default=lambda o: o.__dict__)

@app.route("/api/games", methods=["GET"])
def games():

    return str(manager.get_all_games())

@app.route("/new_game", methods=["GET"])
def new_game():
    play_with_computer = bool(int(request.args.get('ai')))
    game = manager.start_new_game()
    return render_template("game.html", game_data = game , game_json = json.dumps(game.current_state, default=lambda o: o.__dict__))


@app.route("/api/join_game", methods=["GET"])
def join_game():
    name = request.args.get("name")
    game_id = request.args.get('id')
    message = manager.join_game(name, game_id)
    return message.id

@app.route("/api/word_guess", methods=["GET"])
def word_guess():
    word = request.args.get("word_guess")
    game_id = request.args.get('id')
    pass

@app.route("/api/get_game", methods=["GET"])
def get_game():
    game_id = request.args.get('id')
    game = brain.get_game(game_id)
    return json.dumps(game.current_state,default=lambda o: o.__dict__)

@app.route("/api/flip_letter", methods=["GET"])
def flip_letter():
    game_id = request.args.get('id')
    pass

if __name__ == "__main__":
    app.run(debug=True)