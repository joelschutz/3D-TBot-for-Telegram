'''
Custom exceptions of the game
'''

class GameError(Exception):
    pass

class ItemError(GameError):
    pass

class LockedError(GameError):
    pass

class PointsError(GameError):
    pass