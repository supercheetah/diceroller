"""This will define the intermediary language."""

from rollenum import *

class RollInstruction:
    """This will hold the different functions/instructions."""
    function = None
    data = None
    def __init__(self, function, data):
        self.function=fn
        self.data=data_

class DiceRoll:
    """Dice roll structure"""
    isNegative = False
    dieType = ''
    rolls = None
    def __init__(self, is_neg, dtype, r):
        self.isNegative=is_neg
        self.dieNype=dtype
        self.rolls=r

class ExpandedRoll:
    """Expanded roll structure"""
    rollIteration = []
    numRolls = 0
    def __init__(self, roll_iteration, num_rolls):
        self.rollIteration = roll_iteration
        if rollIteration.isNegative:
            if num_rolls<0:
                self.rollIteration.isNegative = False
        elif num_rolls<0:
            self.rollIteration.isNegative = True
        self.numRolls = abs(num_rolls)
