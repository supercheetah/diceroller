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
    def __init__(self, fn, d):
        function=fn
        data=d

class DiceRoll:
    """Dice roll structure"""
    is_negative = False
    die_type = ''
    rolls = None
    def __init__(self, is_neg, dtype, r):
        is_negative=is_neg
        die_type=dtype
        rolls=r
        return self

class ExpandedRoll:
    """Expanded roll structure"""
    die_type = ''
    rolls = []
    is_negative = False
    def __init__(self, is_neg, dtype, single_roll_set, num_rolls):
        is_negative = is_neg
        die_type = dtype
        if is_neg:
            if num_rolls<0:
                is_negative = False
        elif num_rolls<0:
            is_negative = True
        for i in range(abs(num_rolls)):
            rolls.append(single_roll_set)
        return self
