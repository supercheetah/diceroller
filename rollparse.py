from simpleparse.common import numbers,strings,comments
from simpleparse.parser import Parser
#from simpleparse.error import ParserSyntaxError
from dispexcept import VarNestedException, VarMultipleException
import logging
import lexer

declaration = r''' #this defines the language, of course
root          := roll
roll          := space,root_fn/sep_grouping,space
root_fn       := operations
operations    := function
function      := (dice,op,operations)/(grouping,op,operations)/(constant,op,operations)/(xdice,op,operations)/xdice/dice/constant/grouping
constant      := number
grouping      := var_grouping/const_grouping
var_grouping  := negation?,'(',space,operations,space,')'
const_grouping:= negation?,'[',space,operations,space,']'
negation      := '-'
sep_grouping  := '{',space,xdice,space,'}',(op,operations)?
sep_dice      := num_dice?,incl_zero,num_sides
dice          := num_dice?,incl_zero,num_sides
xdice         := number,'x',sep_dice # This will expand an expression, so '6x3d6' becomes '3d6+3d6+3d6', and returns it as a list
incl_zero     := [dD]
num_sides     := number
num_dice      := number
op            := space,[-+*],space
space         := [ \t]*
'''

class RollParser( Parser ):
    def BuildProcessor(self):
        try:
            return lexer.Lexer()
        except SyntaxError, se:
            raise se

rollparser = RollParser( declaration )

def space_carot( num_spaces ):
    s = ''
    for i in range(num_spaces):
        s += ' '
    s += '^'
    return s

def solve_roll( roll_str ):
    resolution = None
    try:
        success, children, nextchar = rollparser.parse( roll_str, processor=lexer.Lexer() )
        if not (success and len(roll_str)==nextchar):
            raise Exception(roll_str+'\n'+space_carot(nextchar+1)+"\nI'm sorry, but I don't understand that.")
    except SyntaxError, se:
        raise Exception(roll_str+'\n'+space_carot(se.position)+"\nThis doesn't look right.")
    except VarNestedException, nest_e:
        raise Exception(roll_str+'\n'+space_carot(nest_e.position)+"\nCan't nest variable groupings.")
    except VarMultipleException, mult_e:
        raise Exception(roll_str+'\n'+space_carot(mult_e.posotion)+"\nCan't have more than one variable grouping.")
        
    is_separated = lexer.is_separated()
    if is_separated:
        resolution = lexer.get_sep_grp_results()
    else:
        resolution = lexer.get_resolution()

    return is_separated, lexer.get_const_strings(), resolution
    
