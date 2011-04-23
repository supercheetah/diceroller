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
    roll = None
    eqnStr = ''
    diceSum = None
    numRolls = -1
    
    def __init__(self, is_neg, dtype, r, num_rolls):
        self.isNegative=is_neg
        self.dieType=dtype
        self.rolls=r
        self.numRolls = num_rolls

    def __repr__(self):
        n = (self.isNegative and -len(self.rolls) or len(self.rolls))
        return "DiceRoll: {0}{1}".format(n, self.dieType)

    def sum( self, negate ):
        self.diceSum = 0
        self.eqnStr = ''
        self.diceSum += self.roll()
        if self.isNegative:
            self.eqnStr += '-'
        self.eqnStr += '({0}: '.format(self.dieType)

        if 1<self.numRolls:
            for i in self.numRolls:
                dval = self.roll()
                self.diceSum += -dval if self.isNegative else dval # I found out too late that this syntax is available
                self.eqnStr += ' + {0}'.format(dval)
        self.eqnStr += ')'

        if negate:
            self.diceSum = -self.diceSum

        return self.eqnStr, self.diceSum

    def hasSum( self ):
        return ('' != self.eqnStr) and (None !=self.diceSum)

class ExpandedRoll:
    """Expanded roll structure"""
    rollIteration = None
    numRolls = 0
    eqnStr = ''
    adderExtension = []
    
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
        roll_sum, self.eqnStr = self.rollIteration.sum(negate)
        self.adderExtension = [roll_sum]
        for i in range(1, self.numRolls):
            roll_sum, dice_str = self.rollIteration.sum(negate)
            self.adderExtension.append(roll_sum)
            self.eqnStr += ' + '+dice_str

        return self.eqnStr, self.adderExtension

    def insertAdderExtension(self, other_list):
        buffer = self.adderExtension[:]
        buffer.extend(other_list)
        return buffer

    def hasExpansion( self ):
        return ('' != self.eqnStr) and ([] != self.adderExtension)
