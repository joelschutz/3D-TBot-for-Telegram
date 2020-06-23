'''
This script contains the classes of characters
'''
import inspect
from game.scripts.exceptions import CharAttributeError, ItemError, PointsError, SkillError

import game.scripts.meta as mt
from game.scripts.mechanics import CharHandler, Inventory


#Character class is used as a template for more especific classes os characters
class Character:
    def __init__(self, name, race, level):
        #Character data
        #All the data is strored as a index, the names of races and professions are stored in a
        # separet file. The value '-1' indicates that the character was iniated but the 'create'
        # funcion was not called yet. 
        self._name = name
        self._exp = level * 100
        self._points = self.level * 10
        self._profession = 0

        #Attributes of the character
        self._attributes = {'Strength':0,
                            'Dexterity':0,
                            'Resistence':0,
                            'Intelligence':0,
                            'Agility':0,
                            'Charisma':0}
        self._skills = []

        #HP and MP
        self._hp_base = self._calc_hp(self._attributes['Resistence'])
        self._hp_state = self._hp_base
        self._mp_base = self._calc_mp(self._attributes['Intelligence'])
        self._mp_state = self._mp_base

        #Additional information of the Character
        self.race = race
        self._inventory = Inventory()
        self.history = ''

    @property
    def name(self): return self._name

    @property
    def points(self): return self._points

    @points.setter
    def points(self, value):
        if self._have_points(value): self._points = value
        else: raise PointsError('Points can not be less than 0')
    
    def _have_points(self, value):
        if self._points - value >= 0: True
        else: False

    @property
    def level(self): return int(self._exp / 100)

    @property
    def exp(self): return self._exp

    def gain_exp(self, exp): self._exp += exp

    @property
    def race(self): return mt.acessdata('races','name', self._race)

    #Modifies de Character Attibutes based on its race. 
    # '0' is the humam race with no modifiers.
    @race.setter
    def race(self, race):
        if race == 0: self._race = 0
        else:
            self._race = race
            self._points -= int(mt.acessdata('races','cost', race))
            race_skills = mt.acessdata('races','skills', race)
            race_skills = race_skills.split(';')
            self.give_skills(*race_skills)
            race_modifiers = mt.acessdata('races','Modifiers', race)
            race_modifiers = mt.parse_modifiers(race_modifiers)
            self.give_attributes(**race_modifiers)

    @property
    def profession(self): return mt.acessdata('profession','name', self._profession)

    @property
    def attributes(self): return self._attributes

    @attributes.setter
    def attributes(self, attribute):
        try: self._attributes[attribute[0].capitalize()] += attribute[1]
        except KeyError: raise CharAttributeError(f'{attribute[0]} is not a valid attribute')
        except TypeError: raise CharAttributeError(f'{attribute[0].captalize()} value must be a "int"')
        except AttributeError: raise CharAttributeError(f'{attribute[0]} must be a "str"')

    def buy_attributes(self, **kwargs):
            for key, value in kwargs.items():
                if self._have_points(value):
                    self.attributes = (key, value)
                    self.points -=  value
                else: raise PointsError('Do not have enough points')

    def give_attributes(self, **kwargs):
        for key, value in kwargs.items():
            try: self.attributes = (key, value)
            except CharAttributeError: pass

    @property
    def hp(self): return (self._hp_base, self._hp_state)

    @hp.setter
    def hp(self, value):
        self._hp_state += value

    @staticmethod
    def _calc_hp(resistance): return resistance * 5
    
    @property
    def mp(self): return (self._mp_base, self._mp_state)

    @mp.setter
    def mp(self, value):
        self._mp_state += value

    @staticmethod
    def _calc_mp(intelligence): return intelligence * 5

    @property
    def skills(self):
        list = []
        for skill in self._skills:
            list.append(mt.acessdata('skills', 'name', skill))
        return list
    
    @skills.setter
    def skills(self, skill):
        try: 
            skill = int(skill)
            if skill > 0:
                self._skills.append(skill)
            else:
                raise SkillError('This skill do not exist')
        except ValueError: raise SkillError('Characteistic must be a "int"')
    
    def buy_skills(self, *args):
        for skill in args:
            cost = int(mt.acessdata('skills', 'cost', skill))
            if self._have_points(cost):
                self.points -= cost
                self.skills = skill
            else: raise PointsError('Character do not have enough points')
    
    def give_skills(self, *args):
        for skill in args:
            try: self.skills = skill
            except SkillError: pass

    def use(self, item, target=None):
        if not target:
            target = self
        item.effect(target)

    def __str__(self):
        return inspect.cleandoc(f'''
        Name: {self._name}
        Level: {self.level}
        HP: {self.hp}
        MP: {self.mp}
        Race: {self.race}
        Attributes: {self.attributes}
        Profession: {self._profession}
        Skills: {self.skills}
        Inventory: {self._inventory}
        History: {self.history}
        ''')

class Player(Character):
    def __init__(self):
        super.__init__(self)
        self._faction = ''
