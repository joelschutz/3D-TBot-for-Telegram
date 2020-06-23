'''
This module defines different types of itens in the game
'''

class Item:
    @property
    def name(self):
        raise NotImplementedError

    @property
    def value(self):
        raise NotImplementedError

    def use(self):
        raise NotImplementedError


class Potion(Item):
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self): return self._name

    @property
    def value(self): return 10

class HealthPotion(Potion):

    def effect(self, character):
        character.hp = 10

class MagicPotion(Potion):

    def effect(self, character):
        character.mp = 10



