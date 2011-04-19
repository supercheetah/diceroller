import logging
from rollenum import *

xor = lambda x,y: (not x and y) or (not y and x)

def dice_add( (dice_type, dice_rolls, is_neg), negate ):
    eqn_str = ''
    dice_sum = 0
    d0 = dice_rolls.pop(0)
    dice_sum += d0() # Performs the actual roll here.
    if is_neg:
        eqn_str += '-'
    eqn_str += '({0}: '.format(dice_type)
    eqn_str += '{0}'.format(dice_sum)
    for dice in dice_rolls:
        dval = dice() # Performs the actual roll here.
        dice_sum += is_neg and -dval or dval
        eqn_str += ' + {0}'.format(dval)
    eqn_str += ')'
    dice_rolls.insert(0, d0) # We need to put the first roll back in for the other lists, or else it just disappears.

    if negate:
        dice_sum = -dice_sum

    return eqn_str, dice_sum

def process_instructions( bytecode ):
    """This does the processing of the raw equation."""
    adder = []
    negate = False
    eqn_str = ''
    c_grp_count = 0
    logging.debug("process raw:")
    for instruction in bytecode:
        # This was quick and dirty. Each of the
        # different instructions's logic should probably
        # be separated into their own function.
        op_fn, data = instruction
        if op_fn == Fn.constant:            
            eqn_str += str(data)
            adder.insert(0, str(negate and -data or data)) # Turn it into a string to signify it's a constant
            negate = False
            logging.debug(str(eqn_str)+'\n\t'+str(adder))
        elif op_fn == Fn.const_grouping:
            adder.insert(0, str(negate and -data or data))
            c_grp_count += 1
            eqn_str += '[{0}: {1}]'.format(c_grp_count, data)
            negate = False
            logging.debug(str(eqn_str)+'\n\t'+str(adder))
        elif op_fn == Fn.dice:
            dice_str, dice_sum = dice_add(data, negate)
            eqn_str += dice_str
            adder.insert(0, dice_sum)
            negate = False
            logging.debug(str(eqn_str)+'\n\t'+str(adder))
        elif op_fn == Fn.xdice:
            dice_type, dice_rolls = data
            roll0, is_neg = dice_rolls.pop(0)
            dice_str, _sum = dice_add( (dice_type, roll0, is_neg), negate )
            eqn_str += dice_str
            adder.insert(0, _sum)
            for roll in dice_rolls:
                roll_iter, is_neg = roll
                dice_str, _sum = dice_add( (dice_type, roll_iter, is_neg), negate )
                eqn_str += ' + '+dice_str
                adder.insert(0, _sum)
            dice_rolls.insert(0, (roll0, is_neg))
            negate = False
            logging.debug(str(eqn_str)+'\n\t'+str(adder))
        elif op_fn == Fn.var_grouping:
            is_negative = data.pop()
            var_str, var_adder = process_instructions( data )
            if xor(negate, is_negative):
                neg_var_adder = []
                for i in var_adder:
                    if isinstance(i, int):
                        neg_var_adder.append(-i)
                    else:
                        neg_var_adder.append(str(-int(i)))
                var_adder = neg_var_adder
            if is_negative:
                eqn_str += '-('+var_str+')'
            else:
                eqn_str += '('+var_str+')'
            data.append(is_negative)
            adder.append(var_adder)
            negate = False
            logging.debug(str(eqn_str)+'\n\t'+str(adder))
        elif op_fn == Fn.op:
            op_str = ' + '
            if data == Ops.sub:
                negate = True
                op_str = ' - '
            eqn_str += op_str
            logging.debug(str(eqn_str)+'\n\t'+str(adder))
    return eqn_str, adder

def add_up( num_array, addition ):
    _sum = 0
    const_adder = 0
    add_later = 0
    for i in num_array:
        if isinstance( i, int ):
            _sum += i + addition
        elif isinstance( i, str ):
            const_adder += int(i)
        else:
            _sum += const_adder
            _sum, add_later = add_up( i, _sum )
            _sum += add_later
    return _sum, const_adder

def _compile( bytecode ):
    """doesn't really have another purpose other than
    to call process_instructions"""
    eqn_str, result = process_instructions(bytecode)
    last_elem = result[len(result)-1]
    if isinstance(last_elem, str) or isinstance(last_elem, int):
        result.append([0]) # This takes care of the corner case where there are no var_groupings
    final, garbage = add_up( result, 0 )
    logging.debug("final: "+str(final))
    return eqn_str, final

def compile( bytecode ):
    """temporary debug version of the above"""
    print bytecode
    return '', 0
