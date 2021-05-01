from random import randrange
from storage import Storage

class StringBank:
    def __init__(self, strings: list, store: Storage = None):
        self.strings = set()
        if strings is not None:
            self.strings.update(strings)
        self.store = store

    def add(self, string: str):
        self.strings.add(string)
        if self.store is not None:
            self.store.add(string)

    def remove(self, string: str):
        self.strings.discard(string)

    def get(self, string: str = None):
        for s in self.strings:
            if s == string:
                return s

    def get_random(self):
        rand_i = randrange(0, len(self.strings))
        i = 0
        for s in self.strings:
            if i == rand_i:
                return s 
            i += 1

class Thesaurus(StringBank):
    def print_all(self):
        words = self.strings
        all_words = ''
        for w in words:
            all_words += w + '\n'
        return all_words.strip()


class Phrasebook(StringBank):
    def print_all(self):
        phrases = self.strings
        all_phrases = ''
        for p in phrases:
            all_phrases += p + '\n'
        return all_phrases.strip()

