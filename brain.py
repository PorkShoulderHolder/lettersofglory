__author__ = 'sam.royston'
from gamestates import *
import redis
import pickle

client = redis.StrictRedis.from_url(config.REDIS_URI)

def process_gamestate(state):
    assert state.__class__ == State

def set_new_game(ai, state = None, expiry = 3600):
    if state is not None:
        game = Game(ai, state, expiry)
    else:
        game = Game(ai)
    set_game(game)
    return game

def set_game(game):
    pickled_game = pickle.dumps(game)
    key = make_game_key(game.id)
    client.set(key, pickled_game)
    client.expire(key, game.expiry)

def get_all_games():
    """
    """
    keys = client.keys("*")
    games = []
    for key in keys:
        game = get_game(get_id_string(key))
        games.append(game)
    return games

def make_game_key(id):
    return "game:" + id

def get_id_string(key):
    return key[5:]

def get_game(id):
    """
    get game from database based on id key
    """
    game = None
    key = make_game_key(id)
    pickled_game = client.get(key)
    if pickled_game:
        game = pickle.loads(pickled_game)
        client.set(key, pickled_game)
        client.expire(key, game.expiry)

    return game

    pass


