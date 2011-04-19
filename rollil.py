"""This will define the intermediary language."""

from rollenum import *

class RollInstruction:
    """This will hold the different functions/instructions."""
    function = None
    data = None
    def __init__(self, function, data):
        self.function=function
        self.data=data

    def __repr__(self):
        return "RollInstruction: {0} -> {1}".format(self.function, self.data)

class DiceRoll:
    """Dice roll structure"""
    isNegative = False
    dieType = ''
    rolls = None
    def __init__(self, is_neg, dtype, r):
        self.isNegative=is_neg
        self.dieType=dtype
        self.rolls=r

    def __repr__(self):
        n = (self.isNegative and -len(self.rolls) or len(self.rolls))
        return "DiceRoll: {0}{1}".format(n, self.dieType)

class ExpandedRoll:
    """Expanded roll structure"""
    rollIteration = None
    numRolls = 0
    def __init__(self, roll_iteration, num_rolls):
        self.rollIteration = roll_iteration
        if self.rollIteration.isNegative:
            if num_rolls<0:
                self.rollIteration.isNegative = False
        elif num_rolls<0:
            self.rollIteration.isNegative = True
        self.numRolls = abs(num_rolls)

    def __repr__(self):
        return "ExpandedRoll: {0}x({1})".format(self.numRolls, str(self.rollIteration))
