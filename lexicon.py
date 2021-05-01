from random import randrange
from storage import Storage

#
# StringBank stores a set of strings in-memory. It allows
# basic CRUD operations on that set, as well as a method
# to get a random string from the set. It optionally takes
# a store argument for persisting added strings.
#
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
    def to_embed_dict(self):
        words = self.strings
        words_dict = {
            'title': 'Patronizing words',
            'description': ''
        }
        i = 0
        for w in words:
            words_dict['description'] += f'**{i + 1}.** {w}\n'
            i += 1
        return words_dict


class Phrasebook(StringBank):
    def to_embed_dict(self):
        phrases = self.strings
        phrases_dict = {
            'title': 'Patronizing phrases',
            'description': ''
        }
        i = 0
        for p in phrases:
            phrases_dict['description'] += f'**{i + 1}.** {p}\n'
            i += 1
        return phrases_dict

