"""This will define the intermediary language."""

from rollenum import *
from collections import deque

class RollInstruction:
    """This will hold the different functions/instructions."""
    opFn = None
    data = None
    def __init__(self, function, data):
        self.opFn=function
        self.data=data

    def __repr__(self):
        return "RollInstruction: {0} -> {1}".format(self.opFn, self.data)

class DiceRoll:
    """Dice roll structure"""
    isNegative = False
    dieType = ''
    roll = None
    eqnStr = ''
    diceSum = None
    numRolls = -1
    
    def __init__(self, is_neg, dtype, r, num_rolls):
        self.isNegative=is_neg
        self.dieType=dtype
        self.roll=r
        self.numRolls = num_rolls

    def __repr__(self):
        n = -self.numRolls if self.isNegative else self.numRolls
        return "DiceRoll: {0}{1}".format(n, self.dieType)

    def __call__(self, negate, multiplier=1):
        return self.sum(negate, multiplier)

    def sum( self, negate, multipier=1 ):
        self.diceSum = 0
        self.eqnStr = ''
        self.diceSum += self.roll()
        if self.isNegative:
            self.eqnStr += '-'
        self.eqnStr += '<{0}: {1}'.format(self.dieType, self.diceSum)

        if 1<self.numRolls:
            for i in range(1, self.numRolls):
                dval = self.roll()
                self.diceSum += -dval if self.isNegative else dval # I found out too late that this syntax is available
                self.eqnStr += ' + {0}'.format(dval)
        self.eqnStr += '>'

        if negate:
            self.diceSum = -self.diceSum

        self.diceSum*=multipier

        return self.eqnStr, self.diceSum

    def hasSum( self ):
        return ('' != self.eqnStr) and (None !=self.diceSum)

class ExpandedRoll:
    """Expanded roll structure"""
    rollIteration = None
    numRolls = 0
    eqnStr = ''
    adderExtension = None
    
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

    def expand( self, negate ):
        self.eqnStr, roll_sum = self.rollIteration.sum(negate) #negation from subtraction is only applied on the first iteration
        self.adderExtension = deque([roll_sum])
        for i in range(1, self.numRolls):
            dice_str, roll_sum = self.rollIteration.sum(False)
            self.adderExtension.append(roll_sum)
            self.eqnStr += ' + '+dice_str

        return self.eqnStr, self.adderExtension

    def hasExpansion( self ):
        return ('' != self.eqnStr) and (None != self.adderExtension)
