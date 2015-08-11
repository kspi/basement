import re


VOWELS = frozenset("aoeiu")

def starts_with_vowel(word):
    # TODO: smarter pronounciation handling
    return word[0] in VOWELS


def add_article(word):
    return ("an " if starts_with_vowel(word) else "a ") + word


def camelcase_to_words(s):
    return re.sub(r"([A-Z])", r" \1", s).strip().lower()


class Object:
    symbol = '?'

    @property
    def name(self):
        return add_article(camelcase_to_words(self.__class__.__name__))
