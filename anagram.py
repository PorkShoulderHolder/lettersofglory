__author__ = 'sam.royston'
import nltk
from nltk.corpus import wordnet
import random
import config
import itertools

__words__ = nltk.corpus.words.words('en')
__anagrams__ = nltk.defaultdict(list)
for word in __words__:
    key = ''.join(sorted(word))
    __anagrams__[key].append(word)

def lemmalist(str):
    """
    get synonyms
    """
    syn_set = []
    for synset in wordnet.synsets(str):
        for item in synset.lemma_names:
            syn_set.append(item)
    return syn_set

def same_core_meaning(word_one, word_two):
    pass

def calculate_anagram(word,letters, depth = 1):
    """
    calc optimal anagram for word
    """
    solutions = []
    letter_set = letters
    subset_permutations = []
    for n in xrange(1, len(letters) + 1):
       subset_permutations.extend(itertools.combinations(letter_set,n))

    subset_permutations = sorted(subset_permutations, cmp=lambda x,y: cmp(len(y),len(x)))

    for subset in subset_permutations:
        if depth < 1:
            break
        alphabetical = []
        alphabetical[:0] = word + ''.join(subset)
        alphabetical = sorted(alphabetical)
        alphabetical = ''.join(alphabetical)
        sols = __anagrams__[alphabetical]
        solutions.extend(sols)
        if len(sols) > 0:
            depth -= 1

    return solutions

def calculate_best_word(words,letters, solution_depth = 3, stopwords = None):
    depth_cp = solution_depth
    if stopwords is None:
        stopwords = {}
    words = sorted(words, cmp=lambda x,y: cmp(len(y),len(x)))
    choices = []
    if len(words) == 0:
        words.append('')
    for word in words:
        if depth_cp == 0:
                break
        anagrams = calculate_anagram(word, letters, depth = depth_cp)
        print anagrams
        for choice in anagrams:
            if depth_cp == 0:
                break
            elif len(choice) >= config.MIN_WORD_LENGTH:
                try:
                    a = stopwords[choice]
                    pass
                except KeyError:
                    dif = letter_difference(word, choice)
                    choices.append({"new_word":choice, "old_word":word, "letters_used": dif})
                    depth_cp -= 1


    choices = sorted(choices, cmp=lambda x,y: cmp(len(y),len(x)))
    if len(choices) > solution_depth:
        return choices[0:solution_depth]
    elif len(choices) > 0:
        return choices
    return None

def letter_difference(word_one,word_two):
    arr_one = sorted(word_one)
    arr_two = sorted(word_two)
    longest = arr_one if len(arr_one) > len(arr_two) else arr_two
    shortest = arr_one if len(arr_one) <= len(arr_two) else arr_two
    diff = []
    i = 0
    j = 0
    while i < len(longest):
        if j >= len(shortest):
            diff.append(longest[i])
        elif longest[i] is not shortest[j]:
            diff.append(longest[i])
        else:
            j += 1
        i += 1

    return diff

