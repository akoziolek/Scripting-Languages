import sys
from functools import reduce
from collections import defaultdict


def make_alpha_dict(s):
    words = s.split()

    def get_letter_word_pairs(word):
        letters = set(filter(lambda x: x.isalpha(), word.lower()))
        return map(lambda letter: (letter, word), letters)

    all_pairs = reduce(
        lambda acc, word: acc + list(get_letter_word_pairs(word)),
        words,
        []
    )

    def add_to_dict(acc, pair):
        letter, word = pair
        acc[letter].append(word)
        return acc

    return dict(reduce(
        add_to_dict,
        all_pairs,
        defaultdict(list)
    ))

if __name__ == '__main__':
    print(make_alpha_dict("wineo fnw ori"))