"""This will define the intermediary language."""

from rollenum import *

class PStruct:
    """A python version of a C struct, makes my life easier."""
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class RollInstruction:
    """This will hold the different functions/instructions."""
    function = None
    data = None
    def __init__(self, fn, data_):
        function=fn
        data=data_

class DiceRoll:
    """Dice roll structure"""
    isNegative = False
    dieType = ''
    rolls = None
    def __init__(self, is_neg, dtype, r):
        isNegative=is_neg
        dieNype=dtype
        rolls=r
        return self

class ExpandedRoll:
    """Expanded roll structure"""
    rollIteration = []
    numRolls = 0
    def __init__(self, roll_iteration, num_rolls):
         rollIteration = roll_iteration
        if rollIteration.isNegative:
            if num_rolls<0:
                rollIteration.isNegative = False
        elif num_rolls<0:
            rollIteration.isNegative = True
        numRolls = abs(num_rolls)
        return self
