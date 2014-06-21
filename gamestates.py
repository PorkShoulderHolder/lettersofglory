__author__ = 'sam.royston'
import config
import random
import uuid
from manager import *

class Player(object):
    def __init__(self,name = "no_name"):
        self.name = name
        self.words = []

    def calculate_score(self):
        """
        get the player's current score
        """
        score = 0
        for word in self.words:
            score += len(word) - 2
        return score

class Game(object):
    def __init__(self, expiry = 3600, initial_state = None, players = []):
        self.states = []
        self.expiry = expiry
        if initial_state is not None:
            self.current_state = initial_state
            self.players = initial_state.players
        else:
            self.current_state = State()
            self.players = players
        self.id = self.current_state.id
        self.states.append(self.current_state)

    def flip_letter(self,letter):
        self.current_state.flip_letter(letter)
        self.states.append(self.current_state)

    def unflip_letter(self,letter):
        self.current_state.unflip_letter(letter)
        self.states.append(self.current_state)

    def get_leader(self):
        top_player = Player()
        for player in self.players:
            if top_player.calculate_score() < player.calculate_score():
                top_player = player
        return top_player

class State(object):
    def __init__(self, players = [], exposed_letters = [], hidden_letters = config.TILES, ai = True):
        players.append(Player("snatcher"))
        self.players_dict = {}
        self.id = str(uuid.uuid4())[:8]
        self.hidden_letters = hidden_letters
        self.exposed_letters = exposed_letters
        self.words = [""]
        for player in players:
            self.players_dict[player.name] = player
            for word in player.words:
                self.words.append(word)

    def add_word(self, word):
        for letter in word:
            self.flip_letter(letter)
        self.update_after_snatch(word,'',word.split())



    def update_after_snatch(self, new_word, old_word, letters_used, player = None):
        """
        when a player finds a new word, update the state of the game
        """
        for letter in letters_used:
            if letter in self.exposed_letters:
                self.exposed_letters.remove(letter)
        if old_word != '':
            self.words.remove(old_word)
        self.words.append(new_word)



    def flip_letter(self, letter_to_flip = None):
        """
        flip a random letter
        """
        letter_to_flip = str(letter_to_flip)
        if letter_to_flip is None:
            letter_to_flip = random.choice(self.hidden_letters)
            self.hidden_letters.remove(letter_to_flip)
        elif letter_to_flip not in self.hidden_letters:
            print "WARNING: I think that you didn't count your tiles right..."
        else:
            self.hidden_letters.remove(letter_to_flip)
        self.exposed_letters.append(letter_to_flip)

    def unflip_letter(self, letter_to_unflip):
        """
        turn an exposed letter back over
        """
        letter_to_unflip = str(letter_to_unflip)
        if letter_to_unflip in self.exposed_letters:
            self.exposed_letters.remove(letter_to_unflip)
            self.hidden_letters.append(letter_to_unflip)





