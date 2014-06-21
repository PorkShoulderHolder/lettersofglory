__author__ = 'sam.royston'
from redis import client
import brain
import anagram
from gamestates import *
from textblob import Word

def flip_new_letter(game_id, letter = None):
    """
    handle retrieving the game and updating the game state as we calculate the best word
    """
    print game_id
    game = brain.get_game(str(game_id))

    if game is None:
        return "GAME_NOT_FOUND"
    game.flip_letter(letter)

    new_data = anagram.calculate_best_word(game.current_state.words,game.current_state.exposed_letters)
    options = []
    if new_data is not None:
        for option in new_data:
            if option is not None and len(option["new_word"]) >= config.MIN_WORD_LENGTH:
                option["definition"] = str(Word(option["new_word"]).definitions)
                options.append(option)

    brain.set_game(game)
    if new_data is None:
        return "no new words found"
    else:
        return options

def add_word_for_state(state,word):
    state.add_word(word)

def flip_letter_for_state(state,letter):
    """
    to beat the girls at snatch
    """
    new_data = anagram.calculate_best_word(state.words, state.exposed_letters)
    options = []
    if new_data is not None:
        for option in new_data:
            if option is not None and len(option["new_word"]) >= config.MIN_WORD_LENGTH:
                option["definition"] = str(Word(option["new_word"]).definitions)
                options.append(option)

    if new_data is None:
        return "no new words found"
    else:
        return options


def validate_solution(game_id,new_word,old_word,letters_used,player = None):
    game = brain.get_game(str(game_id))
    if game is None:
        return "GAME_NOT_FOUND"
    elif old_word in game.current_state.words:
        game.current_state.update_after_snatch(new_word, old_word, letters_used)
        brain.set_game(game)
        return True
    return False


def validate_solution_for_state(state,new_word,old_word,letters_used,player = None):
    if old_word in state.words:
        state.update_after_snatch(new_word, old_word, letters_used)
        return True
    return False


def get_all_games():
    """
    return all active games
    """
    games = brain.get_all_games()
    return games


def start_new_game():
    game = brain.set_new_game()
    return game

def join_game(game_id, name = "anon"):
    game = brain.get_game(game_id)
    names = [player.name for player in game.players]
    player_number = 0
    while name in names:
        player_number += 1
        name += str(player_number)
    new_player = Player(name)
    game.players.append(new_player)
    brain.set_game(game)
    return game
