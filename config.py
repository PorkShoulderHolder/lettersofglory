__author__ = 'sam.royston'
import sys

REDIS_URI =  "redis://localhost:6380/0" if sys.platform == 'darwin' else "redis://localhost:6379/0"

print "REDIS_URI:" + REDIS_URI
LETTER_COUNTS = {
                    "a":5,
                    "b":2,
                    "c":4,
                    "d":4,
                    "e":12,
                    "f":4,
                    "g":2,
                    "h":5,
                    "i":5,
                    "j":1,
                    "k":1,
                    "l":5,
                    "m":4,
                    "n":5,
                    "o":6,
                    "p":3,
                    "q":1,
                    "r":5,
                    "s":5,
                    "t":7,
                    "u":4,
                    "v":2,
                    "w":3,
                    "x":1,
                    "y":3,
                    "z":1
                }
TILES = []
for key in LETTER_COUNTS.keys():
    i = LETTER_COUNTS[key]
    while i > 0:
        TILES.append(key)
        i -= 1

MIN_WORD_LENGTH = 3