'''
This module has all the mechanics of the game
'''
from exceptions import ItemError, LockedError, PointsError
from collections import Counter
import character, meta, itens

class CharHandler:
   pass


#This is class is used to store itens. Every item is a key in a dict where the value is the amount
#  of identical itens in the inventory. It uses the '+' and '-' operators to add or remove itens from
#  storage. Can accept the 'in' comparator and can be iterated.
class Inventory:
    def __init__(self):
        self._itens = []

    #Uses the '+' operator to add itens, if it is already there, it increments the amount 
    def __add__(self, item):
        if isinstance(item, itens.Item): self._itens.append(item)  
        else: raise ItemError(f'{item} is not a Item')

    #Uses the '-' operator to remove itens, if it does not exist, it raises a custom ItemError
    def __sub__(self, item):
        if item in self._itens: self._itens.remove(item)  
        else: 
            if isinstance(item, itens.Item): raise ItemError('Item not in inventory')
            else: raise ItemError(f'{item} is not a Item')

    #Uses a 'in' comparator to verify the presence of an item
    def __contains__(self, item):
        return True if item in self._itens else False
    
    #Allow the iteration of the itens in the inventory
    def __iter__(self):
        yield from self._itens

    def __str__(self):
        return str(dict(Counter(self._itens)))

class Chest(Inventory):
    def __init__(self):
        super.__init__(self)
        self._locked = False

    def open(self):
        if not self._locked: return self._itens
        else: raise LockedError('This chest is locked')
    
    def lock_unlock(self):
        self._locked = not self._locked

    



    

